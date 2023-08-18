# Victo

Victo is a AI Native, Lightweight, Plugable, Portable, Scalable Vector Database.

## Introduction

Vector embeddings are the integral part of AI applications. There is a need for a database to store and effeciently retrive vectors. For which, Victo is a best choice.

The highlevel architecture of Victo is,

```
Database -> contains Collections -> contains Vectors
```

The DB operations supported by Victo are:
- Add a Collection
- Delete a Collection
- Get the count of collections
- List the collections in a database
- Add a Vector Record
- Delete a Vector Record
- Retrive a Vector Record
- Query Vector
- Get the count of vectors in a collection
- Get the list of vectors in a collection

The Query vector works based on the vector distance calculation. Supported methods:
- Euclidean Distance
- Cosine Similarity
- Manhattan Distance
- Minkowski Distance Method

Some of the usecases for Victo are:
- NLP
- Generative AI
- Recommender System
- Image Search
- eCommerce
- Machine Learning
- Social Networks

## Built With
- Python 3.6
- C


## Getting Started

### Pip Install

```
pip install victo
```

### Facade

Facade is the interface to execute DB operations on Victo

```
from victo import facade as fd
```

### Add a new Collection
```
fd.newCollection(db, collection)

Arguments:
    db          : string    : Eg: /path/tp/victodb/data
    collection  : string    : Eg: reports
Returns:
    returns a result set object (rs)
    rs.errCode  : int       
    rs.errMsg   : string
```
### Delete a Collection
```
fd.deleteCollection(db, collection)

Arguments:
    db          : string    : Eg: /path/tp/victodb/data
    collection  : string    : Eg: reports
Returns:
    returns a result set object (rs)
    rs.errCode  : int       
    rs.errMsg   : string
```

### Get the count of Collections in a DB
```
fd.collectionCount(db)

Arguments:
    db          : string    : Eg: /path/tp/victodb/data
Returns:
    returns a result set object (rs)
    rs.errCode  : int       
    rs.errMsg   : string
    rs.count    : int
```

### Get the list of Collections in a DB
```
fd.collectionList(db)

Arguments:
    db          : string    : Eg: /path/tp/victodb/data    
Returns:
    returns a result set object (rs)
    rs.errCode      : int       
    rs.errMsg       : string
    rs.collections  : Array of string
```

### Add a vector records to a Collection
```
fd.putVector(db, collection, ai_model, hash, vdim, vp, is_normal, overwrite)

Arguments:
    db          : string            : Eg: /path/tp/victodb/data
    collection  : string            : Eg: reports
    ai_model    : string            : Eg: any_ai_model_used_for_vector_embedding (Max. 64 chars)
    hash        : string            : Eg: vector_id (Max. 64 chars)
    vdim        : int               : 768 (size of vector dimension - Max. 2048)
    vp          : Array of float    : Vector Embeddings
    is_normal   : bool              : True or False (normalize before save)
    overwrite   : bool              : True or False (overwrite if vector already exist) 
Returns:
    returns a result set object (rs)
    rs.errCode  : int       
    rs.errMsg   : string
    rs.hash     : string    : Eg: vector_id
```

### Query a single vector recors from a Collection
```
fd.getVector(db, collection, hash)

Arguments:
    db          : string            : Eg: /path/tp/victodb/data
    collection  : string            : Eg: reports
    hash        : string            : Eg: vector_id (Max. 64 chars)
Returns:
    returns a result set object (rs)
    rs.errCode  : int       
    rs.errMsg   : string
    rs.node     : vector node
        node.ai_model   :   string
        node.hash       :   string
        node.normal     :   int     : 0 - normalized, 1 - not normalized
        node.vdim       :   int
        node.vp         :   array of float
```

### Query vector records based on a condition from a Collection
```
fd.queryVector(db, collection, ai_model, vdim, vp, vector_distance_method, query_limit, logical_op, k_value, p_value, do_normal, include_fault)

Arguments:
    db                      : string            : Eg: /path/tp/victodb/data
    collection              : string            : Eg: reports
    ai_model                : string            : Eg: any_ai_model_used_for_vector_embedding (Max. 64 chars)
    vdim                    : int               : 768 (size of vector dimension - Max. 2048) (input vector)
    vp                      : Array of float    : Vector Embeddings (input_vector)
    vector_distance_method  : int               : 0 - Euclidean, 1 - CosineSimilarity, 2 - Manhattan, 3 - Minkowski (Default: 0)
    query_limit             : int
    logical_op              : int               : 0 - equal, 1 - greater than, 2 - greater than or equal, -1 - less than, -2 - less than or equal (Default: 0)
    k_value                 : float             : value used for comparison while query (Default: 0)
    p_value                 : float             : (Default: 0)
    do_normal               : bool              : Do normalize before search (Default: False)
    include_fault           : bool              : (Default: False)
Returns:
    returns a result set object (rs)
    rs.errCode          : int       
    rs.errMsg           : string
    rs.queryCount       : int
    rs.faultCount       : int
    rs.queryVectorRS    : Array of vector result
        queryVectorRS.errCode   : int
        queryVectorRS.errMsg    : string
        queryVectorRS.ai_model  : string
        queryVectorRS.normal    : int
        queryVectorRS.hash      : string
        queryVectorRS.vdim      : int
        queryVectorRS.distance  : double      
    rs.faultVectorRS    : Array of vector result
        faultVectorRS.errCode   : int
        faultVectorRS.errMsg    : string
        faultVectorRS.ai_model  : string
        faultVectorRS.normal    : int
        faultVectorRS.hash      : string
        faultVectorRS.vdim      : int
        faultVectorRS.distance  : double  
```

### Delete a vector record in a Collection
```
fd.deleteVector(db, collection, hash)

Arguments:
    db          : string    : Eg: /path/tp/victodb/data
    collection  : string    : Eg: reports 
    hash        : string    : Eg: vector_id   
Returns:
    returns a result set object (rs)
    rs.errCode  : int       
    rs.errMsg   : string
```   

### Get the count of vector records in a Collection
```
fd.vectorCount(db, collection)

Arguments:
    db          : string    : Eg: /path/tp/victodb/data
    collection  : string    : Eg: reports    
Returns:
    returns a result set object (rs)
    rs.errCode  : int       
    rs.errMsg   : string
    rs.count    : int
```

### Get the list of vector records in a Collection
```
fd.vectorList(db, collection)

Arguments:
    db          : string    : Eg: /path/tp/victodb/data    
    collection  : string    : Eg: reports  
Returns:
    returns a result set object (rs)
    rs.errCode  : int       
    rs.errMsg   : string
    rs.vectors  : Array of string
```

## Usage

The sample project listed [here](https://github.com/m-sparrow/victo-py-cmd-cli) is a command line utility makes use of [Cohere](https://cohere.com/) for vector embedings and victo for storing and processing vector embeddings. 

## Roadmap

- The project right now is supported is only in MacOS. Work is in progress to be supported in Linux and Windows
- Add support for additional Vector distance calculation methods such as: Jaccard Similarity and Hamming Distance

## Contributing

Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Adding AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Authors

Sree Hari - hari.tinyblitz@gmail.com

## Version History

Latest: v0.0.12

