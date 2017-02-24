from django.conf.urls import include, url
from django.conf import settings

from Services.views import *

urlpatterns = [
    url(r'^service/$' ,                                                        service,               name='service'),
    url(r'^serviceTakeMaterial/(?P<bench>[\w|\W]+)/$' ,                        serviceTakeMaterial,   name='serviceTakeMaterial'),
    url(r'^serviceViewXml/(?P<user>[\w|\W]+)/$' ,                              serviceViewXml,        name='serviceViewXml'),
    url(r'^serviceReloadMaterial/(?P<bench>[\w|\W]+)/$' ,   serviceReloadMaterial, name='serviceReloadMaterial'),
    url(r'^serviceSmokePlace/(?P<user>[\w|\W]+)/$' ,                           serviceSmokePlace,     name='serviceSmokePlace'),
]