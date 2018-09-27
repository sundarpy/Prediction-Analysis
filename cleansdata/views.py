from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseServerError, HttpResponseNotFound
from datetime import datetime
import time
import itertools
import sys, os
import pytz
import requests
import json
import re
import ast
import math
from rest_framework import status
from django.http import Http404
from rest_framework.response import Response
from .serializers import *
from requests import Request, Session
from rest_framework.decorators import api_view
from django.views.generic import View
from django.views import View
from rest_framework.views import APIView
from django.utils.decorators import method_decorator
from rest_framework import serializers

#===================DATA_LIBRARY_MODULE===============#

import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt

#===========PREDICTION-ARIMA LIBRARIES================#

# import seaborn as sns
import warnings
def ignore_warn(*args, **kwargs):
    pass
warnings.warnings = ignore_warn
import statsmodels
import statsmodels.api as sm
from statsmodels.tsa.stattools import coint, adfuller
import statsmodels.api as sm
import statistics
from statsmodels.tsa.arima_model import ARMA
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
#===========PREDICTION-PROPHET LIBRARIES================#
# from datetime import timedelta
# import fbprophet
# from datetime import timedelta
# from fbprophet.diagnostics import performance_metrics
# from fbprophet.diagnostics import cross_validation
# from scipy.special import inv_boxcox
# from scipy.stats import boxcox
# import statsmodels.api as sm 
#===========================#
import logging
logger = logging.getLogger(__name__)
#============Production View===============#

#============PROXY for Local Testing=====================#
proxyDict = { 
	"http"  : "194.138.0.62:9400",
	"https"  : "194.138.0.62:9400"
} # proxies=proxyDict

#==================HOME_PAGE======================#

def home(request):
	date_time = datetime.now(pytz.timezone('Asia/Kolkata')).strftime("%d-%m-%Y %H:%M:%S")
	return HttpResponse("Data Visualization and Prediction: " + '' + date_time)

#========================DS_PUSH_PART========================#

@api_view(['GET'])
def cleansingdataview(request): 
	assetid = request.GET.get('assetid')
	aspectname = request.GET.get('aspectname')
	q1 = request.GET.get('from')
	q2 = request.GET.get('to')
	token_value = request.META.get('HTTP_AUTHORIZATION')
	# print("Hey Your Token is: %s" %token_value)
	mind_url = "enter your URL"
	headersKey = { 'Accept' : 'application/json', 'Content-Type' : 'application/json', 'Authorization' : token_value }	
	resp = requests.get(mind_url, headers=headersKey)
	event = resp.content  # IN BYTES
	print("Response GET Value  is %s" %event)
	# logger.debug(event)
	respo = event.decode('utf-8')
	final_response = ast.literal_eval(respo)  # IN DICT
	try:
		if('status' in final_response): 
			raise ValueError("%s " %status_error)
		else:
			df = pd.DataFrame.from_records(final_response)
			if(df.isnull().values.any()==True):			
				df = df.interpolate(method='linear')
			df_normalise = df.loc[:, df.columns != '_time']				
			time = df['_time']
			idx = 0
			df_normalise.insert(loc=idx, column='_time', value = time)
			df_normalise = df_normalise.drop_duplicates()
			df_normalise = df_normalise.dropna()
			df_timestamp = df_normalise
			resp_data = {
				"assetId" :  assetid,
				"aspectName" : str(aspectname),
				"datapoints" : df_timestamp.to_dict('records')
			}

			response = {'Meta': {'status': 'Success'}, 'Data': resp_data}
			print(response)	
	except Exception as e:
		response_data = {'Meta': {'status': 'Failure'}, 'Failure reason': str(e)}
		r_data = json.dumps(response_data)
		return HttpResponseNotFound(r_data)
	return JsonResponse(response)

#=================================UI Cleansing Data=====================#

