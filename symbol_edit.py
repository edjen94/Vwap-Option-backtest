# -*- coding: utf-8 -*-
"""
Created on Sun Aug 22 15:36:22 2021

@author: jvsla
"""

import pandas as pd 

df=pd.read_csv('APR_22nd.csv')
x=[]
for i, v in enumerate(df.Symbol):
        #print(v[5:])        
        x.append(v[7:])
print(x)      
df['Symbol']=x

df.to_csv('APR_22nd.csv',index=False)
