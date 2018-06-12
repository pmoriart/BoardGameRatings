#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 13:24:46 2018

@author: pamela
"""

import pickle
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import scipy
import statsmodels.api as sm
import statsmodels.genmod as 
import statsmodels as sm
from sklearn import datasets, linear_model
from sklearn.model_selection import train_test_split

#file_name = "/media/pamela/Stuff/compiled_info"
file_name = '/home/pamela/Documents/xmls_parsed.pickle'
fileObject = open(file_name,'rb') 
with open(file_name, 'rb') as f:
    full_info = pickle.load(f)
fileObject.close()   


#remove games without a complexity rating or with fewer than 10 people having rated it
red_info = list(full_info)

idx_to_del = []
for i in range(len(red_info)):
    if red_info[i]['complexity'] == '0' or red_info[i]['age'] == '':
        idx_to_del.append(i)
    
for i in range(len(idx_to_del)-1,0, -1):       
    del red_info[idx_to_del[i]]

    
idx_to_del = []
for i in range(len(red_info)):
    if int(red_info[i]['num_comp']) < 10:
        idx_to_del.append(i)
for i in range(len(idx_to_del)-1,0, -1):       
    del red_info[idx_to_del[i]]
    
#pull out the variables I'm using
ages = [red_info[game]['age'] for game in range(len(red_info))]
ages = list(map(float, ages))
complexities =  [red_info[game]['complexity'] for game in range(len(red_info))]
complexities = list(map(float, complexities))

for i in range(len(ages)):
#to_drop = [compiled_info[game]['id'] for game in range(len(compiled_info)) if compiled_info[game]['complexity'] == 0]
#del compiled_info[43610]ge(len(ages)):
    try: 
        ages[i] = float(ages[i])
    except ValueError:
        print(i)

nmech = [len(red_info[game]['mechanics']) for game in range(len(red_info))]
nmech = list(map(float, nmech))

#nplayerrange = [int(red_info[game]['maxplayers']) - int(red_info[game]['minplayers']) for game in range(len(compiled_info))]

is_strategy = ['Strategy Games' in red_info[game]['subdomains'] for game in range(len(red_info))]
is_party = ['Party Game' in red_info[game]['categories'] for game in range(len(red_info))]
strat_bool = np.array(is_strategy) * 1
party_bool = np.array(is_party) * 1

#make a dataframe of the cleaned and processed variables I'm using
all_vars = pd.DataFrame()
all_vars['ages'] = ages
all_vars['nmech'] = nmech
all_vars['strategy'] = strat_bool
all_vars['party'] = party_bool
all_vars['complexity'] = complexities
#all_vars['nplayerrange'] = nplayerrange


all_no0 = all_vars[all_vars['complexity'] != 0 ]
#all_no0['std_complex'] =  all_no0['complexity']/5.0001

bounded_y = (all_no0['complexity'] - 1)/4
bounded_y[bounded_y == 0]
bounded_y[bounded_y == 1]
bounded_y[bounded_y == 0] = .001
bounded_y[bounded_y == 1] = 0.99
continuous_y = scipy.special.logit(bounded_y)
continuous_y[np.isnan(continuous_y)]

plt.figure()
plt.hist(continuous_y)#approximatley normal!