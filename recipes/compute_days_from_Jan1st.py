# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu

# Read recipe inputs
days_till_blooming = dataiku.Dataset("days_till_blooming")
df = days_till_blooming.get_dataframe()

df.sort_values([u'場所', u'開花日'], ascending=True, inplace=True)

s_ave = df.groupby([u'場所'])[u'年初からの日数'].expanding().mean().values

df[u'年初からの日数_暦年平均']=s_ave

# Write recipe outputs
days_from_Jan1st = dataiku.Dataset("days_from_Jan1st")
days_from_Jan1st.write_with_schema(df)
