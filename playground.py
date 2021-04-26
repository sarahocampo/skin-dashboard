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

# Make list of keywords of interest.
kw_list = ['eczema']
pytrend, df = cd.pytrend_data(kw_list)

# Make list of the economic abbreviation for each country.
econ_name = cd.econ_name_list(df)
df['econ_name'] = econ_name # Add to df.

# Create df with very basic economic information.
economic_df = cd.economic_information(econ_name)
new_df = df.join(economic_df) # Join the two dataframes together.

# Create list of related topics. 
both_list, top_list, rising_list=cd.related_topics_str_list(pytrend, topic='eczema')

# Format the results and get unique topics only. 
unique_topic_list = cd.unique_related_topics(both_list)

# Find related variable ids from a certain db.
test_list = ['fertility', 'expectancy']
related_var_ids, related_var_titles = cd.find_related_variables(db_num=16, unique_topic_list=test_list)

# Get data from world data.
world_data = cd.retrieve_data(related_var_ids, 16, year='2014', econ_name=econ_name)

# Join world data and trend data.
joined_df = cd.order_and_join_data(df, world_data)



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



