from django.urls import path, re_path
from . import views
from django.views.generic import TemplateView
from django.views.defaults import page_not_found, server_error

urlpatterns = [
	path('', views.home, name='home'),
    path('cleansingdata/', views.cleansingdatauiview, name='cleansing-data-post-to-java'),
    path('cleansingdata/data/', views.cleansingdataview, name='receive-data'),
    path('predictiondata/', views.predictiondata, name='prediction-post-data'),
    # path('test/', views.testapi, name='for-testing-purpose'),
]
# urlpatterns += [
#     path('400/', TemplateView.as_view(template_name='400.html')),
#     path('403/', TemplateView.as_view(template_name='403.html')),
#     path('404/', page_not_found),
#     path('500/', server_error),
# ]

	