# -*- coding: utf-8 -*-
"""
Created on Mon Aug 16 01:13:46 2021

@author: jvsla
"""

import pandas as pd 
import os
import glob 

path=os.getcwd()
csv_files = glob.glob(os.path.join(path, "*.csv"))

try:
    for f in csv_files:    
         df=pd.read_csv(f) 
         
         df['Time'] = pd.to_timedelta(df['Time']+':00')    
         df['Time'] = df['Time'].astype(str).map(lambda x: x[7:])
         df['Date']=pd.to_datetime(df['Date']).dt.strftime('%Y%m%d')
         df['Datetime']=df[['Date','Time']].apply(lambda x : '{},{}'.format(x[0],x[1]), axis=1)
         df['Datetime'] = pd.to_datetime(df['Datetime'], format='%Y%m%d,%H:%M:%S')
         df = df.set_index(['Datetime'])
         ohlc = {
             'Symbol':'first',
             'Open': 'first',
             'High': 'max',
             'Low': 'min',
             'Close': 'last',
             'Volume': 'sum',
             'Open Interest': 'sum'
             
         }
         df= df.resample('15min').apply(ohlc,'Symbol')
         df=df.between_time('9:15','15:30')
         df=df.dropna()
         #print and check if all data is being processed 
         df.to_csv(f)
         print(df)
except ValueError:
    pass


 

    

