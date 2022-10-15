# -*- coding: utf-8 -*-
"""
Created on Wed Aug 11 00:04:21 2021

@author: jvsla
"""

import pandas as pd 
from pandas import DataFrame as df
import numpy as np
import datetime
df= pd.read_csv('2021_f1_MERGED.csv',parse_dates=['Datetime'])
df= df.set_index(df['Datetime'])
x=pd.read_csv('APR_ALL-EXPIRY.csv')
x=x.set_index('Datetime')        
def vwap(df):    
    data={'Datetime':df['Datetime'],
        'vp':df['Volume']*((df['Close']+df['High']+df['Low'])/3),
          'vol':df.groupby((df["Datetime"]).dt.floor("D"))["Volume"].cumsum()}        
    df1=pd.DataFrame(data)
    vp= df1.groupby(pd.Grouper(key='Datetime', freq='D')).vp.cumsum()
    vwap=vp/df1['vol']
    
    return df.insert(6,'Vwap',vwap,True)
vwap(df)

def check_spot():
    
    match_timestamp = "12:30:00"
    value_check=df.loc[df.index.strftime("%H:%M:%S") == match_timestamp]
        
    return value_check['Close'],value_check['Vwap']



def trigger_check():
    deets=pd.DataFrame(check_spot())
    deets=deets.transpose()
    sell_PE=deets['Close']>deets['Vwap']
    sell_PE=sell_PE[sell_PE].index
    sell_CE=deets['Close']<deets['Vwap']
    sell_CE=sell_CE[sell_CE].index
    return sell_PE,sell_CE



def option_strike_roundoff():
    PE_df_strike= round((df[df['Datetime'].isin(trigger_check()[0])]['Close'])/50)*50    
    CE_df_strike=round((df[df['Datetime'].isin(trigger_check()[1])]['Close'])/50)*50    
    
    return (PE_df_strike.astype(float)).astype(int),(CE_df_strike.astype(float)).astype(int)


def short_options():
    data=pd.DataFrame(option_strike_roundoff())     
    data=data.transpose()
    data.columns=['PEstrike','CEstrike']   
    data=data.fillna(0)
    data['PEstrike']=(data['PEstrike'].astype(int)).astype(str)+'PE'
    data['CEstrike']=(data['CEstrike'].astype(int)).astype(str)+'CE'
    #x=pd.read_csv('APR_ALL-EXPIRY.csv')
    #x=x.set_index('Datetime')        
    x.index=pd.to_datetime(x.index)
    z=pd.merge(data,x,left_on=data.index,right_on=x.index)
    pe_strike=z.loc[z['PEstrike']==z['Symbol']]
    ce_strike=z.loc[z['CEstrike']==z['Symbol']]
    return pe_strike,ce_strike,x,z


def get_option_details():
    opt_deets=short_options()[2]        
    opt_deets['Datetime']=opt_deets.index
    PE=pd.DataFrame(short_options()[0])
    PE=PE.set_index('key_0')
    CE=pd.DataFrame(short_options()[1])
    CE=CE.set_index('key_0')
    start='12:30:00'
    end='15:15:00'
    get_data =opt_deets.loc[(opt_deets.index.strftime("%H:%M:%S") > start )&(opt_deets.index.strftime("%H:%M:%S") <=end )]
    get_data=get_data.set_index('Symbol')
    
    PE_range=get_data.loc[get_data.index.isin(PE['Symbol'].values)]  
    CE_range=get_data.loc[get_data.index.isin(CE['Symbol'].values)]
    return PE,CE,PE_range,CE_range

