# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE_MAGIC_CELL
# Automatically replaced inline charts by "no-op" charts
# %pylab inline

# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu
import requests
from bs4 import BeautifulSoup
import csv

place_code = {"東京":{"prec_no":"44", "block_no":"47662", "type":"s1"},
              "大分":{"prec_no":"83", "block_no":"0808", "type":"a1"},
              "弘前":{"prec_no":"31", "block_no":"0166", "type":"a1"}}
base_url = "http://www.data.jma.go.jp/obd/stats/etrn/view/daily_%s.php?prec_no=%s&block_no=%s&year=%s&month=%s&day=&view=p1"

def str2float(str):
    try:
        return float(str)
    except:
        return 0.0

l = []
for place in place_code.keys():
    prec_no = place_code[place]["prec_no"]
    block_no = place_code[place]["block_no"]
    data_type = place_code[place]["type"]

    for year in range(1991, 2022):
        print(year)
        if year == 2021:
            last_month = 3
        else:
            last_month = 13
        for month in range(1,last_month):
            url = base_url%(data_type, prec_no, block_no, year, month)
            print(place, year, month, url)
            r = requests.get(url)
            r.encoding = r.apparent_encoding

            soup = BeautifulSoup(r.text)
            rows = soup.findAll('tr',class_='mtx')

            if data_type == "a1":
                rows_data = rows[3:]

                for row in rows_data:
                    data = row.findAll('td')
                    day = data[0].findAll('a')[0].string # 日にち
                    date = str(year) + "/" + str(month) + "/" + day
                    precip_total  = data[1].string #降水量(mm)合計
                    temp_ave = data[4].string #平均気温
                    temp_high = data[5].string #最高気温
                    temp_low = data[6].string #最低気温
                    daylight = data[13].string #日照時間
                    d = {"date":date, "precip_total":precip_total, "temp_ave":temp_ave, "temp_high":temp_high, "temp_low":temp_low, "daylight":daylight, "place":place}
                    l.append(d)
            else:
                rows_data = rows[4:]
                for row in rows_data:
                    data = row.findAll('td')

                    day = data[0].findAll('a')[0].string
                    date = str(year) + "/" + str(month) + "/" + day
                    precip_total  = data[3].string #降水量(mm)合計
                    temp_ave = data[6].string #平均気温
                    temp_high = data[7].string #最高気温
                    temp_low = data[8].string #最低気温
                    daylight = data[16].string #日照時間
                    d = {"date":date, "precip_total":precip_total, "temp_ave":temp_ave, "temp_high":temp_high, "temp_low":temp_low, "daylight":daylight, "place":place}
                    l.append(d)

df = pd.DataFrame(l)

historical_tenki_scraped = dataiku.Dataset("historical_tenki_scraped")
historical_tenki_scraped.write_with_schema(df)