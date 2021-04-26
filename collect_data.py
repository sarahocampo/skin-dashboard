# -*- coding: utf-8 -*-
"""
Created on Fri Apr 23 17:51:03 2021

@author: sehoc
"""

import pandas as pd                
import pytrends     
from pytrends.request import TrendReq
import wbgapi as wb


def econ_name_list(df, geoname_list):
    econ_name = []
    for name in geoname_list:
        try:
            econ_value = wb.economy.coder(df['geoName'])['{}'.format(str(name))][:3]
        except TypeError:
            econ_value = ""
        econ_name.append(econ_value) 
    return econ_name

def econ_df(econ_name_list):
    econ_df_list = []
    for name in econ_name_list:
        print(str(name))
        try:
            income_value = wb.economy.DataFrame(['{}'.format(str(name))])
        except wb.APIResponseError:
            income_value = ""
        except wb.APIError:
            income_value = ""
        econ_df_list.append(income_value)
    return econ_df_list

def econ_df_info(econ_df):    
    latitude = []
    longitude = []
    income_level = []
    region = []
    for i in range(0, len(econ_df)):
        try:
            econ_value_df = econ_df[i]
            longitude_value = econ_value_df['longitude'][0]
            latitude_value = econ_value_df['latitude'][0]
            income_level_value = econ_value_df['incomeLevel'][0]
            region_value = econ_value_df['region'][0]
            latitude.append(latitude_value)
            longitude.append(longitude_value)
            income_level.append(income_level_value)
            region.append(region_value)
        except IndexError:
            latitude.append("")
            longitude.append("")
            income_level.append("")
            region.append("")
        except TypeError:
            latitude.append("")
            longitude.append("")
            income_level.append("")
            region.append("")        
    return latitude, longitude, income_level, region


def related_topics_str_list(topic='eczema'):
    rising_list = []
    top_list = []
    both_list = []
    for i in range (0, len(pytrend.related_topics()[topic]['rising']['topic_type'])):
        rising_values = pytrend.related_topics()[topic]['rising']['topic_type'][i]
        rising_list.append(rising_values)
        both_list.append(rising_values)
    for i in range (0, len(pytrend.related_topics()[topic]['top']['topic_type'])):
        top_values = pytrend.related_topics()[topic]['top']['topic_type'][i]
        top_list.append(top_values)
        both_list.append(top_values)
    return both_list, top_list, rising_list



def unique_related_topics(both_list):
    unique_topic_list = []
    for i in range (0, len(both_list)):
       topic_value = both_list[i].lower()
       if topic_value not in unique_topic_list:
           topic_value = topic_value.split()
           unique_topic_list.append(topic_value[0].lower())
    return unique_topic_list
       

   
# def find_related_variables(db_num=16, unique_topic_list):
#     wb.db = db_num
#     db_var = wb.series.info()
#     db_var.columns
#     # related_var_titles = []
#     related_var_ids = []
#     for i in range (0, len(db_var.items)):
#         desc_split = db_var.items[i]['value'].split()
#         id_split = db_var.items[i]['id']
#         for val in desc_split:
#             if val.lower() in unique_topic_list:
#                 # related_var_titles.append(desc_split)
#                 related_var_ids.append(id_split)
#         # return related_var_titles, related_var_ids
#     return related_var_ids
     
# def find_all_related_variables(unique_topic_list:
#     all_related_var_id_list = []
#     db_num_list = []
#     for i in range(1, 83):
#         print(i)
#         related_var_ids = find_related_variables(db_num=i, unique_topic_list=unique_topic_list)
#         if len(related_var_ids) != 0:
#             try:
#                 all_related_var_id_list.append(related_var_ids)
#                 db_num_list.append(i)
#             except wb.APIResponseError:
#                 all_related_var_id_list.append("")
#                 db_num_list.append(i)
#     return all_related_var_id_list, db_num_list
