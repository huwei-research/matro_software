"""Tiny CPU math compatibility layer for the pinned Windows gfortran build.

The pinned gfortran -O2 build merges every paired sin/cos site in TRSAPP,
BIGLAG and BIGDEN into libmingwex sincos, using x87 FSINCOS. Independent
FSIN/FCOS are not always bitwise equivalent to the merged instruction.
This leaf routine reproduces FSINCOS and its large-argument range reduction,
with binary64 input/output. It contains no optimization logic or compiler dependency,
and neither load nor call the official NEWUOA/PDFO DLL. All solver operations
remain in the generated Python. The OS API is used only for executable memory.

Supported compatibility target: Windows x86_64, round-to-nearest CPU mode.
The instruction sequences and SHA256 are exposed for independent inspection.
"""
from __future__ import annotations
import ctypes
import hashlib
import platform
import sys
import math
from contextlib import contextmanager
from contextvars import ContextVar

_BACKEND = ContextVar('matro_math_backend', default='auto')

def _reference_platform():
    return sys.platform == 'win32' and platform.machine().lower() in ('amd64', 'x86_64')

def _use_reference():
    choice = _BACKEND.get()
    return choice == 'reference' or (choice == 'auto' and _reference_platform())

@contextmanager
def backend(choice):
    """Select arithmetic locally to a solve, including nested/threaded solves."""
    if choice not in ('auto', 'reference', 'portable'):
        raise ValueError('math_backend must be auto, reference, or portable')
    if choice == 'reference' and not _reference_platform():
        raise RuntimeError('reference arithmetic requires Windows x86_64')
    token = _BACKEND.set(choice)
    try:
        yield
    finally:
        _BACKEND.reset(token)

_PAGE = None
_FUNCTIONS = None

def _build():
    global _PAGE, _FUNCTIONS
    if _FUNCTIONS is not None:
        return _FUNCTIONS
    if sys.platform != 'win32' or platform.machine().lower() not in ('amd64','x86_64'):
        raise RuntimeError('Exact PDFO 2.2.0 math compatibility requires Windows x86_64')
    # Windows ABI: x in xmm0, sin output pointer rdx, cos output pointer r8.
    # FSINCOS returns cos in st(0), sin in st(1). If C2 is raised, reduce
    # modulo 2*pi with FPREM1, as in the pinned libmingwex sincos routine.
    code = bytes.fromhex(
        '48 83 ec 18 f2 0f 11 44 24 08 dd 44 24 08 d9 fb '
        'df e0 a9 00 04 00 00 74 15 d9 eb d8 c0 d9 c9 '
        'd9 f5 df e0 a9 00 04 00 00 75 f5 dd d9 d9 fb '
        'd9 c9 dd 1a 41 dd 18 48 83 c4 18 c3')
    kernel = ctypes.WinDLL('kernel32',use_last_error=True)
    kernel.VirtualAlloc.argtypes=(ctypes.c_void_p,ctypes.c_size_t,ctypes.c_ulong,ctypes.c_ulong)
    kernel.VirtualAlloc.restype=ctypes.c_void_p
    kernel.VirtualProtect.argtypes=(ctypes.c_void_p,ctypes.c_size_t,ctypes.c_ulong,ctypes.POINTER(ctypes.c_ulong))
    kernel.VirtualProtect.restype=ctypes.c_int
    kernel.FlushInstructionCache.argtypes=(ctypes.c_void_p,ctypes.c_void_p,ctypes.c_size_t)
    kernel.FlushInstructionCache.restype=ctypes.c_int
    address=kernel.VirtualAlloc(None,len(code),0x3000,0x04)
    if not address:
        raise ctypes.WinError(ctypes.get_last_error())
    ctypes.memmove(address,code,len(code))
    old=ctypes.c_ulong()
    if not kernel.VirtualProtect(address,len(code),0x20,ctypes.byref(old)):
        raise ctypes.WinError(ctypes.get_last_error())
    kernel.FlushInstructionCache(ctypes.c_void_p(-1),address,len(code))
    pointer=ctypes.POINTER(ctypes.c_double)
    prototype=ctypes.CFUNCTYPE(None,ctypes.c_double,pointer,pointer)
    _PAGE=(address,code)
    _FUNCTIONS=prototype(address)
    return _FUNCTIONS

def metadata():
    if not _use_reference():
        return {'implementation': 'Python math.sin/cos (platform libm)',
                'bitwise_reference_parity': False, 'platform': sys.platform,
                'official_library_calls': False, 'compiler_required': False}
    _build()
    return {'implementation':'x87 FSINCOS paired local CPU primitive',
            'version':2,
            'platform':'Windows x86_64','bytes':len(_PAGE[1]),
            'machine_code_hex':_PAGE[1].hex(),
            'machine_code_sha256':hashlib.sha256(_PAGE[1]).hexdigest(),
            'official_library_calls':False,'compiler_required':False}

def sincos(x):
    if not _use_reference():
        return math.sin(x), math.cos(x)
    sine,cosine=ctypes.c_double(),ctypes.c_double()
    _build()(x,ctypes.byref(sine),ctypes.byref(cosine))
    return sine.value,cosine.value

def sin(x):
    return sincos(x)[0]

def cos(x):
    return sincos(x)[1]
