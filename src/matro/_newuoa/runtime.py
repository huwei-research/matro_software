"""IEEE scalar arithmetic and Fortran-compatible shared array views."""
from __future__ import annotations
import math
import numpy as np
from .x87_math import sin as _x87_sin, cos as _x87_cos

def _div(a, b):
    if b != 0:
        return a / b
    if a == 0 or math.isnan(a):
        return math.nan
    return math.copysign(math.inf, a) * math.copysign(1., b)

def _idiv(a, b):
    return abs(a)//abs(b) * (-1 if (a < 0) != (b < 0) else 1)

def _sqrt(x):
    return math.sqrt(x) if x >= 0 else math.nan

def _sin(x):
    return _x87_sin(x) if math.isfinite(x) else math.nan

def _cos(x):
    return _x87_cos(x) if math.isfinite(x) else math.nan

_atan = math.atan

def _min(*args):
    value=args[0]
    for other in args[1:]:
        # SSE min chooses its second operand for unordered/equal operands.
        value=value if value < other else other
    return value

def _max(*args):
    value=args[0]
    for other in args[1:]:
        value=value if value > other else other
    return value

def _huge(_):
    return float.fromhex('0x1.fffffffffffffp+1023')

class FArray:
    """One-based column-major array, including Fortran sequence association."""
    __slots__=('data','leading')
    def __init__(self,data,leading=0):
        self.data=data
        self.leading=leading
    @classmethod
    def zeros(cls,size):
        return cls(np.zeros(size,dtype=np.float64))
    def with_leading(self,leading):
        return FArray(self.data,leading)
    def tail(self,first):
        return FArray(self.data[first-1:])
    def __getitem__(self,index):
        if isinstance(index,tuple):
            i,j=index
            return float(self.data[i-1+self.leading*(j-1)])
        return float(self.data[index-1])
    def __setitem__(self,index,value):
        if isinstance(index,tuple):
            i,j=index
            self.data[i-1+self.leading*(j-1)]=value
        else:
            self.data[index-1]=value
    def array(self,shape):
        return self.data[:int(np.prod(shape))].reshape(shape,order='F')
