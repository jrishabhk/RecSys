#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  2 11:42:33 2018

@author: J Rishabh Kumar
@main
"""

import numpy as np
import pandas as pd
from prepro_func import *


#Loading dataset 
dataset = pd.read_csv("/home/j/AnacondaProjects/RecommendationSystem/Dataset/amazon_co-ecommerce_sample.csv")

product_mat = pd.DataFrame(dataset,copy = True)
del product_mat['description']
prod_uiq_id = product_mat.uniq_id
prod_name = pd.Series(product_mat.product_name.unique())
manufacturer = pd.Series(product_mat.manufacturer.unique())
dfbuyafter = product_mat.loc[:,['uniq_id']]
dfbuyafter = dfbuyafter.join(product_mat['items_customers_buy_after_viewing_this_item'].str.split('|', expand=True).stack().map(str.strip).reset_index(level=1, drop=True).rename('items_customers_buy_after_viewing_this_item'))
dfbuyafter.shape
dfbuyalso = product_mat.loc[:,['uniq_id']]
dfbuyalso = dfbuyalso.join(product_mat['customers_who_bought_this_item_also_bought'].str.split('|', expand=True).stack().map(str.strip).reset_index(level=1, drop=True).rename('customers_who_bought_this_item_also_bought'))
dfbuyalso.shape
category_lists = product_mat['amazon_category_and_sub_category']
product_mat.info()


"""
    code is here
    
"""
#changing number if available in stocks to int

foo = lambda x: pd.Series([i for i in mapnumber_available_in_stock(x)])
prod_stock= product_mat.loc[:]['number_available_in_stock']
rev = prod_stock.apply(foo)
rev.columns = ['number_available_in_stock','class_available_in_stock']
product_mat['number_available_in_stock'],product_mat['class_available_in_stock']  = rev['number_available_in_stock'],rev['class_available_in_stock']

product_mat.info()


#changing price to float and removing euro sign

foo = lambda x: pd.Series([i for i in mapprice(x)])
prod_price = product_mat.loc[:]['price']
rev = prod_price.apply(foo)
product_mat['price'] = rev

product_mat.info()


#converting no. of reviews to int

if product_mat['number_of_reviews'].dtype != 'int64':  
    product_mat['number_of_reviews'] = product_mat['number_of_reviews'].map(mapnumber_of_reviews)
    
product_mat.info()


# avg review rating to float
if product_mat['average_review_rating'].dtype != 'float64':
    product_mat['average_review_rating'] = product_mat['average_review_rating'].map(mapaverage_review_rating)

product_mat.info()



#Splitting products customers saw before buying this
product_mat['items_customers_buy_after_viewing_this_item'] = product_mat['items_customers_buy_after_viewing_this_item'].apply(mapurlsplitter)

#Split customers_who_bought_this_item_also_bought
product_mat['customers_who_bought_this_item_also_bought'] = product_mat['customers_who_bought_this_item_also_bought'].apply(mapurlsplitter)

# categories and their count of depth
product_mat['amazon_category_and_sub_category'] = product_mat['amazon_category_and_sub_category'].apply(mapcategories)
product_mat['amazon_category_and_sub_category'].map(lambda lst: len(lst)).value_counts()



df_count_buyalso = dfbuyalso.groupby('uniq_id')['customers_who_bought_this_item_also_bought'].count().reset_index()
df_count_buyafter = dfbuyafter.groupby('uniq_id')['items_customers_buy_after_viewing_this_item'].count().reset_index()

a = pd.Series(dfbuyafter['items_customers_buy_after_viewing_this_item'].value_counts())
b = pd.Series(dfbuyalso['customers_who_bought_this_item_also_bought'].value_counts())

dfx = product_mat['sellers'][0:2][1]
dfx
#split the sellers data, put it into another 
sellers = product_mat['sellers'].str
sellers = sellers.map(myseller)

list1 = list(product_mat['items_customers_buy_after_viewing_this_item'])
list2 = list(product_mat['customers_who_bought_this_item_also_bought'])
item_set1 = takeOutList(list1)
item_set2 = takeOutList(list2)


item_set = pd.Series(item_set1 + item_set2)
item_set = pd.Series(item_set.unique())


#total no. of transaction
total_tran = addSum(a) + addSum(b)
matrix = pd.DataFrame()
matrix = pd.DataFrame(matrix, index = prod_uiq_id, columns= item_set ,dtype =float)





