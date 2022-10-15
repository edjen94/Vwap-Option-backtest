# Vwap backtest on option data in NSE
* Pass futures and option data through time_edit.py if the data is shifted
* Then pass Futures data through Data_convert.py and options data throughData_convert_options.py
* Some data may have need some cleaning and editing, under these circumstances use symbol_edit.py and remove_data.py
* For now use the 2021_f1_MERGED.csv as the sample futures data, it has all the data from Jan 2021 to April 2021
* Use JAN_all_EXPIRY.csv and the other months as option data
* Final output is in CSV

##Brief on how the code works

We look at the close of the Fut and then compare it with the vwap data at 12:30, then we short a call option if the close<vwap and short a put option if close>vwap.
The backtest aims to look at the total P&L at the end of each month. Each month needs to be done seperately.

