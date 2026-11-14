"""Fully local scalar-Python translation of PDFO 2.2.0 NEWUOA.

No Fortran, optimizer DLL, PDFO installation or compilation is used. The
Windows x86_64 CPU math compatibility layer is documented in x87_math.py.
"""
from __future__ import annotations
import math
from pathlib import Path
import numpy as np
from .runtime import FArray
from .generated import _newuoa
from .x87_math import metadata as math_metadata

class _Context:
    def __init__(self,fun,hook,variant):
        self.fun=fun
        self.hook=hook
        self.variant=variant
        self.queries=[]
        self.values=[]
        self.errors=[]
        self.hook_calls=0
        self.evaluations=0

    def objective(self,n,x):
        self.evaluations+=1
        value=math.inf
        if not self.errors:
            point=x.array((n,)).copy()
            try:
                value=float(self.fun(point))
                self.queries.append(point)
                self.values.append(value)
            except BaseException as error:
                self.errors.append(error)
        return 2.0**100 if math.isnan(value) or value>2.0**100 else value

    def observe(self,frame):
        scalars=('idz','delta','rho','xoptsq','diffa','diffb','diffc','itest')
        original=tuple(frame[k] for k in scalars)
        if self.variant!='hooked':
            return original
        self.hook_calls+=1
        if self.hook is None or self.errors:
            return original
        n,npt,ndim=(frame[k] for k in ('n','npt','ndim'))
        state={k:frame[k] for k in ('n','npt','nf','ndim','kopt')}
        shapes={'x':(n,),'xbase':(n,),'xopt':(n,),'xnew':(n,),
                'xpt':(npt,n),'fval':(npt,),'gq':(n,),'hq':(n*(n+1)//2,),
                'pq':(npt,),'bmat':(ndim,n),'zmat':(npt,npt-n-1)}
        for k,shape in shapes.items():
            state[k]=frame[k].array(shape)
        for k in scalars:
            state[k]=np.array([frame[k]],dtype=np.int32 if k in ('idz','itest') else np.float64)
        try:
            self.hook(state)
        except BaseException as error:
            self.errors.append(error)
        return tuple(int(state[k][0]) if k in ('idz','itest') else float(state[k][0]) for k in scalars)

class PythonNewuoa:
    """NativeNewuoa-compatible local implementation; see provenance.json."""
    def __init__(self,variant='plain',build_dir=None):
        if variant not in ('plain','hooked'):
            raise ValueError(variant)
        self.variant=variant
        self.path=Path(__file__).with_name('generated.py')

    def run(self,fun,x0,*,npt=None,rhobeg=1.,rhoend=1e-8,maxfun=1000,
            ftarget=-np.inf,hook=None):
        x=np.array(x0,dtype=np.float64,copy=True)
        if x.ndim!=1 or x.size<2 or not np.all(np.isfinite(x)):
            raise ValueError('x0 must be a finite one-dimensional array of size at least two')
        n=x.size
        npt=(n+1)*(n+2)//2 if npt is None else int(npt)
        if not n+2<=npt<=(n+1)*(n+2)//2:
            raise ValueError('invalid npt')
        if not (np.isfinite(rhobeg) and np.isfinite(rhoend) and 0<rhoend<=rhobeg):
            raise ValueError('require finite 0 < rhoend <= rhobeg')
        if int(maxfun)!=maxfun or maxfun<=0:
            raise ValueError('maxfun must be a positive integer')
        if np.isnan(ftarget):
            raise ValueError('ftarget must not be NaN')
        if hook is not None and self.variant!='hooked':
            raise ValueError('plain core has no state hook')
        ctx=_Context(fun,hook,self.variant)
        work=FArray.zeros((npt+13)*(npt+n)+3*n*(n+3)//2+1)
        out=_newuoa(ctx,n,npt,FArray(x),float(rhobeg),float(rhoend),0,int(maxfun),work,
                    math.nan,-999,float(ftarget))
        if ctx.errors:
            raise RuntimeError('callback failed during NEWUOA') from ctx.errors[0]
        result,info=out[-3:-1]
        assert ctx.evaluations==len(ctx.queries) and ctx.evaluations<=maxfun
        raw_values=np.array(ctx.values)
        mask=np.isnan(raw_values)|(raw_values>2.0**100)
        return {'x':x,'fun':result,'status':info,'nfev':ctx.evaluations,
                'queries':np.array(ctx.queries),'values':raw_values,
                'model_values':np.where(mask,2.0**100,raw_values),
                'barrier':{'threshold':2.0**100,'replaced':int(np.count_nonzero(mask)),
                           'negative_infinity_preserved':True},
                'hook_calls':ctx.hook_calls,'library':str(self.path),'variant':self.variant,
                'math_backend':math_metadata(),
                'implementation':'pdfo-2.2.0-scalar-python-002-fsincos'}
