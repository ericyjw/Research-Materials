from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('csv_file.urls')),
    path('', include('corr_report.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

