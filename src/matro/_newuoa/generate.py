"""Translate the pinned PDFO NEWUOA Fortran subset, without numerical rewrites.

Generated Python uses scalar operations and explicit basic-block jumps. This is
a deliberately narrow source translator, not a general Fortran compiler.
"""
from __future__ import annotations
import ast
import hashlib
import json
import re
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
NAMES = ('newuoa', 'newuob', 'trsapp', 'biglag', 'bigden', 'update')
REFERENCE = HERE/'reference_source'
SOURCE = REFERENCE

def split_args(text):
    depth = 0
    start = 0
    result = []
    for i, c in enumerate(text):
        depth += (c == '(') - (c == ')')
        if c == ',' and depth == 0:
            result.append(text[start:i].strip())
            start = i + 1
    result.append(text[start:].strip())
    return result

def statements(path):
    result = []
    for lineno, raw in enumerate(path.read_text().splitlines(), 1):
        if not raw.strip() or raw[0] in 'Cc*!':
            continue
        text = raw[6:72].split('!')[0].strip().lower()
        if not text:
            continue
        if raw[5:6] not in (' ', '0', ''):
            result[-1][2] += ' ' + text
        else:
            result.append([lineno, raw[:5].strip(), text])
    return result

def integer_name(name):
    return name[0] in 'ijklmn'

class Expressions(ast.NodeTransformer):
    def __init__(self, arrays):
        self.arrays = arrays

    def isint(self, node):
        if isinstance(node, ast.Constant):
            return isinstance(node.value, int)
        if isinstance(node, ast.Name):
            return integer_name(node.id)
        if isinstance(node, ast.UnaryOp):
            return self.isint(node.operand)
        if isinstance(node, ast.BinOp):
            return self.isint(node.left) and self.isint(node.right)
        if isinstance(node, ast.Call):
            return isinstance(node.func, ast.Name) and node.func.id in ('max0', 'min0', 'int')
        return False

    def visit_BinOp(self, node):
        integral = self.isint(node.left) and self.isint(node.right)
        node = self.generic_visit(node)
        if isinstance(node.op, ast.Div) and integral:
            return ast.Call(ast.Name('_idiv', ast.Load()), [node.left, node.right], [])
        if isinstance(node.op, ast.Pow) and isinstance(node.right, ast.Constant):
            power = node.right.value
            if power in (2, 3, 4):
                # GCC's scalar integer exponent expansion uses squaring for 4.
                square = ast.BinOp(node.left, ast.Mult(), node.left)
                if power == 2:
                    return square
                if power == 3:
                    return ast.BinOp(square, ast.Mult(), node.left)
                return ast.BinOp(square, ast.Mult(), square)
        if isinstance(node.op, ast.Div):
            # IEEE zero division rather than Python's ZeroDivisionError.
            return ast.Call(ast.Name('_div', ast.Load()), [node.left, node.right], [])
        return node

    def visit_Call(self, node):
        name = node.func.id
        node = self.generic_visit(node)
        if name in self.arrays:
            return ast.Subscript(ast.Name(name, ast.Load()),
                node.args[0] if len(node.args) == 1 else ast.Tuple(node.args, ast.Load()), ast.Load())
        names = {'dsqrt':'_sqrt','dabs':'abs','dmin1':'_min','dmax1':'_max',
                 'min':'_min','max':'_max','max0':'max','min0':'min','dfloat':'float',
                 'datan':'_atan','dcos':'_cos','dsin':'_sin','huge':'_huge'}
        if name not in names:
            raise ValueError('Unknown intrinsic ' + name)
        node.func = ast.Name(names[name], ast.Load())
        return node

    def convert(self, text):
        text = re.sub(r'(\d+(?:\.\d*)?|\.\d+)d([+-]?\d+)', r'\1e\2', text)
        for src, dest in (('.and.',' and '),('.or.',' or '),('.not.',' not '),('/=','!=')):
            text = text.replace(src, dest)
        node = self.visit(ast.parse(text.strip(), mode='eval').body)
        return ast.unparse(ast.fix_missing_locations(node))

def header(items):
    name, params = re.match(r'subroutine\s+(\w+)\s*\((.*)\)', items[0][2]).groups()
    arrays = {}
    for _, _, text in items:
        if text.startswith('dimension '):
            for item in split_args(text[10:]):
                array, dimensions = re.match(r'(\w+)\((.*)\)', item).groups()
                arrays[array] = split_args(dimensions)
    return name, split_args(params), arrays

