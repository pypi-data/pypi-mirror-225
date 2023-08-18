import ctypes
from victo.c_ds import *

class Response:
    def __init__(self, obj):
        self.errCode = obj.errCode
        self.errMsg = ctypes.string_at(obj.errMsg).decode('utf-8')

class Node:
    def __init__(self, obj):
        self.ai_model = obj.node.ai_model if obj.errCode == 0 else None # ctypes.string_at(obj.node.ai_model).decode('utf-8') if obj.errCode == 0 else None
        self.hash = obj.node.hash if obj.errCode == 0 else None # ctypes.string_at(obj.node.hash).decode('utf-8') if obj.errCode == 0 else None
        self.normal = obj.node.normal if obj.errCode == 0 else None # ctypes.string_at(obj.node.normal).decode('utf-8') if obj.errCode == 0 else None
        self.vdim = obj.node.vdim if obj.errCode == 0 else 0
        self.vp = [obj.node.vp[i] for i in range(obj.node.vdim)] if obj.errCode == 0 else []

class PutVectorRS:
    def __init__(self, obj):
        self.errCode = obj.errCode
        self.errMsg = ctypes.string_at(obj.errMsg).decode('utf-8')
        self.hash = ctypes.string_at(obj.hash).decode('utf-8')

class GetVectorRS:
    def __init__(self, obj):
        self.errCode = obj.errCode
        self.errMsg = ctypes.string_at(obj.errMsg).decode('utf-8')
        self.node = Node(obj)

class QueryVectorRS:
    def __init__(self, obj):
        self.errCode = obj.errCode
        self.errMsg =  obj.errMsg # ctypes.string_at(obj.errMsg).decode('utf-8') if obj.errCode == 0 else None
        self.ai_model = obj.ai_model # ctypes.string_at(obj.ai_model).decode('utf-8') if obj.errCode == 0 else None
        self.normal = obj.normal  # ctypes.string_at(obj.normal).decode('utf-8') if obj.errCode == 0 else None
        self.hash = obj.hash  # ctypes.string_at(obj.hash).decode('utf-8') if obj.errCode == 0 else None
        self.vdim = obj.vdim 
        self.distance = obj.distance if obj.errCode == 0 else None

class QueryVectorRSWrapper:
    def __init__(self, obj):
        self.errCode = obj.errCode
        self.errMsg = ctypes.string_at(obj.errMsg).decode('utf-8')
        self.queryCount = obj.queryCount
        self.faultCount = obj.faultCount
        self.queryVectorRS = [QueryVectorRS(obj.queryVectorRS[i]) for i in range(obj.queryCount)] 
        self.faultVectorRS = [QueryVectorRS(obj.faultVectorRS[i]) for i in range(obj.faultCount)]

class CountRS:
    def __init__(self, obj):
        self.errCode = obj.errCode
        self.errMsg = ctypes.string_at(obj.errMsg).decode('utf-8')
        self.count = obj.count

class CollectionListRS:
    def __init__(self, obj):
        self.errCode = obj.errCode
        self.errMsg = ctypes.string_at(obj.errMsg).decode('utf-8')
        self.collections = []
        collections_pointer = obj.collections
        i = 0
        while collections_pointer[i]:
            self.collections.append(ctypes.string_at(collections_pointer[i]).decode('utf-8'))
            i += 1

class VectorListRS:
    def __init__(self, obj):
        self.errCode = obj.errCode
        self.errMsg = ctypes.string_at(obj.errMsg).decode('utf-8')
        self.vectors = []
        vectors_pointer = obj.vectors
        i = 0
        while vectors_pointer[i]:
            self.vectors.append(ctypes.string_at(vectors_pointer[i]).decode('utf-8'))
            i += 1

class QueryOptions(ctypes.Structure):
    def __init__(self, obj):
        self.vectorDistanceMethod = obj.vectorDistanceMethod
        self.queryLimit = obj.queryLimit
        self.queryLogicalOP = obj.queryLogicalOP
        self.queryValue = obj.queryValue
        self.includeFault = obj.includeFault
        self.pValue = obj.pValue
        self.doNormal = obj.doNormal


