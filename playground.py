# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 12:49:59 2021

@author: sehoc
"""


import sys
sys.path.append(r'C:\Users\sehoc\OneDrive\Documents\GitHub\skin-dashboard')
import collect_data as cd
from pytrends.request import TrendReq
import wbgapi as wb
# https://pypi.org/project/pytrends/
# https://pypi.org/project/wbgapi/


pytrend = TrendReq()
pytrend.build_payload(kw_list=["eczema"])
df = pytrend.interest_by_region().reset_index()
df = df[df['eczema']!=0].reset_index(drop=True)


geoname_list = df['geoName'].tolist()
econ_name = cd.econ_name_list(df, geoname_list)
df['econ_name'] = econ_name


econ_df = cd.econ_df(econ_name)
econ_df_list = []
for name in econ_name:
    print(str(name))
    income_value = wb.economy.DataFrame(['{}'.format(str(name))])
    econ_df_list.append(income_value)

latitude, longitude, income_level, region = cd.econ_df_info(econ_df)
df['income_level'] = income_level
df['latitude'] = latitude
df['longitude'] = longitude
df['region'] = region



# wb.source.info()
# wb.series.info(db=16)
# wb.time.info(db=16)
# wb.series.info('NY.GDP.PCAP.CD')
# wb.data.DataFrame('SP.POP.TOTL', time=2015, labels=True).reset_index()

# wb.db = 66

# new_test = wb.data.DataFrame('LP.LPI.INFR.XQ', time=2018, labels=True)
# new_test

# both_list, top_list, rising_list = related_topics_str_list(topic='eczema')

# unique_topic_list = unique_related_topics(both_list)

       
# related_var_ids = find_related_variables(db_num=39, unique_topic_list=unique_topic_list)



# all_related_var_id_list, db_num_list = find_all_related_variables(unique_topic_list = unique_topic_list)



# wb.db = 83
# db_var = wb.series.info()
# db_var.columns
# related_var_titles = []
# related_var_ids = []
# for i in range (0, len(db_var.items)):
#     desc_split = db_var.items[i]['value'].split()
#     id_split = db_var.items[i]['id']
#     if desc_split in unique_topic_list:
#         try:
#             related_var_titles.append(desc_split)
#             related_var_ids.append(id_split)
#         except wb.APIResponseError:
#             related_var_titles.append("")
#             related_var_ids

# x = wb.search('Drug')
# wb.source.info()
# unique_topic_list.split()

# rq_df = pd.DataFrame.from_dict(pytrend.related_queries()['eczema']['rising'])
# rq = pytrend.related_queries()
# rq_df = rq['eczema']['rising']['query']

# rq_df = pd.DataFrame()
# rq_df['eczema'] = rq['eczema']['rising']['query']
# rq_df['eczema_value'] = rq['eczema']['rising']['value']



