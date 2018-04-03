#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  2 11:39:57 2018

@author: J Rishabh Kumar
@Contains : Pre-processing functions
"""

import pandas as pd
import numpy as np
import json

def mapprice(v): 
    if pd.isnull(v):
        return  [ np.nan]
    try:
        vv = v.split('-')
        p0 = vv[0].strip()[1:].replace(",","")
        return  [float(p0)]
    except ValueError:
        return  [np.nan]
    
    
def mapnumber_available_in_stock(v): 
    if pd.isnull(v):
        return np.NaN  ,np.NaN  
    try:
        vv = v.split('\xa0')
        return int(vv[0]),str(vv[1])
    except ValueError:        
        return np.NaN ,np.NaN    

    
def mapnumber_of_reviews(v): 
    if pd.isnull(v):
        return np.nan
    try:
        vv = v.replace(",","")
        return int(vv)
    except ValueError:
        return np.nan

    
def mapaverage_review_rating(v): 
    if pd.isnull(v):
        return np.nan
    try:
        vv = float(v.split('out')[0].strip())
        return vv
    except ValueError:        
        return np.nan
    
# read json data of seller    
def myseller(v):
    if pd.isnull(v):
        return 0
    try:
        vv = v.replace('=>',':')
        djson = pd.read_json(vv,orient='records') 
        dict_data = json.loads(djson)
        return dict_data
    except ValueError:        
        return 0      

#split category    
def mapcategories(srs):
    if pd.isnull(srs):
        return []
    else:
        return [cat.strip() for cat in srs.split(">")]  
    
#spliting items viewed before buying this item
def mapurlsplitter(v):
    if pd.isnull(v):
        return []
    else:
        return [c.strip() for c in v.split("|")]
    
def takeOutList(v):
    finalSet = []
    for lst in v:
        if not lst:
            continue
        else:
            for item in lst:
                if item not in finalSet:
                    finalSet.append(item)
    return finalSet

def addSum(v):
    added_sum = 0
    for lst in v:
        added_sum += lst
    return added_sum



        