@api_view(['GET'])
def cleansingdatauiview(request):
	assetid = request.GET.get('assetid')
	aspectname = request.GET.get('aspectname')
	q1 = request.GET.get('from')
	q2 = request.GET.get('to')
	token_value = request.META.get('HTTP_AUTHORIZATION')
	# logger.INFO(token_value)
	mind_url = "enter your URL"
	headersKey = { 'Accept' : 'application/json', 'Content-Type' : 'application/json', 'Authorization' : token_value }	
	resp = requests.get(mind_url, headers=headersKey)
	event = resp.content  # IN BYTES
	print("Response POST Value  is %s" %event)
	respo = event.decode('utf-8')
	final_response = ast.literal_eval(respo)  # IN DICT
	try:
		if('status' in final_response): 
			raise ValueError("%s " %final_response)					
		else:
			df = pd.DataFrame.from_records(final_response)
			if(df.isnull().values.any()==True):			
				df = df.interpolate(method='linear')
			df_normalise = df.loc[:, df.columns != '_time']				
			time = df['_time']
			idx = 0
			df_normalise.insert(loc=idx, column='_time', value = time)
			df_normalise = df_normalise.drop_duplicates()
			df_normalise = df_normalise.dropna()
			df_timestamp = df_normalise
			share_data = {
				"assetId" :  assetid,
				"aspectName" : str(aspectname),
				"datapoints" : df_timestamp.to_dict('records')
			}
			print("SHARE DATA IS : %s" %share_data)
			url = 'https://visualsvc.apps.eu1.mindsphere.io/datastore/cleanseddata'				
			headers = { 'Accept' : 'application/json', 'Content-Type' : 'application/json'}
			response_post = requests.post(url, json = share_data, headers=headers)
			response = response_post
			print("Response POST status  is %s" %response)
	except Exception as e:
		response_data = {'Meta': {'status': 'Failure'}, 'Failure reason': str(e)}
		r_data = json.dumps(response_data)
		return HttpResponseServerError(r_data)
	return HttpResponse(response)

#========================Prediction Data Arima Model=========================#

# @api_view(['POST']) # Previous code
# def predictiondata(request):
# 	key = request.GET.get('key')
# 	try:
# 		r_data = json.loads(request.body)
# 		print("Prediction Get KEY: %s" %key)
# 		print("RAW DATA %s" %r_data)
# 		df_cleaned = pd.DataFrame(r_data)
# 		print("Clean Data is %s" %df_cleaned)
# 		df_timestamp = df_cleaned.copy()
# 		df_timestamp["{}".format(key)]= np.log1p(df_timestamp[f"{key}"].values)
# 		df_new =  df_timestamp[['_time',"{}".format(key)]]
# 		df_new.set_index('_time',inplace=True)

# 		date_sale = df_new.copy()
# 		date_sale.index = pd.to_datetime(date_sale.index)
# 		y = date_sale

# 		print("Y is %s" %y)
# 		p = d = q = range(0, 2)
# 		pdq = list(itertools.product(p, d, q))
# 		seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]

# 		cnt = 0
# 		stop = 0
# 		AIC = float('inf')
# 		for param in pdq:
# 			for param_seasonal in seasonal_pdq:
# 				try:
# 					mod = sm.tsa.statespace.SARIMAX(
# 							y,
# 							order=param,
# 							seasonal_order=param_seasonal,
# 							enforce_stationarity=False,
# 							enforce_invertibility=False
# 							)
# 					results = mod.fit()
# 					if results.aic < AIC and stop < 50:
# 						AIC = results.aic
# 						best_params = param
# 						best_params_seasonal = param_seasonal
# 						stop+=1
# 				except Exception as e:
# 					continue
# 		mod = sm.tsa.statespace.SARIMAX(y,
#                                 order=(best_params[0],best_params[1],best_params[2]),
#                                 seasonal_order=(best_params_seasonal[0],best_params_seasonal[1],best_params_seasonal[2],best_params_seasonal[3]),
#                                 enforce_stationarity=False,
#                                 enforce_invertibility=False)
# 		results = mod.fit()
# 		pred = results.get_prediction(start = 0, end = 200, dynamic=False)
# 		pred_ci = pred.conf_int()
# 		pred_ci["{}".format(key)] = (pred_ci['lower' + ' '+  "{}".format(key) ] + pred_ci['upper' + ' '+  "{}".format(key)])/2
# 		pred_ci = pred_ci.drop(['lower' + ' '+  "{}".format(key),'upper' + ' '+  "{}".format(key)], axis=1)
# 		pred_ci.index.name = '_time'
# 		pred_ci["{}".format(key)] = np.exp(pred_ci[f"{key}"].values)

# 		pred_ci.reset_index(inplace=True)
# 		#print("predi_ci is %s" %pred_ci)
# 		new_timetz =[]
# 		for i in range(0,len(pred_ci)):
# 			v = pred_ci['_time'][i].isoformat() +'Z'
# 			new_timetz.append(v)
# 		pred_ci['_time'] = new_timetz

# 		print("predi_ci is %s" %pred_ci)

# 		prediction_data = {
# 			"assetId" :  "",
# 			"aspectName" : "",
# 			"datapoints" : pred_ci.to_dict('records')
# 		}

