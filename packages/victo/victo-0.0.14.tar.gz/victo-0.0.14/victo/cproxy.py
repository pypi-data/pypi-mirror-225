from victo.py_ds import *
from victo.c_ds import *
import ctypes
import os
import platform



class CProxy:    
    def __init__(self):
        system = platform.system()
    
        if system == 'Darwin':
            libName = 'libvicto.dylib'
            sysName = 'macos'
        else:
            raise RuntimeError("Unsupported Platform")

        libPath = os.path.join(os.path.dirname(__file__),'lib', sysName, libName);
        self.c_lib = ctypes.cdll.LoadLibrary(libPath)


    def newCollection(self, location):
        newCollectionFunc = self.c_lib.newCollectionSL
        newCollectionFunc.restype = C_Response
        newCollectionFunc.argtypes = [ctypes.c_char_p]
        rs = newCollectionFunc(location.encode('utf-8'))
        return Response(rs)

    def deleteCollection(self, location):
        deleteCollectionFunc = self.c_lib.deleteCollectionSL
        deleteCollectionFunc.restype = C_Response
        deleteCollectionFunc.argtypes = [ctypes.c_char_p]
        rs = deleteCollectionFunc(location.encode('utf-8'))
        return Response(rs)
    
    def collectionCount(self, location):
        collectionCountFunc = self.c_lib.collectionCountSL
        collectionCountFunc.restype = C_CountRS
        collectionCountFunc.argtypes = [ctypes.c_char_p]
        rs = collectionCountFunc(location.encode('utf-8'))
        return CountRS(rs)
    
    def collectionList(self, location):
        collectionListFunc = self.c_lib.collectionListSL
        collectionListFunc.restype = C_CollectionListRS
        collectionListFunc.argtypes = [ctypes.c_char_p]
        rs = collectionListFunc(location.encode('utf-8'))
        return CollectionListRS(rs)

    def putVector(self, location, ai_model, hash, vdim, vp, is_normal, overwrite):
        c_vp = (ctypes.c_double * vdim) (*vp)
        putVectorFunc = self.c_lib.putVectorSL       
        putVectorFunc.restype = C_PutVectorRS
        putVectorFunc.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.c_bool, ctypes.c_bool]
        rs = putVectorFunc(location.encode('utf-8'), ai_model.encode('utf-8'), hash.encode('utf-8'), vdim,c_vp,is_normal, overwrite);
        return PutVectorRS(rs)       

    def getVector(self, location, hash):
        getVectorFunc = self.c_lib.getVectorSL
        getVectorFunc.restype = C_GetVectorRS
        getVectorFunc.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
        rs = getVectorFunc(location.encode('utf-8'), hash.encode('utf-8'))
        return GetVectorRS(rs)

    def queryVector(self, location, ai_model, vdim, vp, vector_distance_method, query_limit, logical_op, query_value, p_value, do_normal, include_fault):
        c_vp = (ctypes.c_double * vdim) (*vp)
        queryOptions = C_QueryOptions()
        queryOptions.vectorDistanceMethod = vector_distance_method
        queryOptions.queryLimit = query_limit
        queryOptions.queryLogicalOP = logical_op
        queryOptions.queryValue = query_value
        queryOptions.includeFault = include_fault
        queryOptions.pValue = p_value
        queryOptions.doNormal = do_normal

        queryVectorFunc = self.c_lib.queryVectorSL
        queryVectorFunc.restype = C_QueryVectorRSWrapper
        queryVectorFunc.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int, ctypes.POINTER(ctypes.c_double), C_QueryOptions]
        rs = queryVectorFunc(location.encode('utf-8'), ai_model.encode('utf-8'), vdim, c_vp, queryOptions)
        return QueryVectorRSWrapper(rs)

    def deleteVector(self, location, hash):
        deleteVectorFunc = self.c_lib.deleteVectorSL
        deleteVectorFunc.restype = C_Response
        deleteVectorFunc.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
        rs = deleteVectorFunc(location.encode('utf-8'), hash.encode('utf-8'))
        return Response(rs)
    
    def vectorCount(self, location):
        vectorCountFunc = self.c_lib.vectorCountSL
        vectorCountFunc.restype = C_CountRS
        vectorCountFunc.argtypes = [ctypes.c_char_p]
        rs = vectorCountFunc(location.encode('utf-8'))
        return CountRS(rs)
    
    def vectorList(self, location):
        vectorListFunc = self.c_lib.vectorListSL
        vectorListFunc.restype = C_VectorListRS
        vectorListFunc.argtypes = [ctypes.c_char_p]
        rs = vectorListFunc(location.encode('utf-8'))
        return VectorListRS(rs)

