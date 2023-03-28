from numba import njit
import numpy as np
import ctypes
import gmpy2
from numpy.ctypeslib import ndpointer


@njit
def simpleSieve(limit):
    mark = np.ones(limit+1, dtype=np.uint8)
    mark[:2] = 0
    for i in range(2, int(np.sqrt(limit))+1):
        if mark[i]:
            mark[i*i::i] = 0  
    return np.where(mark==1)[0].astype(np.uint32)

    
@njit
def nn(prime,mod,inv,max):
   res=np.ones(max+1,dtype=np.uint8)
   for p,m,i in zip(primes,mod,inv):
       res[((p-(m))*i)%p::p]=False
       res[((p-(m+4)%p)*i)%p::p]=False
       res[((p-(m+6)%p)*i)%p::p]=False
       res[((p-(m+10)%p)*i)%p::p]=False
       res[((p-(m+12)%p)*i)%p::p]=False
       
   return np.where(res==1)[0].astype(np.uint32)

def inverse(hash,p):
     return gmpy2.powmod(hash, int(p-2),int(p))

def mine(T,prime,inv,max,offset):
    primorial=gmpy2.primorial(223)
    T = int((T+primorial)-(T%primorial))+offset
    lib = ctypes.CDLL('./pradeep.so')
    lib.get_uint_arrays_py.argtypes = [ctypes.c_char_p,ndpointer(ctypes.c_uint32, flags="C_CONTIGUOUS"),ndpointer(ctypes.c_uint32, 
    flags="C_CONTIGUOUS"),ctypes.c_uint32]
    mod=np.zeros(len(prime),dtype=np.uint32)
    T=str(hex(T))[2:]
    lib.get_uint_arrays_py(T.encode('utf-8'),prime,result,len(mod))
    r=nn(prime,mod,inv,max)
    fac=0
    for l in r:
         n=primorial*l+T
         if gmpy2.is_fermat_prp(n,2)==1 and gmpy2.is_fermat_prp(n+4,2)==1 and gmpy2.is_fermat_prp(n+6,2)==1 and gmpy2.is_fermat_prp(n+10,2)==1 and gmpy2.is_fermat_prp(n+12,2)==1: 
          fac=l
          break
    return fac



     