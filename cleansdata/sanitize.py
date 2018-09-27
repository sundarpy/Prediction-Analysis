# import pandas as pd
# import json 
# import numpy as np
# import requests 
# import ast
# import sys
# import matplotlib.pyplot as plt
# from django.http import HttpResponse, JsonResponse

# entity = 'cf33fbcca4e94777bde9658ee7e90550'
# propertysetname = 'power_turbine_aspect'
# dates ='2018-06-22T00:00:00Z&to=2018-08-22T23:50:00Z'
# url = "api/iottimeseries/v3/timeseries/'{}'/'{}'/?from='{}'".format(entity,propertysetname,dates).replace("'", "")
# headersKey = { 'Accept' : 'application/json', 'Content-Type' : 'application/json','Authorization' : 'Bearer'}
# TimeUrl = url 
# resp = requests.get(TimeUrl, headers=headersKey)
# event = resp.content  # IN BYTES
# respo = event.decode('utf-8')
# final_response = ast.literal_eval(respo)  # IN DICT
# flag = 0
# try:
#     if('status' in final_response):  
#         status_error = {"status":final_response['status'],"error":final_response['error'],"message":final_response['message']}
#         response = status_error
#     else:
#         flag = 1
#         if(flag==1):
# 	    	df = pd.DataFrame(final_response) # ORIGINAL
# 		    if(df.isnull().values.any()==True):
# 		        df = df.interpolate(method='linear')
# 		    df_normalise = df.loc[:, df.columns != '_time']
# 		    time = df['_time']
# 		    idx = 0
# 		    df_normalise.insert(loc=idx, column='_time', value = time)
# 		    df_normalise = df_normalise.drop_duplicates()
# 		    df_normalise = df_normalise.dropna()
# 		    df_timestamp = df_normalise
# 		    a = {
# 		        "assetId" :  "cf33fbcca4e94777bde9658ee7e90550",
# 		        "aspectName" : str(propertysetname),
# 		        "datapoints" : df_timestamp.to_dict('records')}
# 		    cleans_data = json.dumps(a) #  DATA RETURN AFTE CLEANSING
# 		    response = cleans_data
# except Exception as e:
#         response = "Caught this Error: " + ' ' + str(e)
# return HttpResponse(response)        

#===============================Prediction Data=================#
%%time


import re
import pandas as pd
import json 
import numpy as np
import requests 
import ast
import sys
import matplotlib.pyplot as plt
import time
import seaborn as sns
import warnings
def ignore_warn(*args, **kwargs):
    pass
warnings.warn = ignore_warn
import statsmodels
import statsmodels.api as sm
from statsmodels.tsa.stattools import coint, adfuller
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
import warnings
import itertools
import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
import itertools
import statistics 


from statsmodels.tsa.arima_model import ARMA


%matplotlib inline



with open('msph_data.json') as f:
    data = json.load(f)

df = pd.DataFrame(data) # ORIGINAL
#print(df.head())



if(df.isnull().values.any()==True):
    df = df.interpolate(method='linear')

df = df.drop_duplicates()
df = df.dropna()


df_timestamp = df



key = 'speed'

scaler = StandardScaler()
df_timestamp["{}".format(key)] = scaler.fit_transform(df_timestamp[["{}".format(key)]])
df_new =  df_timestamp[['_time',"{}".format(key)]]
df_new.set_index('_time',inplace=True)




date_sale = df_new.copy()
date_sale.index = pd.to_datetime(date_sale.index)
y = date_sale



t1 = str(y.index[0])
t2 = str(y.index[1])

first = re.split('[-: ]', t1)
second= (re.split('[-: ]', t2))
old = list(map(int, first))
new = list(map(int, second))
delta = [a - b for a, b in zip(new,old)]
val = max(delta)
if(delta[0]>0):
    frequency = 'A'
elif(delta[1]>0):
    frequency = 'M'
elif(delta[2]>0):
    frequency = 'D'
elif(delta[3]>0):
    frequency = 'H'
elif(delta[4]>0):
    frequency = 'T'
elif(delta[5]>0):
    frequency = 'S'
