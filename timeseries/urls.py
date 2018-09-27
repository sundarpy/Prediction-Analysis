from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import (
    handler400, handler403, handler404, handler500
)

handler400 = 'cleansdata.views.bad_request'
handler403 = 'cleansdata.views.permission_denied'
handler404 = 'cleansdata.views.page_not_found'
handler500 = 'cleansdata.views.server_error'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('cleansdata.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()