def compile_routine(items, specs):
    name, params, arrays = header(items)
    expr = Expressions(arrays).convert
    instructions, labels, stack, origins = [], {}, [], []
    def emit(kind, *args):
        instructions.append([kind, *args])
        return len(instructions)-1
    def condition(text):
        start = text.index('(')
        depth = 0
        for i in range(start, len(text)):
            depth += (text[i] == '(') - (text[i] == ')')
            if depth == 0:
                return text[start+1:i], text[i+1:].strip()
        raise ValueError(text)
    def action(text):
        if text.startswith(('goto ', 'go to ')):
            emit('goto_label', text.split()[-1]); return
        if text == 'return':
            emit('return'); return
        if text.startswith(('print ', 'format ')) or text == 'continue':
            emit('code', 'pass'); return
        if text.startswith('call '):
            callee, actuals = re.match(r'call\s+(\w+)\s*\((.*)\)', text).groups()
            actuals = split_args(actuals)
            if callee == 'calfun':
                emit('code', 'f = _ctx.objective(n, x)'); return
            _, formal, ca = specs[callee]
            arguments, outputs = [], []
            for form, actual in zip(formal, actuals):
                if form in ca:
                    if '(' in actual:
                        a, idx = re.match(r'(\w+)\((.*)\)', actual).groups()
                        arguments.append(f'{a}.tail({expr(idx)})')
                    else:
                        arguments.append(actual)
                else:
                    arguments.append(expr(actual))
                    outputs.append(actual)
            emit('code', ', '.join(outputs) + ' = _' + callee + '(_ctx, ' + ', '.join(arguments) + ')')
            return
        if text.startswith('if '):
            cond, body = condition(text)
            at = emit('branch', 'not (' + expr(cond) + ')', None)
            action(body)
            instructions[at][2] = len(instructions)
            return
        match = re.match(r'([^=]+)=(.*)', text)
        if not match:
            raise ValueError('Unknown statement ' + text)
        lhs, rhs = match.groups()
        lhs = lhs.strip()
        target = expr(lhs)
        value = expr(rhs)
        if '(' not in lhs:
            value = ('int' if integer_name(lhs) else 'float') + '(' + value + ')'
        emit('code', target + ' = ' + value)

    for line, label, text in items[1:]:
        previous_count = len(instructions)
        if label:
            labels[label] = len(instructions)
        if text.startswith(('implicit ', 'dimension ')) or text == 'end':
            continue
        if text.startswith('else if '):
            frame = stack[-1]
            skip = emit('jump', None)
            frame['skips'].append(skip)
            instructions[frame['branch']][2] = len(instructions)
            cond, body = condition(text)
            assert body == 'then'
            frame['branch'] = emit('branch', 'not (' + expr(cond) + ')', None)
        elif text == 'else':
            frame = stack[-1]
            frame['skips'].append(emit('jump', None))
            instructions[frame['branch']][2] = len(instructions)
            frame['branch'] = None
        elif text == 'end if':
            frame = stack.pop()
            assert frame['kind'] == 'if'
            if frame['branch'] is not None:
                instructions[frame['branch']][2] = len(instructions)
            for skip in frame['skips']:
                instructions[skip][1] = len(instructions)
        elif text.startswith('if ') and text.endswith('then'):
            cond, _ = condition(text)
            stack.append({'kind':'if','branch':emit('branch', 'not (' + expr(cond) + ')', None), 'skips':[]})
        elif text.startswith('do '):
            var, bounds = text[3:].split('=', 1)
            var = var.strip()
            bounds = split_args(bounds)
            start, end = map(expr, bounds[:2])
            step = expr(bounds[2]) if len(bounds) == 3 else '1'
            unique = str(len(instructions))
            endvar, stepvar = '_end' + unique, '_step' + unique
            emit('code', f'{var} = int({start}); {endvar} = int({end}); {stepvar} = int({step})')
            at = emit('branch', f'({var} > {endvar} if {stepvar} > 0 else {var} < {endvar})', None)
            stack.append({'kind':'do', 'branch':at, 'var':var, 'step':stepvar})
        elif text == 'end do':
            frame = stack.pop()
            assert frame['kind'] == 'do'
            emit('code', frame['var'] + ' += ' + frame['step'])
            emit('jump', frame['branch'])
            instructions[frame['branch']][2] = len(instructions)
        else:
            action(text)
        if name == 'newuob' and label == '100':
            emit('code', 'idz, delta, rho, xoptsq, diffa, diffb, diffc, itest = _ctx.observe(locals())')
        origins.extend([{'line':line,'statement':text}]*(len(instructions)-previous_count))
    assert not stack
    for instruction in instructions:
        if instruction[0] == 'goto_label':
            instruction[:] = ['jump', labels[instruction[1]]]
    leaders = {0}
    for i, op in enumerate(instructions):
        if op[0] in ('jump', 'branch', 'return'):
            if i+1 < len(instructions):
                leaders.add(i+1)
            if op[0] in ('jump','branch'):
                leaders.add(op[-1])
    leaders = sorted(leaders)
    # All scalar arguments are returned. Arrays mutate their shared storage.
    scalar_params = [p for p in params if p not in arrays]
    ret = 'return ' + ', '.join(scalar_params)
    lines = ['def _' + name + '(_ctx, ' + ', '.join(params) + '):']
    scalar_names = set()
    for _, _, text in items[1:]:
        if text.startswith(('implicit','dimension','format','print')):
            continue
        scalar_names.update(re.findall(r'\b[a-z][a-z0-9_]*\b', re.sub(r"'[^']*'", '', text)))
    reserved = set(params) | set(arrays) | {'if','then','else','end','do','call','goto','go','to','return','and','or','not','continue'}
    for var in sorted(scalar_names - reserved):
        if var in ('d0','d1','d2','d3','d4','d8') or var in specs:
            continue
        lines.append(f'    {var} = ' + ('0' if integer_name(var) else '0.0'))
    for arr, shape in arrays.items():
        if arr in params:
            if len(shape) == 2:
                lines.append(f'    {arr} = {arr}.with_leading({expr(shape[0])})')
        else:
            lines.append(f'    {arr} = FArray.zeros({expr(shape[0])})')
    lines += ['    _pc = 0', '    while True:']
    blocks = []
    for b, start in enumerate(leaders):
        finish = leaders[b+1] if b+1 < len(leaders) else len(instructions)
        block = []
        for op in instructions[start:finish]:
            if op[0] == 'code':
                block.append(op[1])
            elif op[0] == 'branch':
                block += ['if ' + op[1] + ':', f'    _pc = {op[2]}', '    continue']
            elif op[0] == 'jump':
                block += [f'_pc = {op[1]}', 'continue']
            elif op[0] == 'return':
                block.append(ret)
        if not block or block[-1] not in ('continue', ret):
            block += [f'_pc = {finish}', 'continue'] if finish < len(instructions) else [ret]
        blocks.append((start,block))
    def dispatch(blocks, indent):
        if len(blocks) == 1:
            start, block = blocks[0]
            lines.append(' '*indent + f'# {name}: basic block {start}')
            lines.extend(' '*indent + line for line in block)
        else:
            mid = len(blocks)//2
            lines.append(' '*indent + f'if _pc < {blocks[mid][0]}:')
            dispatch(blocks[:mid], indent+4)
            lines.append(' '*indent + 'else:')
            dispatch(blocks[mid:], indent+4)
    dispatch(blocks,8)
    return '\n'.join(lines), {'source_labels':labels,'instructions':instructions,
                             'instruction_source':origins,'blocks':leaders}

