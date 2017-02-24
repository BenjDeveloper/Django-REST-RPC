from django.conf.urls import include, url
from django.conf import settings

from app.views import *

urlpatterns = [
    url(r'^$',                                          index,                 name='index' ),
    url(r'^serviceView/$' ,                             serviceView,           name='serviceView'), 
    url(r'^update_view/$' ,                             update_view,           name='update_view'), 
    url(r'^aceptar/$' ,                                 aceptar,               name='aceptar'), 
    url(r'^cancelar/$' ,                                cancelar,              name='cancelar'), 
    url(r'^serviceReloadMatch/$' ,                      serviceReloadMatch,    name='serviceReloadMatch'),
    url(r'^serviceReloadPaper/$' ,                      serviceReloadPaper,    name='serviceReloadPaper'),
    url(r'^serviceReloadTobacco/$' ,                    serviceReloadTobacco,  name='serviceReloadTobacco'),
    url(r'^serviceViewXml/$' ,                          serviceViewXml,        name='serviceViewXml'), 
    url(r'^serviceAlertSeller/(?P<bench>[\w|\W]+)/$' ,  serviceAlertSeller,    name='serviceAlertSeller'),
    
]