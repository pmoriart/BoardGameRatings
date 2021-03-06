#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 13:24:46 2018

@author: pamela
@purpose: create dataframe of features of all games and predict complexity
"""

import pickle
import pandas as pd
import numpy as np
from sklearn.preprocessing import Imputer


file_name = "/media/pamela/Stuff/xmls_parsed"

fileObject = open(file_name, 'rb')
with open(file_name, 'rb') as f:
    full_info = pickle.load(f)
fileObject.close()

#make dataframe of all games
red_info = list(full_info)

df_info = pd.DataFrame()
for game in range(len(red_info)):
    df_tmp = pd.DataFrame.from_dict(red_info[game], orient='index')
    df_info = pd.concat([df_info, df_tmp], axis=1)

df_info.index.rename('attribute', inplace=True)
df_info2 = df_info.transpose().copy()
df_info2.columns

#make variables for regression: nmech, is_party
nmech = [len(np.asarray(df_info2['mechanics'])[game]) for game in range(df_info2.shape[0])]

sub_df = pd.DataFrame()
sub_df['id'] = df_info2['id']
sub_df['ages'] = df_info2['age']
sub_df['nmech'] = nmech
sub_df['complexity'] = df_info2['complexity']
sub_df['name'] = df_info2['name']

##make complexity categorical
sub_df.reset_index(drop=0, inplace=True)
sub_df['categorical'] = sub_df['complexity']
mid_index = sub_df['complexity'][(sub_df['complexity'] >= 2)]# and (sub_df['complexity'] <=3.5)]
mid_index = mid_index[mid_index <= 3.5].index
low_index = sub_df['complexity'][sub_df['complexity'] < 2].index
high_index = sub_df['complexity'][sub_df['complexity'] > 3.5].index
sub_df['categorical'].replace(sub_df['complexity'][low_index], 'low', inplace=True)
sub_df['categorical'].replace(sub_df['complexity'][mid_index], 'medium', inplace=True)
sub_df['categorical'].replace(sub_df['complexity'][high_index], 'high', inplace=True)


sub_df2 = sub_df.copy(deep=True)

###make matrix of subdomains for each game
subdomains = pd.DataFrame(np.zeros([df_info2.shape[0], 7]),
                          columns=['Abstract', 'Thematic', 'Strategy',
                                   'Customizable', 'Party', 'War', 'Family'])
for game in range(df_info2.shape[0]):
    subdomain_tmp = np.asarray(df_info2['subdomains'])[game]
    if 'Abstract Games' in subdomain_tmp:
        subdomains.iloc[game][0] = 1
    if 'Thematic Games' in subdomain_tmp:
        subdomains.iloc[game][1] = 1
    if 'Strategy Games' in subdomain_tmp:
        subdomains.iloc[game][2] = 1
    if 'Customizable Games' in subdomain_tmp:
        subdomains.iloc[game][3] = 1
    if ('Party Games' in subdomain_tmp) or ("Children's Games" in subdomain_tmp):
        subdomains.iloc[game][4] = 1
    #if "Children's Games" in subdomain_tmp:
    #    subdomains.iloc[game][5] = 1
    if 'Wargames' in subdomain_tmp:
        subdomains.iloc[game][5] = 1
    if 'Family Games' in subdomain_tmp:
        subdomains.iloc[game][6] = 1
   
sub_df2 = sub_df2.join(subdomains)


file_name = '/home/pamela/Documents/Data/all_games_df'
fileObject = open(file_name, 'wb')
pickle.dump(df_info2, fileObject)
pickle.dump(sub_df2, fileObject)
fileObject.close()


######predict all games using RF model
file_name = '/home/pamela/Documents/Data/all_games_df'
fileObject = open(file_name, 'rb')
df_info2 = pickle.load(fileObject)
sub_df2 = pickle.load(fileObject)
fileObject.close()

file_name = '/home/pamela/Documents/Data/rf_fit_cached'
fileObject = open(file_name, 'rb')
rf_fit = pickle.load(fileObject)
fileObject.close()

#column order: ages, nmech, abstract, thematic, war, custom, family, party, strategy

predict_mat = pd.DataFrame(columns=['ages', 'nmech', 'abstract', 'thematic',
                                    'war', 'custom', 'family', 'party', 'strategy'])
predict_mat['ages'] = sub_df2['ages']
predict_mat['nmech'] = sub_df2['nmech']
predict_mat['abstract'] = sub_df2['Abstract']
predict_mat['thematic'] = sub_df2['Thematic']
predict_mat['war'] = sub_df2['War']
predict_mat['custom'] = sub_df2['Customizable']
predict_mat['family'] = sub_df2['Family']
predict_mat['party'] = sub_df2['Party']
predict_mat['strategy'] = sub_df2['Strategy']

#impute missing values in prediction matrix
imputer = Imputer()
transformed_values = imputer.fit_transform(predict_mat)
np.isnan(transformed_values).sum()

pred_all = rf_fit.predict(transformed_values)
game_complexity = pd.DataFrame({'id': sub_df2['id'],
                                'name': sub_df2['name'],
                                'complexity': pred_all})

file_name = "/home/pamela/Documents/game_complexity_db"
fileObject = open(file_name, 'wb')
pickle.dump(game_complexity, fileObject)
fileObject.close()
