# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# Read recipe inputs
days_till_blooming = dataiku.Dataset("past_windows")
df = days_till_blooming.get_dataframe()

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
df.head()

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
"""
df.sort_values([u'場所', u'開花日'], ascending=True, inplace=True)

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
s_ave = df.groupby([u'場所'])[u'年初からの日数'].expanding().mean().values

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
df[u'年初からの日数_暦年平均']=s_ave

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
df = df.sort_values([u'場所', u'年月日_parsed'], ascending=False).reset_index(drop=True)

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
df.head()
"""

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
length = dataiku.get_custom_variables(typed=True)["window_size"]

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
var_to_vectorize = [u'平均気温', u'最高気温', u'最低気温', u'降水量合計', u'日照時間']

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
new_df = pd.DataFrame()
for city in df[u'場所'].unique():
    print(city)
    df_sub = df.loc[df[u'場所']==city].reset_index(drop=True)
    for var in var_to_vectorize:
        print(var)
        colname = var + u"推移"
        df_sub[colname] = np.nan
        long_vec = df_sub[var].values.tolist()

        for i in range(0, df_sub.shape[0]):
            small_vec = long_vec[i+1:i+length+1][::-1]
            if len(small_vec) == length:
                df_sub.loc[i, colname]=str(small_vec)
            else: break
    new_df = pd.concat([new_df, df_sub], ignore_index=True)

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
new_df = new_df[~new_df[u'平均気温推移'].isna()]

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
new_df.isna().sum()

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
vectorized_past = dataiku.Dataset("vectorized_past")
vectorized_past.write_with_schema(new_df)