#try to find why the warning is coming from here 
def calculate_price_SL():
    
    opt_deets= short_options()[2]
    #opt_deets=opt_deets.set_index('Datetime')
    data_PE=get_option_details()[0]['Close'],get_option_details()[0]['Close']*1.32,get_option_details()[0]['Symbol']
    short_PE=pd.DataFrame(data_PE)    
    short_PE=short_PE.transpose()
    short_PE.columns=['Close','SL','Symbol']
    short_PE['Datetime']=short_PE.index
    short_PE['Date']=[d.date() for d in short_PE['Datetime']]
    short_PE=short_PE.set_index(['Date','Symbol'])
    
    
    data_CE=get_option_details()[1]['Close'],get_option_details()[1]['Close']*1.32,get_option_details()[1]['Symbol']
    short_CE=pd.DataFrame(data_CE)
    short_CE=short_CE.transpose()
    short_CE.columns=['Close','SL','Symbol']
    short_CE['Datetime']=short_CE.index
    short_CE['Date']=[d.date() for d in short_CE['Datetime']]
    short_CE=short_CE.set_index(['Date','Symbol'])
    
    close_time='15:15:00'
    get_close_value=opt_deets.loc[pd.to_datetime(opt_deets.index).strftime("%H:%M:%S") == close_time]
    get_close_value['Datetime']=get_close_value.index
    get_close_value=get_close_value.set_index('Symbol')
    
    EOD_close_PE=get_close_value.loc[get_close_value.index.isin(get_option_details()[0]['Symbol'].values)]  
    EOD_close_PE['Symbol']=EOD_close_PE.index
    EOD_close_PE['Datetime']=pd.to_datetime(EOD_close_PE['Datetime'])
    EOD_close_PE=EOD_close_PE.set_index(EOD_close_PE['Datetime'])
    EOD_close_PE=EOD_close_PE.set_index([EOD_close_PE.index.date,'Symbol'])
    
    EOD_close_CE=get_close_value.loc[get_close_value.index.isin(get_option_details()[1]['Symbol'].values)]  
    EOD_close_CE['Symbol']=EOD_close_CE.index
    EOD_close_CE['Datetime']=pd.to_datetime(EOD_close_CE['Datetime'])
    EOD_close_CE=EOD_close_CE.set_index(EOD_close_CE['Datetime'])
    EOD_close_CE=EOD_close_CE.set_index([EOD_close_CE.index.date,'Symbol'])
    
    exit_price_PE= []
    exit_price_CE=[]
    
    PE= get_option_details()[2]    
    PE['Symbol']=PE.index    
    PE['Date']= [d.date() for d in PE['Datetime']]
    PE=PE.set_index(['Date','Symbol'])
    
    CE= get_option_details()[3]    
    CE['Symbol']=CE.index    
    CE['Date']= [d.date() for d in CE['Datetime']]
    CE=CE.set_index(['Date','Symbol'])
    
    
    
    #returns PUT DETAILS
    PE_final=pd.merge(PE,short_PE,left_index=True,right_index=True)
    
    PE_final['Result']=np.where(PE_final['High']>=PE_final['SL'],True,False)
    x= PE_final.loc[PE_final['Result']==False]
    x=x.reset_index()
    x=x.drop(['Date','Datetime_y'],axis=1)
    
    x=x.set_index('Datetime_x')
    x=x.set_index([x.index.date,'Symbol'])    
    x = x[~x.index.duplicated(keep='first')]
    x_EOD=EOD_close_PE.loc[EOD_close_PE.index.isin(x.index.values)]     
    for values in x:
        exit_price_PE.append(x_EOD['Open'])
    
   
    
    y= PE_final.loc[PE_final['Result']==True]
    y=y.reset_index()
    y=y.drop(['Date','Datetime_y'],axis=1)
    y=y.set_index('Datetime_x')
    y=y.set_index([y.index.date,'Symbol'])    
    y = y[~y.index.duplicated(keep='first')]
    
    for values in y :
         exit_price_PE.append(y['SL'])
    
    
    # returns CALL details
    CE_final=pd.merge(CE,short_CE,left_index=True,right_index=True)
    
    CE_final['Result']=np.where(CE_final['High']>=CE_final['SL'],True,False)
    c= CE_final.loc[CE_final['Result']==False]
    c=c.reset_index()
    c=c.drop(['Date','Datetime_y'],axis=1)
    
    c=c.set_index('Datetime_x')
    c=c.set_index([c.index.date,'Symbol'])    
    c = c[~c.index.duplicated(keep='first')]
    c_EOD=EOD_close_CE.loc[EOD_close_CE.index.isin(c.index.values)]    
    for values in c:
        exit_price_CE.append(c_EOD['Open'])
    
    e= CE_final.loc[CE_final['Result']==True]
    e=e.reset_index()
    e=e.drop(['Date','Datetime_y'],axis=1)
    e=e.set_index('Datetime_x')
    e=e.set_index([e.index.date,'Symbol'])    
    e = e[~e.index.duplicated(keep='first')]
    
    for values in e :
         exit_price_CE.append(e['SL'])
           
    
    
    
    
    return short_PE['Close'],exit_price_PE,short_CE['Close'],exit_price_CE


 
