from django.db import models
from django.utils import timezone

class DataPoints(models.Model):
	temperature = models.FloatField(default=None)
	distance = models.IntegerField(default=None)
	motor_speed = models.IntegerField(default=None)
	created = models.DateTimeField(default=timezone.now)

	class Meta:
		app_label = 'cleansdata'


class ShareFile(models.Model):
	image = models.ImageField(upload_to='Images/', default='Images/None/No-img.jpg')
	doc = models.FileField(upload_to='Doc/', default='Doc/None/No-doc.pdf')
	class Meta:
		app_label = 'cleansdata'	