# from django.shortcuts import render
# from django.http import HttpResponse, JsonResponse
# from datetime import datetime
# import pytz
# import requests
# import json
# from rest_framework import status
# from django.http import Http404
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from .serializers import *

# from django.views.decorators.csrf import csrf_exempt

#================SET LOGGER FILE=================#
# import logging

# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)

# formatter = logging.Formatter('%(levelname)s:%(asctime)s:%(name)s:%(message)s')

# file_handler = logging.FileHandler('info.log')
# # file_handler.setLevel(logging.INFO)
# file_handler.setFormatter(formatter)

# logger.addHandler(file_handler)

# logging.basicConfig(filename='info.log', level=logging.DEBUG, format='%(levelname)s:%(name)s:%(message)s')
#============Production View===============#

# def home(request):
# 	data = datetime.now(pytz.timezone('Asia/Kolkata')).strftime("%d-%m-%Y %H:%M:%S")
# 	html = "<html><body><h5>Hello DateTime <b>%s</b></h5><p>Get Endpoint Extension is <b>/api/receive</b></p> <p>Post Endpoint Extension is <b>/api/send</b></p></body></html>" % data
# 	url = "https://solarc02-djangotimeseries-solarc02.eu1.mindsphere.io/dbtest/test"
# 	json_data = requests.get(url)
# 	# json_data.text
# 	return HttpResponse(json_data)
#============Local Test Endpoints==================#

# with open('dummy.json') as f:
# 	data = json.load(f)

# # print(data)	
# for temp in data['list']:
# 	del temp['main']['temp_kf']

# with open('dummy_one.json', 'w') as f:
# 	json.dump(data, f, indent=2)
# '%', % data
# url = "https://samples.openweathermap.org/data/2.5/forecast?zip=94040&appid=b6907d289e10d714a6e88b30761fae22'"
# test = requests.get(url)
# print(test.json())
# with open('testapp.json', 'w') as f:
# 	json.dump(test, f, indent=2)


#========================================# 
#Test case#

# @api_view(["POST"])
# def IdealWeight(heightdata):
#     try:
#         height=json.loads(heightdata.body)
#         weight=str(height*10)
#         return JsonResponse("Ideal weight should be:"+weight+" kg",safe=False)
#     except ValueError as e:
#         return Response(e.args[0],status.HTTP_400_BAD_REQUEST)       

#=============================================#

#==================Production Got Passed==========#

# def home(request):
# 	date_time = datetime.now(pytz.timezone('Asia/Kolkata')).strftime("%d-%m-%Y %H:%M:%S")
# 	return HttpResponse("Hello Test App: " + '' + date_time)

# #===================FBV_GET_RESPONSE=====================#

# @api_view(['GET'])
# def receive(request):
# 	try:
# 		GetDataUrl = 'https://dbuitest.apps.eu1.mindsphere.io/dbtest/test'
# 		headers = { 'Accept' : 'application/json', 'Content-Type' : 'application/json','Authorization': 'Basic'}
# 		receive_data = requests.get(GetDataUrl, headers=headers) #, proxies=proxyDict
# 	except Exception as e:
# 		receive_data = "Caught this Error: " + ' ' + str(e)
# 	return HttpResponse(receive_data)

# #=================FBV_POST_RESPONSE====================#

# @api_view(['GET'])
# def push_data(request):
# 	try:
# 		# j_data = json.loads(request.body)
# 		# url = "http://aaeinblr08922l:8080/dbtest/pythoncall"
# 		data = {
# 			'ids': [12, 3, 4, 5, 6]
# 		}
# 		url = 'https://dbuitest.apps.eu1.mindsphere.io/dbtest/pythoncall'				
# 		headers = { 'Accept' : 'application/json', 'Content-Type' : 'application/json','Authorization': 'Basic'}
# 		request_data = requests.post(url, json = json.dumps(data), headers=headers)
# 	except Exception as e:
# 		request_data = "Caught this Error: " + ' ' + str(e)
# 	return HttpResponse(request_data)	

# #========================CBV_GET_RESPONSE========================#

# class TestApi(APIView):
# 	# To turn off CSRF validation (not recommended in production)
# 	@method_decorator(csrf_exempt)
# 	def dispatch(self, request, *args, **kwargs):
# 		return super(TestApi, self).dispatch(request, *args, **kwargs)

# 	def get(self, request):
# 		try:
# 			# url = 'https://solarc02-djangotimeseries-solarc02.eu1.mindsphere.io/dbtest/test'
# 			url = 'https://dbuitest.apps.eu1.mindsphere.io/dbtest/test'
# 			headers = { 'Accept' : 'application/json', 'Content-Type' : 'application/json','Authorization': 'Basic'}
# 			resp_data = requests.get(url, headers=headers)
# 		except Exception as e:
# 			resp_data = "Caught some Error Here: " + ' ' + str(e)
# 		return HttpResponse(resp_data) 

# #=====================CBV_POST_RESPONSE===========================#
# class TestApiPost(APIView):
# 	# To turn off CSRF validation (not recommended in production)
# 	@method_decorator(csrf_exempt)
# 	def dispatch(self, request, *args, **kwargs):
# 		return super(TestApiPost, self).dispatch(request, *args, **kwargs)

# 	def get(self, request):
# 		try:
# 			url = 'https://dbuitest.apps.eu1.mindsphere.io/dbtest/pythoncall'
# 			payload = {
# 				"assetId" : "assetid111",
# 				"aspectName" : "aspectname111",

