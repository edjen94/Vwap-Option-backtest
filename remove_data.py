# -*- coding: utf-8 -*-
"""
Created on Sun Aug 15 02:06:46 2021

@author: jvsla
"""
import pandas as pd 
import os 
import glob
path=os.getcwd()
csv_files = glob.glob(os.path.join(path, "*.csv"))
for f in csv_files:
    opt= pd.read_csv(f)   
    
    opt.columns=['Symbol','Date','Time','Open','High','Low','Close','Volume','Open Interest']
    end='2021/04/16'
    find= opt.index[opt['Date']<end]
    opt=opt.drop(find)
    print(f)        
    opt.to_csv(f,index=False)
    



