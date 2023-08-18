import ctypes

class C_Response(ctypes.Structure):
    _fields_ = [
        ('errCode', ctypes.c_int),
        ('errMsg', ctypes.POINTER(ctypes.c_char_p))
    ]

class C_Node(ctypes.Structure):
    _fields_ = [
        ('ai_model', ctypes.c_char * 64),
        ('hash', ctypes.c_char * 64),
        ('normal', ctypes.c_char * 2),
        ('vdim', ctypes.c_int),
        ('vp', ctypes.c_double * 2048)
    ]    

class C_PutVectorRS(ctypes.Structure):
    _fields_ = [
        ('errCode', ctypes.c_int),
        ('errMsg', ctypes.POINTER(ctypes.c_char_p)),
        ('hash', ctypes.POINTER(ctypes.c_char_p))  
    ]

class C_GetVectorRS(ctypes.Structure):
    _fields_ = [
        ('errCode', ctypes.c_int),
        ('errMsg', ctypes.POINTER(ctypes.c_char_p)),
        ('node', C_Node)
    ]

class C_QueryVectorRS(ctypes.Structure):
    _fields_ = [
        ('errCode', ctypes.c_int),
        ('errMsg', ctypes.c_char * 18),
        ('ai_model', ctypes.c_char * 64),
        ('normal', ctypes.c_char * 2),
        ('hash', ctypes.c_char * 64),
        ('vdim', ctypes.c_int),
        ('distance', ctypes.c_double)
    ]  

class C_QueryVectorRSWrapper(ctypes.Structure):
    _fields_ = [
        ('errCode', ctypes.c_int),
        ('errMsg', ctypes.POINTER(ctypes.c_char_p)),
        ('queryCount', ctypes.c_int),
        ('faultCount', ctypes.c_int),
        ('queryVectorRS', ctypes.POINTER(C_QueryVectorRS)),
        ('faultVectorRS', ctypes.POINTER(C_QueryVectorRS))
    ] 

class C_CountRS(ctypes.Structure):
    _fields_ = [
        ('errCode', ctypes.c_int),
        ('errMsg', ctypes.POINTER(ctypes.c_char_p)),
        ('count', ctypes.c_int)
    ]

class C_CollectionListRS(ctypes.Structure):
    _fields_ = [
        ('errCode', ctypes.c_int),
        ('errMsg', ctypes.POINTER(ctypes.c_char_p)),
        ('collections', ctypes.POINTER(ctypes.POINTER(ctypes.c_char_p)))
    ]

class C_VectorListRS(ctypes.Structure):
    _fields_ = [
        ('errCode', ctypes.c_int),
        ('errMsg', ctypes.POINTER(ctypes.c_char_p)),
        ('vectors', ctypes.POINTER(ctypes.POINTER(ctypes.c_char_p)))
    ]

class C_QueryOptions(ctypes.Structure):
    _fields_ = [
        ('vectorDistanceMethod', ctypes.c_int),
        ('queryLimit', ctypes.c_int),
        ('queryLogicalOP', ctypes.c_int),
        ('queryValue', ctypes.c_double),
        ('includeFault', ctypes.c_bool),
        ('pValue', ctypes.c_double),
        ('doNormal', ctypes.c_bool)
    ]