# 				"datapoints" : [ 
# 					{
# 					"temperature" : 40,
# 					"pressure" : 64,
# 					"_time" : "2018-08-17T06:56:22Z"
# 					}, 
# 					{
# 					"temperature" : 48,
# 					"pressure" : 47,
# 					"_time" : "2018-08-17T06:56:52Z"
# 					}, 
# 					{
# 					"temperature" : 61,
# 					"pressure" : 42,
# 					"_time" : "2018-08-17T06:57:22Z"
# 					}
# 				]
# 			}
# 			headers = { 'Accept' : 'application/json', 'Content-Type' : 'application/json','Authorization': 'Basic'}
# 			post_data = requests.post(url, json=json.dumps(payload), headers=headers)
# 			return JsonResponse({"created": post_data}, safe=False)
# 		except:
# 			return JsonResponse({"error": "not a valid data"}, safe=False)

# #==================LOCAL TEST PURPOSE===================#

# # @api_view(['POST'])
# # def push_data(request):
# # 	try:
# # 		j_data = json.loads(request.body)
# # 		PostDataUrl ='https://dbuitest-solarc02.apps.eu1.mindsphere.io/dbtest/pythoncall'
# # 		request_data = requests.post(PostDataUrl, json=j_data)
# # 	except Exception as e:
# # 		request_data = "Caught this Error: " + ' ' + str(e)
# # 	return HttpResponse(request_data)	

#==================Production Got Passed==========#
	# def get(self, request):
	# 	serializer_data = DataPoints.objects.all()
	# 	serializer = TestSerializer(serializer_data, many=True)
	# 	return Response(serializer.data)


#============================Date is working Now from and to============================#

# path('cleansingdata/<slug:assetid>/<slug:aspectname>/<int:year>/<slug:day>/<slug:slug>/<slug:ho>/<slug:mi>/<int:yearo>/<slug:dayo>/<slug:slugo>/<slug:hoo>/<slug:mio>', views.cleansingdatauiview, name='test-ui-data'),

# @api_view(['GET'])
# def cleansingdatauiview(request, assetid, aspectname, year, day, slug, ho, mi, yearo, dayo, slugo, hoo, mio):
# 	token_value = request.META.get('HTTP_AUTHORIZATION')
# 	mind_url = "https://gateway.eu1.mindsphere.io/api/iottimeseries/v3/timeseries/'{}'/'{}'/?from='{}'-'{}'-'{}':'{}':'{}'&to='{}'-'{}'-'{}':'{}':'{}'".format(assetid, aspectname, year, day, slug, ho, mi, yearo, dayo, slugo, hoo, mio).replace("'", "")
# 	headersKey = { 'Accept' : 'application/json', 'Content-Type' : 'application/json', 'Authorization' : token_value }	
# 	resp = requests.get(mind_url, headers=headersKey)
# 	event = resp.content  # IN BYTES
# 	print("Response Value  is %s" %event)
# 	respo = event.decode('utf-8')
# 	final_response = ast.literal_eval(respo)  # IN DICT
# 	try:
# 		if('status' in final_response): 
# 			status_error = {"status":final_response['status'],"error":final_response['error'],"message":final_response['message']}
# 			response = "This is not a valid data!"			
# 		else:
# 			df = pd.DataFrame.from_records(final_response)
# 			if(df.isnull().values.any()==True):			
# 				df = df.interpolate(method='linear')
# 			df_normalise = df.loc[:, df.columns != '_time']				
# 			time = df['_time']
# 			idx = 0
# 			df_normalise.insert(loc=idx, column='_time', value = time)
# 			df_normalise = df_normalise.drop_duplicates()
# 			df_normalise = df_normalise.dropna()
# 			df_timestamp = df_normalise
# 			a = {
# 				"assetId" :  assetid,
# 				"aspectName" : str(aspectname),
# 				"datapoints" : df_timestamp.to_dict('records')
# 			}

# 			cleans_data = json.dumps(a) #  DATA RETURN AFTE CLEANSING
# 			# url = 'https://dbuitest.apps.eu1.mindsphere.io/dbtest/pythoncall'				
# 			# headers = { 'Accept' : 'application/json', 'Content-Type' : 'application/json','Authorization': 'Basic'}
# 			# request_data = requests.post(url, json = json.dumps(a), headers=headers)				
# 			response = cleans_data
# 	except Exception as e:
# 		response = "Caught this Error : >>" + ' ' + str(e)
# 	return HttpResponse(response)




#============================Logger Setting File============================#
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': True,
#     'formatters': {
#         'standard': {
#             'format': '%(asctime)s [%(levelname)s] : %(name)s : %(message)s'
#         }
#     },
#     'handlers': {
#         'default': {
#             'level': 'DEBUG',
#             'class': 'logging.handlers.RotatingFileHandler',
#             'filename': 'logs/mylog.log',
#             # 'maxBytes': 1024*1024*5, # 5MB
#             'formatter': 'standard',
#         }
#     },
#     'request_handler': {
#         'level': 'DEBUG',
#         'class': 'logging.handlers.RotatingFileHandler',
#         'filename': 'logs/django_request.log',
#         'formatter': 'standard',
#     },
#     'loggers': {
#         '': {
#             'handlers': ['default'],
#             'level': 'DEBUG',
#             'propagate': True,
#         },
#         'django.request': {
#             'handlers': ['request_handler'],
#             'level': 'DEBUG',
#             'propagate': False,
#         },
#     }
# }

# index_log = os.path.join(BASE_DIR, '/timeseries/logs')