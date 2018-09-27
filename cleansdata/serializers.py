from rest_framework import serializers
from django.utils import timezone
from cleansdata.models import *
from cleansdata.views import *

class TestSerializer(serializers.ModelSerializer):
	temperature = serializers.DecimalField(max_digits=10, decimal_places=5)
	distance =serializers.IntegerField()
	motor_speed = serializers.IntegerField()
	created = serializers.DateTimeField(default=timezone.now)

	class Meta:
		model = DataPoints
		fields = ('temperature', 'distance', 'motor_speed', 'created')

class FileSerializer(serializers.ModelSerializer):
	image = serializers.ImageField(max_length=None, use_url=True)
	doc = serializers.FileField(max_length=None, use_url=True)
	created = serializers.DateTimeField(default=timezone.now)	

	class Meta:
		model = ShareFile
		fields = ('image', 'doc', 'created')


# class TestSerializer(serializers.Serializer):
# 	temperature = serializers.DecimalField(max_digits=10, decimal_places=5)
# 	distance =serializers.IntegerField()
# 	motor_speed = serializers.IntegerField()
# 	created = serializers.DateTimeField(default=timezone.now)
