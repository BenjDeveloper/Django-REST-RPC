from django.conf.urls import include, url
from django.conf import settings

from app.views import *

urlpatterns = [
    url(r'^$',                       index,                name='index' ),
    url(r'^serviceView/$' ,          serviceView,          name='serviceView'),
    url(r'^update_view/$' ,                             update_view,           name='update_view'), 
    url(r'^aceptar/$' ,                                 aceptar,               name='aceptar'), 
    url(r'^cancelar/$' ,                                cancelar,              name='cancelar'),
    url(r'^serviceTakeMatch/$' ,     serviceTakeMatch,     name='serviceTakeMatch'),
    url(r'^serviceTakePaper/$' ,     serviceTakePaper,     name='serviceTakePaper'),
    url(r'^serviceTakeTobacco/$' ,   serviceTakeTobacco,   name='serviceTakeTobacco'),
    url(r'^serviceViewXml/$' ,       serviceViewXml,       name='serviceViewXml'),
    url(r'^serviceSmokePlace/$' ,    serviceSmokePlace,    name='serviceSmokePlace'),   
]