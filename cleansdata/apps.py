from django.apps import AppConfig


class CleansdataConfig(AppConfig):
    name = 'cleansdata'




#===================Testing===============#
# def push_data(request):
# 	data = []

# 	try:
# 		url = "http://127.0.0.1:8000/api/push_data_test/" #Local EndPoint
# 		# url = "http://AAEINBLR08922L:8080/datastore/cleanseddata" # Production Endpoint
# 		# url = "https://solarc02-djangotimeseries-solarc02.eu1.mindsphere.io/dbtest/pythoncall" # Production Endpoint
# 		payload = {
# 			"assetId" : "assetid1",
# 			"aspectName" : "aspectname1",

# 			"datapoints" : [ 
# 				{
# 				"temperature" : 40,
# 				"pressure" : 64,
# 				"_time" : "2018-08-17T06:56:22Z"
# 				}, 
# 				{
# 				"temperature" : 48,
# 				"pressure" : 47,
# 				"_time" : "2018-08-17T06:56:52Z"
# 				}, 
# 				{
# 				"temperature" : 61,
# 				"pressure" : 42,
# 				"_time" : "2018-08-17T06:57:22Z"
# 				}
# 			]
# 		}
# 		headers = {'content-type': 'application/json'}
# 		json_data = requests.post(url, data=json.dumps(payload), headers=headers)
# 		data.append(json_data)

# 		if data:
# 			response = { 'Meta': {'status' : 'Success'}, 'data' : data}	
# 		else:
# 			response = { 'Meta': {'status' : 'Failure'}, 'Failure reason' : 'Data are not Post', 'data' : data}

# 	except Exception as e:
# 		response = {'Meta': {'status': 'Failure'}, 'Failure reason': str(e)}
# 	return HttpResponse(response)



#+++++++++++++++++Correct Format+++++++++++++++++++++++++++#
# def index(request):
# 	data = datetime.now(pytz.timezone('Asia/Kolkata')).strftime("%Y-%m-%d %H:%M:%S")
# 	html = "<html><body><h5>Hello! The current Time is <b>%s</b></h5></body></html>" % data
# 	return HttpResponse(html)

# def app_get(request):
# 	url = "https://dbuitest.apps.eu1.mindsphere.io/test"
# 	# url = "http://127.0.0.1:7000/api/data/"
# 	json_data = requests.get(url)
# 	return HttpResponse(json_data)

# class Push_Details_s(APIView):
#     def post(self, request, format=None):
#         # url = "http://127.0.0.1:8000/api/push_data/"
#         url = "http://aaeinblr08922l:8080/pythoncall"
#         payload = {'temperature':'50.50505', 
#                 'distance':'50505',
#                 'motor_speed': '505050'
#                 }
#         headers = {'content-type': 'application/json'}
#         r=requests.post(url, data=json.dumps(payload), headers=headers)
#         return HttpResponse(r.text)	

# class Push_Details_E(APIView):
# 	def post(self, request, format=None):
# 		serializer = DataSetSerializer(data=request.data)
# 		if serializer.is_valid():
# 			data = serializer.save()
# 			return Response(serializer.data, status=status.HTTP_201_CREATED)
# 		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class Get_Details(APIView):
# 	def get(self, request, format=None):
# 		obj = DataSets.objects.all().order_by('-id')
# 		serializer = DataSetSerializer(obj, many=True)
# 		return Response(serializer.data)