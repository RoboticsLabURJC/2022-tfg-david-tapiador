from ctypes import Structure, c_char, c_int64

class MD(Structure):
    _fields_ = [
        ('shape_0', c_int64),
        ('size', c_int64),
        ('count', c_int64)
    ]
