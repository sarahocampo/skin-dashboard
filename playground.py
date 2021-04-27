# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 12:49:59 2021

@author: sehoc
"""


import sys
sys.path.append(r'C:\Users\sehoc\OneDrive\Documents\GitHub\skin-dashboard')
import collect_data as cd
# from pytrends.request import TrendReq
# import wbgapi as wb
# https://pypi.org/project/pytrends/
# https://pypi.org/project/wbgapi/

# Make list of keywords of interest.
kw_list = ['covid']
pytrend, df = cd.pytrend_data(kw_list)
# df = df[df['frog']!=0].reset_index(drop=True)

# Make list of the economic abbreviation for each country.
econ_name = cd.econ_name_list(df)
df['econ_name'] = econ_name # Add to df.

# Create df with very basic economic information.
economic_df = cd.economic_information(econ_name)
new_df = df.join(economic_df) # Join the two dataframes together.

# Create list of related topics. 
both_list, top_list, rising_list=cd.related_topics_str_list(pytrend, kw_list)

# Format the results and get unique topics only. 
unique_topic_list = cd.unique_related_topics(both_list)

# Find related variable ids from a certain db.
related_var_ids, related_var_titles = cd.find_related_variables(db_num=12, unique_topic_list=unique_topic_list)

# Get data from world data.
world_data = cd.retrieve_data(related_var_ids, db_num=12, year='2020', econ_name=econ_name)

# Join world data and trend data.
joined_df = cd.order_and_join_data(df, world_data)

# Find all related variable id's and titles.
related_ids, related_titles, related_db_num = cd.find_all_related_variables(unique_topic_list=unique_topic_list)

# Make related variable df.
related_var_df = cd.create_related_var_df(related_ids, related_titles, related_db_num)

# Data from all related variables.
all_world_data = cd.data_all_vars(related_var_df, year='', econ_name=econ_name)

