from elasticsearch6 import Elasticsearch # https://elasticsearch-py.readthedocs.io/en/v7.15.2/
import pandas as pd

# Don't collapse Pandas Dataframes:
pd.set_option('display.max_rows', None, 'display.max_columns', None)

query = 'minimum age 18 years old'
compound_phrases = ['minimum age','18 years old']
entity_category = 'age'
entity_value = '18'

################################################################################################
################################################################################################
################################################################################################
################################################################################################
## Match Query - Returns documents which in the field “X” contains the token “Y”, token “Z”, or both tokens
##
query_body = {
  "query" : {
    "match" : {
      "description" : {
        "query" : "{0}".format(query)
      }
    }
  }
}

################
################
## Match Phrase Query - Returns documents only if this phrase will be found
##
query_body = {
  "query" : {
    "match_phrase" : {
      "Description" : {
        "query" : "{0}".format(query),
         "slop" : "0"
      }
    }
  }
}

################
################
## Multi Match Query - Returns documents which in the fields “description” and/or "title" contains the tokens “work” and/or “from” and/or "home"
##
query_body = {
  "query" : {
    "multi_match" : {
        "query" : "{0}".format(query),
       "fields" : ["description","title"]
    }
  }
}

################################################################################################
################################################################################################
################################################################################################
################################################################################################
## Term Query - Returns the documents where the value of a field exactly matches the criteria
##
query_body = {
    "query": {
        "term" : {
            "_id" : "771107783"
        }
    }
}

################
################
## Terms Query - Documents returned do not have to match all the values in the "_id" field list
##
query_body = {
    "query": {
        "terms" : {
            "_id": ['7711083', '7710613']
        }
    }
}

################
################
## Range Query - Returns documents in which queried field’s value is within the defined range
##
query_body = {
    "query": {
        "range" : {
            "id" : {
                "gte" : 12135352,
                "lte" : 12135353
            }
        }
    }
}

################
################
## Regexp Query - Returns documents in which queried field’s value is within the defined range
##
query_body = {
    "query": {
        "regexp" : {
            "city" : "Austin.*"
        }
    }
}

################
################
## Exists Query - Returns documents that contain an indexed value for a field
##
query_body = {
    "query": {
        "exists": {
            "field": "city"
        }
    }
}

################################################################################################
################################################################################################
################################################################################################
################################################################################################
## Boolean Query (Compound Query) - Returns documents by wrapping together multiple queries, e.g: combine the score, change behavior of wrapped queries, switch query context to filter context, any of the above combined
##
query_body = {"query" : 
              {"bool" : 
               {"must" : 
                [{"bool" : 
                  {"must" : 
                   [{"match_phrase" : 
                     {"Description" : 
                      {"query" : "{0}".format(compound_phrase),
                        "slop" : "0"
                      }
                     }
                    }]
                  }
                 },
                 {"bool" : 
                  {"should" : 
                   [{"match" : 
                     {"Description" : 
                      {"query" : "{0}".format(query)
                      }
                     }
                    }]
                  }
                 }]
               }
              }
             }

print(query_body)

cluster = 'xxx'
index = 'xxx'
doc_type = 'xxx'
# call the client's search() method, and have it return results
es = Elasticsearch(cluster) ## Update this field if error contains: "Cluster not found"
results = es.search(index=index, doc_type=, body=query_body, size=10)
# results

description_text_list = []
for hit in results['hits']['hits']:
    text = hit['_source']['Description']
    job_description_text_list.append(text)
    
print(description_text_list)

