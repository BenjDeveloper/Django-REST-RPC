from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from app import urls as url_app

urlpatterns = [
    url(r'^', include(url_app)),
    url(r'^admin/', admin.site.urls),
    
]