def main():
    all_items = {name:statements(SOURCE/(name+'.f')) for name in NAMES}
    specs = {name:header(items) for name,items in all_items.items()}
    generated = ['"""Generated from PDFO 2.2.0 maintained NEWUOA; see LICENSE and provenance.json.\nDo not edit: run generate.py to reproduce this file.\n"""',
                 'from .runtime import FArray, _div, _idiv, _sqrt, _atan, _sin, _cos, _min, _max, _huge']
    maps = {}
    for name,items in all_items.items():
        code, maps[name] = compile_routine(items,specs)
        generated.append(code)
    result = '\n\n'.join(generated)+'\n'
    compile(result,'generated.py','exec')
    (HERE/'generated.py').write_text(result,encoding='utf-8')
    (HERE/'source_map.json').write_text(json.dumps(maps,indent=2),encoding='utf-8')
    source_copy = HERE/'reference_source'
    source_copy.mkdir(exist_ok=True)
    hashes = {}
    for name in NAMES:
        path=SOURCE/(name+'.f')
        if path.resolve() != (source_copy/path.name).resolve():
            shutil.copy2(path,source_copy/path.name)
        hashes[path.name]=hashlib.sha256(path.read_bytes()).hexdigest()
    if not (HERE/'LICENSE.txt').exists():
        license_path=SOURCE.parents[1]/'LICENCE.txt'
        if not license_path.exists():
            license_path=next(SOURCE.parents[1].glob('*LICEN*'))
        shutil.copy2(license_path,HERE/'LICENSE.txt')
    (HERE/'provenance.json').write_text(json.dumps({'source':'PDFO 2.2.0 maintained Fortran NEWUOA',
        'source_sha256':hashes,'generated_sha256':hashlib.sha256((HERE/'generated.py').read_bytes()).hexdigest(),
        'math_backend':'x87 FSINCOS paired instruction matching all six merged sincos call sites in the pinned -O2 build',
        'math_backend_sha256':hashlib.sha256((HERE/'x87_math.py').read_bytes()).hexdigest(),
        'changes':'Scalar Python translation; silent iprint=0; optional state hook at NEWUOB label 100.'},indent=2),encoding='utf-8')
    print('Generated',len(result.splitlines()),'Python lines')

if __name__ == '__main__':
    main()
