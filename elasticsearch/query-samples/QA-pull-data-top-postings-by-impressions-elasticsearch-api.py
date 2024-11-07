from datascience.common.io.snowflake import get_snowflake_engine_okta # https://docs.snowflake.com/en/user-guide/python-connector-api.html
from elasticsearch6 import Elasticsearch # https://elasticsearch-py.readthedocs.io/en/v7.15.2/
import pandas as pd
import time
import csv
import re

# Don't collapse Pandas Dataframes:
pd.set_option('display.max_rows', None, 'display.max_columns', None)

def pull_data(sql_query, engine):
    for attempt in range(5):
        try:
            sql_query = re.sub('\s+', ' ', sql_query)
#             print sql_query ## Use for troubleshooting to view the SQL query
            return pd.read_sql(sql_query, engine)
        except Exception as e:
            print(str(e) + '\nAttempt {0} out of 3'.format(attempt + 1))
            if attempt == 2: ## Attempt is '2' because it starts at '0'
                log_errors(e) ## Logs error on final attempt
                time.sleep(2)
            else:
                time.sleep(2)
            
def log_errors(error):
    with open('error-log.csv','ab') as export_file:
        writer = csv.writer(export_file)
        writer.writerow([error])
            
def export_csv(df):
    with open('sql-results.csv','ab') as export_file:
        df.to_csv('sql-results.csv', mode='a', encoding='utf-8', index=False, header=False)

with open('sql-results.csv','ab') as export_file:
    writer = csv.writer(export_file)
    # writer.writerow(['col1','col2','col3']) # Create header row

engine = get_snowflake_engine_okta('patrick.stephens@snagajob.com')

date_range = 7

sql_query = """
SELECT worker_funnel."POSTING_ID"  AS "worker_funnel.posting_id",
       COALESCE(SUM((worker_funnel."IS_IMPRESSION")::int ), 0) AS "worker_funnel.total_impressions"

FROM PROD_DB.ACTIVITY.FACT_WORKER_FUNNEL  AS worker_funnel

WHERE TO_DATE(TO_CHAR(worker_funnel."DATE_KEY"), 'YYYYMMDD') >= DATE_TRUNC('week', CURRENT_DATE())
  AND TO_DATE(TO_CHAR(worker_funnel."DATE_KEY"), 'YYYYMMDD') < DATEADD('day', {0}, DATE_TRUNC('week', CURRENT_DATE()))
  AND worker_funnel."IS_IMPRESSION" = 'true'

GROUP BY 1

ORDER BY 2 DESC

LIMIT 5
""".format(date_range)

print(sql_query)

data_df = pd.DataFrame()
print('Running SQL query...')
data = pd.read_sql(sql_query, engine)
data_df = data_df.append(data)

data_df.head()

# Get a list of Posting IDs:
posting_id_list = data_df['worker_funnel.posting_id'].values.tolist()
print(str(posting_id_list))

## Find multiple postings:
##
query_body = {
    "query": {
        "terms": {
            "_id": ['685870368', '548015699', '613525625', '689194069', '701788767', '685856196', '548028706', '625294541', '688273009', '680100347', '684994184', '697080551', '651623423', '704205043', '622594226', '703998003', '641000792', '691778441', '658264583', '512729210', '691778453', '701740887', '701740291', '703892868', '568896197', '687372006', '642588870', '695954818', '503657741', '642588811', '621098559', '702307150', '676797739', '648960916', '703892949', '615514094', '654184741', '702237661', '642590929', '642590999', '701740190', '642589302', '681258394', '701121560', '696316666', '606395495', '687847719', '699861195', '657551218', '642588254', '681289800', '688452419', '687648019', '701633949', '649096052', '687845447', '556223732', '677555679', '659347688', '702351377', '685823683', '648672098', '671039958', '648673447', '608112038', '688108480', '21138586', '637553916', '702023838', '667341252', '579393506', '695886001', '21138582', '667342581', '702433976', '695886220', '659387762', '648341569', '688481466', '648672796', '697480159', '702897105', '681289817', '688104794', '702855811', '688363784', '694252098', '696565227', '700762583', '648341344', '701455261', '587982450', '659565609', '659565842', '704146901', '704146919', '704147351', '659565500', '687855542', '659565469']
        }
    }
}


# query_body = """
# {
#     "query": {
#         "terms": {
#             "_id": {0}
#         }
#     }
# }
# """.format(str(posting_id_list))

# or write your own query and search:
# query_body = {
#     "query": {
#         "terms": {
#             "_id": ['680462696','680462697']
#         }
#     }
# }

# call the client's search() method, and have it return results
es = Elasticsearch('https://QCfFXJvWwi:L53KRp2EFoUHkhQB7@search-prod-6337689579.us-east-1.bonsaisearch.net:443')
results = es.search(index='postings-prod', doc_type='posting', body=query_body, size=1000)
results

