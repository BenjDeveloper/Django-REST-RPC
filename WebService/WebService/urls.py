from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from Services import urls as url_services

urlpatterns = [
    url(r'^', include(url_services)),
    url(r'^admin/', admin.site.urls),
    
]
