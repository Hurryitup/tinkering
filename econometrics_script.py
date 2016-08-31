''' 

>> Written by: Aditya Hurry
>> For Ec15 Regression Project, Spring 2016 - Rafael Roman and Aditya Hurry

'''
import pandas as pd
import pandas.io.data as web
import datetime as dt

'''date range'''
start = dt.datetime(2007, 4, 2)
end = dt.datetime(2016, 4, 25)

'''Set up for the data query'''
ticker = "AAPL"
source = "yahoo"
hedge_sp = web.DataReader(ticker, source, start, end)
mondays = pd.date_range('4/2/2007', periods=474, freq='W-MON')

'''extracting only days that are mondays'''
dateix = hedge_sp.ix[mondays]
for day in dateix.index:
        try:
                mondayList.append(hedge_sp.loc[day])
        except:
                print "nevermind"

'''Exporting the data'''
mondaySeries = pd.DataFrame(mondayList)
mondaySeries.to_csv("data.csv", mode="a")