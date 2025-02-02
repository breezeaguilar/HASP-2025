import ctypes

lib = ctypes.CDLL("build/libHASP_2025_C_lib.so")

lib.square.argtypes = [ctypes.c_float]
lib.square.restype = ctypes.c_float

def square(x) :
    global lib
    return lib.square(2)

print(square(2))

