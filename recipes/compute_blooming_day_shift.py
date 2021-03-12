# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# Read recipe inputs
three_cities_blooming_day_joined = dataiku.Dataset("three_cities_blooming_day_joined")
df = three_cities_blooming_day_joined.get_dataframe()

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
df = df.sort_values([u'場所', '年月日_parsed'])

d = {}
for city in df[u'場所'].unique():
    d[city] = {}
    df_city = df[df[u'場所']==city]
    for year in df_city[u'年'].unique():
        blooming_day = df[(df[u'場所']==city)&(df[u'年']==year)][u'開花日'].unique()[0]
        d[city][year] = blooming_day

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
d

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
df_bloom = df[df[u'状況']=='開花']
df_bloom

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
df_new = pd.DataFrame()
for city in df[u'場所'].unique():
    print(city)
    df_sub = df[df[u'場所']==city]
    year_seq = df_sub[df_sub[u'年月日_parsed']>df_sub[u'開花日']][u'年'].values
    shifted_year_seq = [d[city][year+1] if year < 2021 else np.nan for year in year_seq]
    df_sub.loc[df_sub[u'年月日_parsed']>df_sub[u'開花日'], u'開花日'] = shifted_year_seq
    df_new = pd.concat([df_new, df_sub])

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
df_new.head()

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# Write recipe outputs
blooming_day_shift = dataiku.Dataset("blooming_day_shift")
blooming_day_shift.write_with_schema(df_new)