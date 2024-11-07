from elasticsearch6 import Elasticsearch # https://elasticsearch-py.readthedocs.io/en/v7.15.2/
import pandas as pd
import time
import csv
import re

# Don't collapse Pandas Dataframes:
pd.set_option('display.max_rows', None, 'display.max_columns', None)

## View Data Stored in Elastic
##
es = Elasticsearch('https://ynxFvkbQ76:2vqhY4uMkRC3cUZrtjWKfya@search-prod-new-2128642592.us-east-1.bonsaisearch.net:443')

posting_id = '771107783'
query = 'cashier'

# Elastic Fields:
posting_id_result = es.get(index='postings-prod', doc_type='posting', id=posting_id)

posting_id_result

# !!! IMPORTANT NOTE !!!
# Using explain this way isn't going to be using our query/template fyi
# so the scores will be completely different than our es scores.
# https://snagajob.slack.com/archives/C02AJKWC509/p1652707799373349?thread_ts=1652707493.717199&cid=C02AJKWC509

# Elastic Score Explainer:
posting_id_result_explain = es.explain(index='postings-prod', doc_type='posting', id=posting_id, q=query)

posting_id_result_explain
