from sklearn.model_selection import train_test_split
from sklearn.ensemble import AdaBoostRegressor

import pandas as pd
import numpy as np

import pickle

## read the file

df=pd.read_csv('hour.csv')


## preprocess

df.rename(columns={'instant':'rec_id',
'dteday':'datetime',
'holiday':'is_holiday',
'workingday':'is_workingday',
'weathersit':'weather_condition',
'hum':'humidity',
'mnth':'month',
'cnt':'total_count',
'hr':'hour',
'yr':'year'},inplace=True)

df['temp_celsius'] = (47 * df.temp) - 8

#for i in range(len(df.temp_celsius)):
#    df['temp_celsius'][i] = int(df.temp_celsius[i])

df = df[['hour', 'is_holiday','temp_celsius', 'weekday','total_count']]

df.temp_celsius = df.temp_celsius.astype(int)
df.is_holiday = df.is_holiday.astype('category')
df.weekday = df.weekday.astype('category')

df = pd.get_dummies(df)


## modelling

x = df.drop(columns = ['total_count'])
y = df['total_count']

#print(x)

ada = AdaBoostRegressor()
ada.fit(x,y)
pickle.dump(ada, open('model.pkl','wb'))