elif(delta[2]>0):
    frequency = 'W'
    



import itertools
p = d = q = range(0, 2)
pdq = list(itertools.product(p, d, q))
seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]




for param in pdq:
    for param_seasonal in seasonal_pdq:
        try:
            mod = sm.tsa.statespace.SARIMAX(df,
                                            order=param,
                                            seasonal_order=param_seasonal,
                                            enforce_stationarity=False,
                                            enforce_invertibility=False)

            results = mod.fit()
            
            print('ARIMA{}x{}12 - AIC:{}'.format(param, param_seasonal, results.aic))
        except:
            continue
            
            
cnt = 0
stop = 0
AIC = float('inf')
for param in pdq:
    for param_seasonal in seasonal_pdq:
        try:
            mod = sm.tsa.statespace.SARIMAX(y,
                                            order=param,
                                            seasonal_order=param_seasonal,
                                            enforce_stationarity=False,
                                            enforce_invertibility=False)
            
            results = mod.fit()
            if results.aic < AIC and stop<100:
                AIC = results.aic
                best_params = param
                best_params_seasonal = param_seasonal
                stop+=1
                #print('ARIMA{}x{} 12 - AIC:{}'.format(param, param_seasonal, results.aic))
        except Exception as e:
            #print(e)
            continue
    


mod = sm.tsa.statespace.SARIMAX(y,
                                order=(best_params[0],best_params[1],best_params[2]),
                                seasonal_order=(best_params_seasonal[0],best_params_seasonal[1],best_params_seasonal[2],best_params_seasonal[3]),
                                enforce_stationarity=False,
                                enforce_invertibility=False)
results = mod.fit()



pred = results.get_prediction(start = 0, end = len(df_new)-1, dynamic=False)
pred_ci = pred.conf_int()
#print(pred_ci.head())


pred_ci["{}".format(key)] = (pred_ci['lower' + ' '+  "{}".format(key) ] + pred_ci['upper' + ' '+  "{}".format(key)])/2
pred_ci = pred_ci.drop(['lower' + ' '+  "{}".format(key),'upper' + ' '+  "{}".format(key)], axis=1)
pred_ci.index.name = '_time'
pred_ci["{}".format(key)] = scaler.inverse_transform(pred_ci[[f"{key}"]].values)
# print(pred_ci)

pred_ci.reset_index(inplace=True)
#print(pred_ci.head())            

new_timetz =[]
for i in range(0,len(pred_ci)):
         v = pred_ci['_time'][i].isoformat() +'Z'
         new_timetz.append(v)
        
pred_ci['_time'] = new_timetz
#print(pred_ci.head())            
            
# b = {
#     "assetId" :  "",
#     "aspectName" : "",
#     "datapoints" : pred_ci.to_dict('records')}


# FORECASTING THE FUTURE VALUES : 


datelist = pd.date_range(y.index[-1], periods = 100, freq=str(val)+str(frequency)).tolist()
df1 = pd.DataFrame({'_time': datelist})

pred_uc = results.get_forecast(steps=100)
pred_future = pred_uc.conf_int()
pred_future["{}".format(key)] = (pred_future['lower' + ' '+  "{}".format(key) ] + pred_future['upper' + ' '+  "{}".format(key)])/2
pred_future = pred_future.drop(['lower' + ' '+  "{}".format(key),'upper' + ' '+  "{}".format(key)], axis=1)
pred_future.index.name = '_time'
pred_future["{}".format(key)] = scaler.inverse_transform(pred_future[[f"{key}"]].values)
pred_future.reset_index(inplace=True)

df1["{}".format(key)] = pred_future["{}".format(key)]

new_timetz_last =[]
for i in range(0,len(df1)):
         v_last = df1['_time'][i].isoformat() +'Z'
         new_timetz_last.append(v_last)
        
df1['_time'] = new_timetz_last
df_final = pred_ci.append(df1, ignore_index=True)

b = {
    "assetId" :  "",
    "aspectName" : "",
    "datapoints" : df_final.to_dict('records')}

print(b)
    
    
    
