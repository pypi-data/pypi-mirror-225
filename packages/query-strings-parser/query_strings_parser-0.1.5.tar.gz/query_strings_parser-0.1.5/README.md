# Query Strings Parser Description

A library created in the context of P2W to parse and transform FastAPI query strings into a format recognized by SQL databases.


**Main Features:**

- Parsing and transforming FastAPI query strings into a format recognized by SQL databases.

---

## Installation and Execution

### 1. Install Python dependencies

```
$ pip3 install virtualenv
$ virtualenv -p python3 venv
$ . venv/bin/activate
$ pip3 install query_strings_parser
```

## Module Usage

### 1. Module Import

```
from query_strings_parser import QueryParser
```

### 2. Parsing Query Strings

The lib exposes the `build_query()` static method which can be used as follows:

```
# Request example: https://localhost:4001/v1/predictions/?fields=attr_1&sort=-attr_1&page=1&limit=20&attr_1=lorem_ipsum

@router.get("/")
def get_all(request: Request):
    query_params_dict = QueryParser.build_query(request.query_params.multi_items())
```

The method parameter must be a list of tuples that can be obtained from **FastAPI** as exemplified above:

```
[
   ("fields", "attr_1"),
   ("sort", "-attr_1"),
   ("page", "1"),
   ("limit", "20"),
   ("attr_1", "lorem_ipsum")
]
```

The return of this method is a dictionary:

```
{
   "fields":[
      "attr_1"
   ],
   "sort":{
      "attr_1":"DESC"
   },
   "pagination":{
      "page":"1",
      "limit":"20"
   },
   "filters":{
      "attr_1":"lorem_ipsum"
   }
}
```

### 3. Supported Query Strings

#### 3.1. Fields

Multiple values must be comma separated and **fields** can appear **n** times in the query.

```
https://localhost:4001/v1/predictions/?fields=attr_1,attr_2

# Result:
#    "fields":[
#       "attr_1",
#       "attr_2"
#    ]

https://localhost:4001/v1/predictions/?fields=attr_1&...&fields=attr_2

# Result:
#    "fields":[
#       "attr_1",
#       "attr_2"
#    ]
```

#### 3.2. Ordination

To sort in descending order, the value must be preceded by a "-". By default, the order is ascending. **sort** can appear **n** times in the query.

```
https://localhost:4001/v1/predictions/?sort=-attr_1

# Result:
#    "sort":{
#       "attr_1":"DESC"
#    }

https://localhost:4001/v1/predictions/?sort=-attr_1&...&sort=attr_2

# Result:
#    "sort":{
#       "attr_1":"DESC",
#       "attr_2":"ASC"
#    }
```

#### 3.3. Pagination

If multiple **page** and **limit** parameters are sent, only the values of the last ones will be considered.

```
https://localhost:4001/v1/predictions/?page=1&limit=20

# Result:
#    "pagination":{
#       "page":"1",
#       "limit":"20"
#    }
```

#### 3.4. Filters

Any parameter other than **fields**, **sort**, **page** and **limit** will be considered a **filter**.

The lib supports OR filters through the comma character.

```
https://localhost:4001/v1/predictions/?attr_1=lorem_ipsum

# Result:
#    "filters":{
#       "attr_1":"lorem_ipsum"
#    }

https://localhost:4001/v1/predictions/?attr_1=lorem_ipsum&...&attr_2=lorem_ipsum_2,lorem_ipsum_3

# Result:
#    "filters":{
#       "attr_1":"lorem_ipsum",
#       "attr_2":{
#          "$or":[
#             "lorem_ipsum_2",
#             "lorem_ipsum_3"
#          ]
#       }
#    }
```

In addition to OR, the lib supports AND filters through the semicolon character.

```
https://localhost:4001/v1/predictions/?attr_1=lorem_ipsum

# Result:
#    "filters":{
#       "attr_1":"lorem_ipsum"
#    }

https://localhost:4001/v1/predictions/?attr_1=lorem_ipsum&...&attr_2=lorem_ipsum_2;lorem_ipsum_3

# Result:
#    "filters":{
#       "attr_1":"lorem_ipsum",
#       "attr_2":{
#          "$and":[
#             "lorem_ipsum_2",
#             "lorem_ipsum_3"
#          ]
#       }
#    }
```

It also supports filtering with search through asterisks as follows:

- Search where `attr` starts with **"value"**.

```
https://localhost:4001/v1/predictions/?attr=value*

# Result:
#    "filters":{
#       "attr":{
#          "$regex":"^v[a,á,à,ä,â,ã]l[u,ú,ù,ü][e,é,ë,ê]"
#       }
#    }
```

- Search where `attr` ends with **"value"**.

```
https://localhost:4001/v1/predictions/?attr=*value

# Result:
#    "filters":{
#       "attr":{
#          "$regex":"v[a,á,à,ä,â,ã]l[u,ú,ù,ü][e,é,ë,ê]$"
#       }
#    }
```

- Search where `attr` has the substring **"value"**.

```
https://localhost:4001/v1/predictions/?attr=*value*

# Result:
#    "filters":{
#       "attr":{
#          "$regex":"v[a,á,à,ä,â,ã]l[u,ú,ù,ü][e,é,ë,ê]"
#       }
#    }
```

Another available feature is filtering with comparison operators as follows:

- Search where `attr` is greater than or equal to **"2023-06-15T14:20:10.555323Z"**.

```
https://localhost:4001/v1/predictions/?attr=gte:2023-06-15T14:20:10.555323Z

# Result:
#    "filters":{
#       "attr":{
#          "$gte":"2023-06-15T14:19:08.555323Z"
#       }
#    }
```

- Search where `attr` is greater than **"2023-06-15T14:20:10.555323Z"**.

```
https://localhost:4001/v1/predictions/?attr=gt:2023-06-15T14:20:10.555323Z

# Result:
#    "filters":{
#       "attr":{
#          "$gt":"2023-06-15T14:19:08.555323Z"
#       }
#    }
```

- Search where `attr` is less than or equal to **"2023-06-15T14:20:10.555323Z"**.

```
https://localhost:4001/v1/predictions/?attr=lte:2023-06-15T14:20:10.555323Z

# Result:
#    "filters":{
#       "attr":{
#          "$lte":"2023-06-15T14:19:08.555323Z"
#       }
#    }
```

- Search where `attr` is less than **"2023-06-15T14:20:10.555323Z"**.

```
https://localhost:4001/v1/predictions/?attr=lt:2023-06-15T14:20:10.555323Z

# Result:
#    "filters":{
#       "attr":{
#          "$lt":"2023-06-15T14:19:08.555323Z"
#       }
#    }
```

- Search where `attr` is different from **"2023-06-15T14:20:10.555323Z"**.

```
https://localhost:4001/v1/predictions/?attr=ne:2023-06-15T14:20:10.555323Z

# Result:
#    "filters":{
#       "attr":{
#          "$ne":"2023-06-15T14:19:08.555323Z"
#       }
#    }
```