# -*- coding: utf-8 -*-
"""
Created on Fri Apr 23 17:51:03 2021

@author: sehoc
"""
                
import wbgapi as wb
import pandas as pd
from pytrends.request import TrendReq

def pytrend_data(kw_list):
    pytrend = TrendReq()
    pytrend.build_payload(kw_list=kw_list)
    df = pytrend.interest_by_region().reset_index()
    df = df[df['eczema']!=0].reset_index(drop=True)
    return pytrend, df

def econ_name_list(df):
    geoname_list = df['geoName'].tolist()
    econ_name = []
    for name in geoname_list:
        try:
            econ_value = wb.economy.coder(df['geoName'])['{}'.format(str(name))][:3]
        except TypeError:
            econ_value = ""
        econ_name.append(econ_value) 
    return econ_name

    
def economic_information(econ_name):
    x = wb.economy.DataFrame(db=1)
    longitude_list = []
    latitude_list = []
    income_list = []
    region_list = []
    for i in range(0, len(econ_name)):
        lon = x['longitude'].loc[econ_name[i]]
        lat = x['latitude'].loc[econ_name[i]]
        inc = x['incomeLevel'].loc[econ_name[i]]
        reg = x['region'].loc[econ_name[i]]
        longitude_list.append(lon)
        latitude_list.append(lat)
        income_list.append(inc)
        region_list.append(reg)
    economic_df = pd.DataFrame()
    economic_df['longitude'] = longitude_list
    economic_df['latitude'] = latitude_list
    economic_df['income_level'] = income_list
    economic_df['region'] = region_list
    return economic_df


def related_topics_str_list(pytrend, topic='eczema'):
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
       

def find_related_variables(db_num=16, unique_topic_list=[]):
    wb.db = db_num
    db_var = wb.series.info()
    related_var_titles = []
    related_var_ids = []
    for i in range (0, len(db_var.items)):
        desc_split = db_var.items[i]['value'].split()
        id_split = db_var.items[i]['id']
        for val in desc_split:
            if val.lower() in unique_topic_list:
                related_var_titles.append(db_var.items[i]['value'])
                related_var_ids.append(id_split)
    return related_var_ids, related_var_titles

     
def find_time_range(db_num):
    time = wb.time.info(db=db_num)
    time_list = []
    for i in range(0, len(time.items)):
        time_value = time.items[i]['value']
        time_list.append(time_value)
    return time_list


def retrieve_data(related_var_ids, db_num, year='', econ_name=[]):
    if year == '':
        time_list = find_time_range(db_num)
        year = max(time_list)
        time_range = int(year)
    else:
        time_range = int(year)
    all_data = wb.data.DataFrame(related_var_ids, time=time_range, labels=True).reset_index()
    subset_boolean = all_data['economy'].isin(econ_name)
    all_data['boolean'] = subset_boolean
    world_data = all_data[all_data['boolean']==True].reset_index().drop(columns=['boolean', 'index'])
    return world_data

def order_and_join_data(df, world_data):
    sorted_df = df.sort_values(by='econ_name').reset_index().drop(columns='index')
    sorted_world_data = world_data.sort_values(by='economy').reset_index().drop(columns='index')
    joined_df = sorted_df.set_index('econ_name').join(sorted_world_data.set_index('economy'))
    joined_df = joined_df.reset_index().drop(columns=['geoName'])
    return joined_df

def create_db_num_list():
    source_info = wb.source.info()
    db_num_list = []
    for i in range (0, len(source_info.items)):
        db_num_values = source_info.items[i]['id']
        db_num_list.append(db_num_values)
    db_num_list = [int(i) for i in db_num_list]
    db_num_list.remove(2)
    db_num_list.remove(72)
    return db_num_list

def find_all_related_variables(unique_topic_list=[]):
    db_num_list = create_db_num_list()
    related_ids = []
    related_titles = []
    related_db_num = []
    for x in range(0, len(db_num_list)):
        db_num = str(db_num_list[x])
        related_var_ids, related_var_titles = find_related_variables(db_num=db_num, unique_topic_list=unique_topic_list)
        related_ids.append(related_var_ids)
        related_titles.append(related_var_titles)
        for i in range(0, len(related_var_ids)):
            related_db_num.append(db_num)  
    related_db_num = [int(i) for i in related_db_num]
    return related_ids, related_titles, related_db_num

def create_related_var_df(related_ids, related_titles, related_db_num): 
    all_rel_ids = []
    all_rel_titles = []
    for i in range(0, len(related_ids)):
        if len(related_ids[i]) != 0:
            all_rel_ids.extend(related_ids[i])
            all_rel_titles.extend(related_titles[i])
    related_var_df = pd.DataFrame()
    related_var_df['ids'] = all_rel_ids
    related_var_df['title'] = all_rel_titles
    related_var_df['db_num'] = related_db_num
    return related_var_df


def xfind_all_related_variables(unique_topic_list=[]):
    db_num_list = create_db_num_list()
    related_ids = []
    related_titles = []
    for x in range(0, len(db_num_list)):
        wb.db = db_num_list[x]
        print(db_num_list[x])
        db_var = wb.series.info()
        related_var_titles = []
        related_var_ids = []
        for i in range (0, len(db_var.items)):
            desc_split = db_var.items[i]['value'].split()
            id_split = db_var.items[i]['id']
            for val in desc_split:
                if val.lower() in unique_topic_list:
                    related_var_titles.append(db_var.items[i]['value'])
                    related_var_ids.append(id_split)
        related_ids.append(related_var_ids)
        related_titles.append(related_var_titles)
    return related_ids, related_titles