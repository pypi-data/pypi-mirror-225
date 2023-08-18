import os
from victo.cproxy import CProxy

cProxy = CProxy()

def newCollection(db, collection):
    return cProxy.newCollection(os.path.join(db, collection))


def deleteCollection(db, collection):
    return cProxy.deleteCollection(os.path.join(db, collection))

    
def collectionCount(db):
    return cProxy.collectionCount(db)

    
def collectionList(db):
    return cProxy.collectionList(db)


def putVector(db, collection, ai_model, hash, vdim, vp, is_normal=False, overwrite=False):
    return cProxy.putVector(os.path.join(db, collection), ai_model, hash, vdim, vp, is_normal, overwrite)
    

def getVector(db, collection, hash):
    return cProxy.getVector(os.path.join(db, collection), hash)

def queryVector(db, collection, ai_model, vdim, vp, vector_distance_method=0, query_limit=-99, logical_op=0, k_value=0, p_value=0, do_normal=False, include_fault=False):
    return cProxy.queryVector(os.path.join(db, collection), ai_model, vdim, vp, vector_distance_method, query_limit, logical_op, k_value, p_value, do_normal, include_fault)


def deleteVector(db, collection, hash):
    return cProxy.deleteVector(os.path.join(db, collection), hash)

    
def vectorCount(db, collection):
    return cProxy.vectorCount(os.path.join(db, collection))

    
def vectorList(db, collection):
    return cProxy.vectorList(os.path.join(db, collection))


