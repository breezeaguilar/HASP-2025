import ctypes

lib = ctypes.CDLL("HASP_2025_build/libHASP_2025_C_lib.so")

lib.square.argtypes = [ctypes.c_float]
lib.square.restype = ctypes.c_float

print(lib.square(2))