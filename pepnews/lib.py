# -*- coding: UTF-8 -*-
# Copyright (C) 2018 Jean Bizot <jean@styckr.io>
""" Main lib for pepnews Project
"""

from os.path import split
import pandas as pd
import datetime
from newsapi import NewsApiClient
from time import sleep
import requests 
from google_trans_new import google_translator 

pd.set_option('display.width', 200)

def news():
    print('='*20)

    API_KEY ="65115d9c499d4450b83bb88f94ea1c8a"
    params = {
      #"q":"Xiaomi"
      #"country": "cn", #Note: you can't mix this param with the sources param.
      "sources": "Appledaily.com, Aastocks.com, Sina.com.cn, Gold678.com, Eastmoney.com, xinhua-net, Finance.ce.cn, the-wall-street-journal , Chinatimes.com" ,
      #"sources" :"bbc-news, bloomberg, CNBC, OilPrice.com, The Verge, Reuters", #Note: you can't mix this param with the country or category params.
      #"language":"cn", #it cannot be mixed with sources
      "pageSize" : "5",  #result number :20 is the default, 100 is the maximum.
      "sortBy" : "publishedAt" # options: relevancy, popularity, publishedAt
      #"category": "business", #Note: you can't mix this param with the sources param.
    }
    headers={'X-Api-Key': API_KEY,}
    main_url = "http://newsapi.org/v2/everything"
    top_headlines = requests.get(main_url, params=params, headers=headers).json()
    headlines= top_headlines['articles']
    print("Here are some of the top articles\n\n")
    top = [key["title"] for key in headlines] 

    for i, key in enumerate(top):
        print(i+1,key)
        
    print('='*20)

    translator = google_translator()  
    # text = translator.translate("Cerco un centro di gravità permanente", lang_src='it', lang_tgt='en')
    # print(text)
    for i, key in enumerate(top):
        topen = translator.translate(key, lang_src='zh', lang_tgt='en')
        print(i+1,topen)
    #topen = top.apply(lambda x: translator.translate(x, lang_src='fr', lang_tgt='en'))
    #options (headlines.url(10),headlines['title'].head(10),headlines['description'].head(10),headlines['content'].head(10))

    print('='*20)
   
def clean_data(data):
    """ clean data
    """
    # Remove columns starts with vote
    cols = [x for x in data.columns if x.find('vote') >= 0]
    data.drop(cols, axis=1, inplace=True)
    # Remove special characteres from columns
    data.loc[:, 'civility'] = data['civility'].replace('\.', '', regex=True)
    # Calculate Age from day of birth
    actual_year = datetime.datetime.now().year
    data.loc[:, 'Year_Month'] = pd.to_datetime(data.birthdate)
    data.loc[:, 'Age'] = actual_year - data['Year_Month'].dt.year
    # Uppercase variable to avoid duplicates
    data.loc[:, 'city'] = data['city'].str.upper()
    # Take 2 first digits, 2700 -> 02700 so first two are region
    data.loc[:, 'postal_code'] = data.postal_code.str.zfill(5).str[0:2]
    # Remove columns with more than 50% of nans
    cnans = data.shape[0] / 2
    data = data.dropna(thresh=cnans, axis=1)
    # Remove rows with more than 50% of nans
    rnans = data.shape[1] / 2
    data = data.dropna(thresh=rnans, axis=0)
    # Discretize based on quantiles
    data.loc[:, 'duration'] = pd.qcut(data['surveyduration'], 10)
    # Discretize based on values
    data.loc[:, 'Age'] = pd.cut(data['Age'], 10)
    # Rename columns
    data.rename(columns={'q1': 'Frequency'}, inplace=True)
    # Transform type of columns
    data.loc[:, 'Frequency'] = data['Frequency'].astype(int)
    # Rename values in rows
    drows = {1: 'Manytimes', 2: 'Onetimebyday', 3: '5/6timesforweek',
             4: '4timesforweek', 5: '1/3timesforweek', 6: '1timeformonth',
             7: '1/trimestre', 8: 'Less', 9: 'Never'}
    data.loc[:, 'Frequency'] = data['Frequency'].map(drows)
    return data

def Xmas():
    weekDays = ("Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday")
    thisXMas    = datetime.date(2020,12,25)
    thisXMasDay = thisXMas.weekday()
    thisXMasDayAsString = weekDays[thisXMasDay]
    print("This year's Christmas is on a {}".format(thisXMasDayAsString))

    nextNewYear     = datetime.date(2021,1,1)
    nextNewYearDay  = nextNewYear.weekday()
    nextNewYearDayAsString = weekDays[nextNewYearDay]
    print("Next New Year is on a {}".format(nextNewYearDayAsString))

if __name__ == '__main__':
    # For introspections purpose to quickly get this functions on ipython
    import pepnews
    folder_source, _ = split(pepnews.__file__)
    df = pd.read_csv('{}/data/data.csv.gz'.format(folder_source))
    clean_data = clean_data(df)
    print(news())
    print(' dataframe cleaned')
    print(Xmas())
