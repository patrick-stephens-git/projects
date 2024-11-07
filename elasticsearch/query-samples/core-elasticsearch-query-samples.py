from elasticsearch6 import Elasticsearch # https://elasticsearch-py.readthedocs.io/en/v7.15.2/
import pandas as pd

# Don't collapse Pandas Dataframes:
pd.set_option('display.max_rows', None, 'display.max_columns', None)

query = "work from home"

################################################################################################
################################################################################################
################################################################################################
################################################################################################
## Match Query - Returns documents which in the field “X” contains the token “Y”, token “Z”, or both tokens
##
# query_body = {
#   "query" : {
#     "match" : {
#       "JobDescription" : {
#         "query" : "masters degree required"
#       }
#     }
#   }
# }

################
################
## Match Phrase Query - Returns documents only if this phrase will be found
##
# query_body = {
#   "query" : {
#     "match_phrase" : {
#       "JobDescription" : {
#         "query" : "masters degree required",
#          "slop" : "0"
#       }
#     }
#   }
# }

################
################
## Multi Match Query - Returns documents which in the fields “description” and/or "title" contains the tokens “work” and/or “from” and/or "home"
##
# query_body = {
#   "query" : {
#     "multi_match" : {
#         "query" : "work from home",
#        "fields" : ["JobDescription","NormalizedJobTitle"]
#     }
#   }
# }

################################################################################################
################################################################################################
################################################################################################
################################################################################################
## Term Query - Returns the documents where the value of a field exactly matches the criteria
##
# query_body = {
#     "query": {
#         "term" : {
#             "_id" : "771107783"
#         }
#     }
# }

################
################
## Terms Query - Documents returned do not have to match all the values in the "_id" field list
##
# query_body = {
#     "query": {
#         "terms" : {
#             "_id": ['771107783', '771110613']
#         }
#     }
# }

################
################
## Range Query - Returns documents in which queried field’s value is within the defined range
##
# query_body = {
#     "query": {
#         "range" : {
#             "CustomerId" : {
#                 "gte" : 37135352,
#                 "lte" : 37135353
#             }
#         }
#     }
# }

################
################
## Regexp Query - Returns documents in which queried field’s value is within the defined range
##
# query_body = {
#     "query": {
#         "regexp" : {
#             "CustomerNameCityState" : "Forest City.*"
#         }
#     }
# }

################
################
## Exists Query - Returns documents that contain an indexed value for a field
##
# query_body = {
#     "query": {
#         "exists": {
#             "field": "CustomerNameCityState"
#         }
#     }
# }

################################################################################################
################################################################################################
################################################################################################
################################################################################################
## Boolean Query (Compound Query) - Returns documents by wrapping together multiple queries, e.g: combine the score, change behavior of wrapped queries, switch query context to filter context, any of the above combined
##
query = 'minimum age 15 years old'
entity = 'age'
age_entity = '15'
compound_phrase = '15 years old'

query_body = {"query" : 
              {"bool" : 
               {"must" : 
                [{"bool" : 
                  {"must" : 
                   [{"match_phrase" : 
                     {"JobDescription" : 
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
                     {"JobDescription" : 
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

# call the client's search() method, and have it return results
es = Elasticsearch('https://ynxFvkbQ76:2vqhY4uMkRC3cUZrtjWKfya@search-prod-new-2128642592.us-east-1.bonsaisearch.net:443') ## Update this field if error contains: "Cluster not found"
results = es.search(index='postings-prod', doc_type='posting', body=query_body, size=2)
results

