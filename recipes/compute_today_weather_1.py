import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu
import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime as dt
from datetime import datetime, timedelta

place_code = {"東京":{"prec_no":"44", "block_no":"47662", "type":"s1"}, "大分":{"prec_no":"83", "block_no":"0808", "type":"a1"}, "弘前":{"prec_no":"31", "block_no":"0166", "type":"a1"}}
base_url = "http://www.data.jma.go.jp/obd/stats/etrn/view/daily_%s.php?prec_no=%s&block_no=%s&year=%s&month=%s&day=&view=p1"

def str2float(str):
    try:
        return float(str)
    except:
        return 0.0

l = []

today = dt.today() - timedelta(days=1) #前日の気温を取得するため
day = int(today.day) 
month = int(today.month)
year = int(today.year)


for place in place_code.keys():
    prec_no = place_code[place]["prec_no"]
    block_no = place_code[place]["block_no"]
    data_type = place_code[place]["type"]

    year = year
    url = base_url%(data_type, prec_no, block_no, year, month)
    print(today, place, url)
    r = requests.get(url)
    r.encoding = r.apparent_encoding

    soup = BeautifulSoup(r.text)
    rows = soup.findAll('tr',class_='mtx')

    # 大分と弘前のページ
    if data_type == "a1":
        row = rows[3:][day-1]
        data = row.findAll('td')
        date = str(year) + "/" + str(month) + "/" + str(day)
        precip_total  = data[1].string #降水量(mm)合計
        temp_ave = data[4].string #平均気温
        temp_high = data[5].string #最高気温
        temp_low = data[6].string #最低気温
        daylight = data[13].string #日照時間
        d = {"date":date, "precip_total":precip_total, "temp_ave":temp_ave, "temp_high":temp_high, "temp_low":temp_low, "daylight":daylight, "place":place}
        l.append(d)
        
    # 東京のページ（大分、弘前とはテーブルのフォーマットが微妙に違う）
    else:
        row = rows[4:][day-1]
        data = row.findAll('td')
        date = str(year) + "/" + str(month) + "/" + str(day)
        precip_total  = data[3].string #降水量(mm)合計
        temp_ave = data[6].string #平均気温
        temp_high = data[7].string #最高気温
        temp_low = data[8].string #最低気温
        daylight = data[16].string #日照時間
        d = {"date":date, "precip_total":precip_total, "temp_ave":temp_ave, "temp_high":temp_high, "temp_low":temp_low, "daylight":daylight, "place":place}
        l.append(d)

df = pd.DataFrame(l)

todays_weather = dataiku.Dataset("todays_weather")
todays_weather.write_with_schema(df)