# 		response = prediction_data
# 		print("Prediction data is: %s" %prediction_data)
# 	except Exception as e:
# 		response = {'Meta': {'status': 'Failure'}, 'Failure reason': str(e)}
# 	return JsonResponse(response)		

#===================================New ARIMA Prediction=======================#

@api_view(['POST'])
def predictiondata(request):
	key = request.GET.get('key')
	try:
		r_data = json.loads(request.body)
		print("Prediction Get KEY: %s" %key)
		print("RAW DATA %s" %r_data)
		df_cleaned = pd.DataFrame(r_data)
		print("Clean Data is %s" %df_cleaned)
		df_timestamp = df_cleaned.copy()
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
		elif(delta[2] == 7):
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

		prediction_data = {
		    "assetId" :  "",
		    "aspectName" : "",
		    "datapoints" : df_final.to_dict('records')}

		response = prediction_data
		print("Prediction data is: %s" %prediction_data)
	except Exception as e:
		response = {'Meta': {'status': 'Failure'}, 'Failure reason': str(e)}
	return JsonResponse(response)

#========================Prediction Data Prophet Model=========================#

# @api_view(['POST'])
# def predictiondata(request, slug):
# 	try:
# 		r_data = json.loads(request.body)
# 		# data = json.loads()
# 		df_cleaned = pd.DataFrame(r_data)
# 		df_cleaned["{}".format(key)], lam = boxcox(df_cleaned["{}".format(key)])
# 		data_clean = df_cleaned[['_time',"{}".format(key)]]
# 		data_clean['_time'] = pd.to_datetime(data_clean['_time'])
# 		df_check = data_clean.copy()
# 		df_check.reset_index(inplace=True)
# 		df_check = df_check.rename(columns={'_time':'ds', "{}".format(key):'y'})
# 		dates = pd.Index(pd.DatetimeIndex(df_check['ds']))
# 		s = pd.Series(df_check['y'].values, dates)
# 		t1 = str(df_check['ds'][0])
# 		t2 = str(df_check['ds'][1])
# 		x= re.split('[-: ]', t1)
# 		y = (re.split('[-: ]', t2))
# 		old = list(map(int, x))
# 		new = list(map(int, y))
# 		delta = [a - b for a, b in zip(new,old)]
# 		if(delta[0]==1):
# 			frequency = 'A'
# 		elif(delta[1]==1):
# 			frequency = 'M'
# 		elif(delta[2]==1):
# 			frequency = 'D'
# 		elif(delta[3]==1):
# 			frequency = 'H'
# 		elif(delta[4]==1):
# 			frequency = 'T'
# 		elif(delta[5]==1):
# 			frequency = 'S'
# 		elif(delta[2]>=6):
# 			frequency = 'W'   

# 		s = (s.asfreq("{}".format(frequency)))
# 		if(s.isnull().values.any()==True):
# 			s = s.interpolate()
	        
# 		model = fbprophet.Prophet()

# 		model.fit(df_check)
# 		df_forecast = model.make_future_dataframe(periods =100, freq="{}".format(frequency))  #"{}".format(frequency)
# 		df_forecast = model.predict(df_forecast)

# 		df_predict = df_forecast[['ds','yhat']]

# 		# tz format conversion
# 		new_timetz =[]
# 		for i in range(0,len(df_predict)):
# 			v = df_predict['ds'][i].isoformat() +'Z'
# 			new_timetz.append(v)
	            
# 		df_predict['ds'] = new_timetz 

# 		df_predict = df_predict.rename(columns={'ds': '_time', 'yhat':"{}".format(key)})

# 		df_predict[["{}".format(key)]] = df_predict[["{}".format(key)]].apply(lambda x: inv_boxcox(x, lam))



# 		b = {
# 	    	"assetId" :  "",
# 	    	"aspectName" : "",
# 	    	"datapoints" : df_predict.to_dict('records')
# 	    }
# 		response = json.dumps(b)
# 	except Exception as e:
# 		response = "Caught this Error: " + ' ' + str(e)
# 	return HttpResponse(response)

#=========================TESTING PURPOSE=============================#
# def testapi(request):
# 	data = []
# 	try:
# 		test_data = {
# 			"Hello": "Hey",
# 			"Hey": "Hello",
# 		}
# 		response = test_datas
# 	except Exception as e:
# 		response = {'Meta': {'status': 'Failure'}, 'Failure reason': str(e)}
# 	return JsonResponse(response)