def calculate_PL():
    PE_close= pd.DataFrame(calculate_price_SL()[0])  
    PE_SL_EOD=pd.DataFrame(calculate_price_SL()[1])
    PE_SL_EOD=PE_SL_EOD.transpose()
    PE_SL_EOD=PE_SL_EOD.loc[:,~PE_SL_EOD.columns.duplicated()]
    PE_SL_EOD=PE_SL_EOD.fillna(0)
    check_PE=PE_SL_EOD[PE_SL_EOD['SL']!=0]['Open'].index
    x1=PE_SL_EOD.loc[check_PE,'Open']
    PE_SL_EOD['Open']=PE_SL_EOD.drop(x1.index)
    PE_SL_EOD=PE_SL_EOD.fillna(0)
    PE_SL_EOD['EOD CLOSE']= PE_SL_EOD['Open']+PE_SL_EOD['SL']

    CE_close= pd.DataFrame(calculate_price_SL()[2])  
    CE_SL_EOD=pd.DataFrame(calculate_price_SL()[3])
    CE_SL_EOD=CE_SL_EOD.transpose()
    CE_SL_EOD=CE_SL_EOD.loc[:,~CE_SL_EOD.columns.duplicated()]
    CE_SL_EOD=CE_SL_EOD.fillna(0)
    check_CE=CE_SL_EOD[CE_SL_EOD['SL']!=0]['Open'].index
    x2=CE_SL_EOD.loc[check_CE,'Open']
    CE_SL_EOD['Open']=CE_SL_EOD.drop(x2.index)
    CE_SL_EOD=CE_SL_EOD.fillna(0)
    CE_SL_EOD['EOD CLOSE']= CE_SL_EOD['Open']+CE_SL_EOD['SL']
    
    PL_PE= (PE_close['Close'].values) - (PE_SL_EOD['EOD CLOSE'].values)
    PL_CE= (CE_close['Close'].values)- (CE_SL_EOD['EOD CLOSE'].values)    
    #PL=float(PL_PE+PL_CE)
    
   
    #lot=50.0
    #final_PL=PL*lot
    
    
    return PE_close['Close'],PE_SL_EOD['EOD CLOSE'].values,CE_close['Close'],CE_SL_EOD['EOD CLOSE'].values

a=calculate_PL()[0]
b=calculate_PL()[1]
c=calculate_PL()[2]
d=calculate_PL()[3]

 
daily_data1=pd.DataFrame({'PE_short':calculate_PL()[0],
                           'PE_close':calculate_PL()[1]
                            })
daily_data1['PE_PL']=(daily_data1['PE_short']-daily_data1['PE_close'])*50



daily_data2=pd.DataFrame({'CE_short':calculate_PL()[2],
                           'CE_close':calculate_PL()[3]
                            })
daily_data2['CE_PL']=(daily_data2['CE_short']-daily_data2['CE_close'])*50

final_data= pd.concat([daily_data1['PE_PL'],daily_data2['CE_PL']])
#final_data.to_csv('Vwapstrategy_backtestF1_APR_daily.csv')


    

    








