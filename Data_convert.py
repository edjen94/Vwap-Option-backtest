"""
Created on Sat Aug  7 00:53:17 2021

@author: jvsla
"""
import pandas as pd 
from pandas import DataFrame as df
import datetime as dt
import time 

x= pd.read_csv('NIFTY_JAN_2021.csv')
#x=x.drop('Unnamed: 0', axis=1)
x.columns=['Symbol','Date','Time','Open','High','Low','Close','Volume','-']
x['Time'] = pd.to_timedelta(x['Time']+':00')
x['Time'] = x['Time'].astype(str).map(lambda x: x[7:])
x['Datetime']=x[['Date','Time']].apply(lambda x : '{},{}'.format(x[0],x[1]), axis=1)
x['Datetime'] = pd.to_datetime(x['Datetime'], format='%Y%m%d,%H:%M:%S')
x = x.set_index(['Datetime'])

ohlc = {
    'Open': 'first',
    'High': 'max',
    'Low': 'min',
    'Close': 'last',
    'Volume': 'sum'
}
x= x.resample('15min').apply(ohlc)
x=x.between_time('9:15','15:30')
x=x.dropna()
x.to_csv('NIFTY_JAN_2021_15min.csv')




