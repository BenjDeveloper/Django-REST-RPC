import sys
import os
import json
import random
import requests
from django.core import serializers
from django.http import Http404, HttpResponseRedirect , HttpResponse
from django.contrib.auth.models import User, Permission, Group
from django.shortcuts import render, render_to_response
from django.template import RequestContext, Context
from django.template.loader import get_template
from datetime import datetime, timedelta
from app.util import *
from django.views.decorators.csrf import csrf_exempt
import xmlrpc.client as connect_rpc # new
from threading import Thread# new
from xmlrpc.server import SimpleXMLRPCServer # new

# Variables Globales
IP_WEB_SERVICE = "127.0.0.1" #
PUERTO_WEB_SERVICE = "2020"  # puerto del servidor web 
HOST_WEB_SERVICE = IP_WEB_SERVICE + ":" + PUERTO_WEB_SERVICE
MATCH = PAPER = TOBACCO = "NOOK"
HTML_ELEMENT_XML = ''
HTML_REQUEST = ''
XML_SET = 0
USER = 'SMOKER_1'
VIEW_MODAL = False


# Create your views here.
def index(request):
    global MATCH
    global PAPER
    global TOBACCO
    global HTML_REQUEST
    global HTML_ELEMENT_XML
    global VIEW_MODAL
    HTML_ELEMENT_XML_TEMP = ''
    
    if XML_SET == 1 :
        HTML_ELEMENT_XML_TEMP = HTML_ELEMENT_XML

    context = { 'MATCH':MATCH ,'PAPER':PAPER, 'TOBACCO':TOBACCO , 'HTML_ELEMENT_XML':HTML_ELEMENT_XML_TEMP, 'HTML_REQUEST':HTML_REQUEST}
    return render_to_response('index.html', context)


#Service 0
@csrf_exempt
def serviceView(resquest):
    global XML_SET

    if resquest.method == 'POST':
        CHOISE = resquest.POST['action']
        XML_SET = 0
        if (CHOISE == 'MATCH'):
            return HttpResponseRedirect('/serviceTakeMatch')
        if (CHOISE == 'PAPER'):
            return HttpResponseRedirect('/serviceTakePaper')
        if (CHOISE == 'TOBACCO'):
            return HttpResponseRedirect('/serviceTakeTobacco')
        if (CHOISE == 'SMOKE'):
            return HttpResponseRedirect('/serviceSmokePlace')
        if (CHOISE == 'XML'):
            XML_SET = 1
            return HttpResponseRedirect('/serviceViewXml')
        # ---------------------------------
        if CHOISE == 'REPLICATE':
            replicate_one()
        if CHOISE == 'RESTORE':
            restoreXml()

    return HttpResponseRedirect('/')

#Service 1
@csrf_exempt
def serviceTakeMatch(resquest):
    global MATCH
    global HTML_REQUEST

    url = 'http://' + HOST_WEB_SERVICE + '/serviceTakeMaterial/MATCH'
    r = requests.get(url)
    json_data = json.loads(r.text)
    for key, value in json_data.items():
        val = value[0]
        lista = val[0]
        for k, v in lista.items():
            if (v == 'OK'): 
                MATCH = 'OK'
            HTML_REQUEST = HTML_REQUEST +" "+ k +" "+ v 
    HTML_REQUEST = HTML_REQUEST +"/"
    return HttpResponseRedirect('/')


#Service 1
@csrf_exempt
def serviceTakePaper(resquest):
    global PAPER
    global HTML_REQUEST
    print('entro')
    url = 'http://' + HOST_WEB_SERVICE + '/serviceTakeMaterial/PAPER'
    r = requests.get(url)
    json_data = json.loads(r.text)
    for key, value in json_data.items():
        val = value[0]
        lista = val[0]
        for k, v in lista.items():
            if (v == 'OK'): 
                PAPER = 'OK'
            HTML_REQUEST = HTML_REQUEST +" "+ k +" "+ v 
    HTML_REQUEST = HTML_REQUEST +"/"
    return HttpResponseRedirect('/')

#Service 1
@csrf_exempt
def serviceTakeTobacco(resquest):
    global TOBACCO
    global HTML_REQUEST

    url = 'http://' + HOST_WEB_SERVICE + '/serviceTakeMaterial/TOBACCO'
    r = requests.get(url)
    json_data = json.loads(r.text)
    for key, value in json_data.items():
        val = value[0]
        lista = val[0]
        for k, v in lista.items():
            if (v == 'OK'): 
                TOBACCO = 'OK'
            HTML_REQUEST = HTML_REQUEST +" "+ k +" "+ v 
    HTML_REQUEST = HTML_REQUEST +"/"
    return HttpResponseRedirect('/')

#Service 2
@csrf_exempt
def serviceSmokePlace(resquest):
    global MATCH 
    global PAPER
    global TOBACCO
    global HTML_REQUEST
    global USER

    if (MATCH == 'OK' and PAPER == 'OK' and TOBACCO == 'OK'):
        MATCH = PAPER = TOBACCO = "NOOK"
        url = 'http://' + HOST_WEB_SERVICE + '/serviceSmokePlace/'+USER
        requests.get(url)
        HTML_REQUEST = HTML_REQUEST + "stock X bench X answer OK detail succefull type SMOKER-PLACE/" 
    return HttpResponseRedirect('/')
        

#Service 3
def serviceViewXml(resquest):
    global HTML_ELEMENT_XML
    global XML_SET 
    global USER

    url = 'http://' + HOST_WEB_SERVICE + '/serviceViewXml/'+USER
    r = requests.get(url)
    HTML_ELEMENT_XML = str(r.text)

    return HttpResponseRedirect('/')

#----------------------------------------------------------------------
#----------------------------------------------------------------------
#----------------METODOS COMUNICACION CON EL COORDINADOR---------------
#----------------------------------------------------------------------
#----------------------------------------------------------------------

PORT_COORDINATOR_SERVER = '2525' # puerto del servidor coordinador

def restoreXml():
    global HTML_REQUEST
    try:
        response = connect_rpc.ServerProxy("http://"+IP_WEB_SERVICE+":"+PORT_COORDINATOR_SERVER+"/")
        msg = response.restoreXml_fumador()
        safeFile(msg[0])
        HTML_REQUEST = HTML_REQUEST + msg[1]+"/"
        print(msg[1])
    except Exception as e:
        print(e)

def replicate_one():
    try:
        response = connect_rpc.ServerProxy("http://"+IP_WEB_SERVICE+":"+PORT_COORDINATOR_SERVER+"/")
        response.replicate_coordinator('VOTE_COMMIT')
    except Exception as e:
        print(e)

def replicate_accept_one(*args, **kwargs):
    global VIEW_MODAL
    print(args[0])
    
    if args[0] == 'VOTE_COMMIT':
        VIEW_MODAL = True
        print('VIEW_MODAL')
    else:
         VIEW_MODAL = False
    
    return True 

@csrf_exempt
def update_view(request):
    global VIEW_MODAL
    response = {}
    response['VIEW_MODAL'] = VIEW_MODAL
    return HttpResponse(json.dumps(response), content_type='application/json')


def aceptar(request):
    global VIEW_MODAL
    global HTML_REQUEST
    VIEW_MODAL = False
    res = {}
    res['bool'] = VIEW_MODAL
    try:
        response = connect_rpc.ServerProxy("http://"+IP_WEB_SERVICE+":"+PORT_COORDINATOR_SERVER+"/")
        msgXML = response.aceptar_replica_fumador('VOTE_COMMIT')
        HTML_REQUEST = HTML_REQUEST + msgXML[1]+"- GLOBAL_REPLICA /"
        safeFile(msgXML[0])
    except Exception as e:
        print(e)
    return HttpResponse(json.dumps(res), content_type='application/json')

def cancelar(request):
    global VIEW_MODAL
    global HTML_REQUEST
    VIEW_MODAL = False
    res = {}
    res['bool'] = VIEW_MODAL
    try:
        HTML_REQUEST = HTML_REQUEST +" DUAL - VOTE_ABORT UNO /"
        response = connect_rpc.ServerProxy("http://"+IP_WEB_SERVICE+":"+PORT_COORDINATOR_SERVER+"/")
        response.cancelar_replica_fumador('VOTE_ABORT')
    except Exception as e:
        print(e)
    return HttpResponse(json.dumps(res), content_type='application/json')

def envioXML_fumador(msg, accion=None): # Settea los atributos a string
    global HTML_REQUEST
    HTML_REQUEST = HTML_REQUEST + accion+"/"
    safeFile(msg)
    print(msg)
    print(accion)
    return msg

def respond_replicate(accion=None): # Settea los atributos a string
    global HTML_REQUEST
    HTML_REQUEST = HTML_REQUEST + accion + "/"
    print(accion)
    return msg

def deleteXml_log(accion=None): # Settea los atributos a string
    print(accion)
    print("ANTES")
    deleteXml()
    print("DESPUES")
    return accion


#----------------------------------------------------------------------
#----------------------------------------------------------------------
#---------------------SERVIDOR REPLICADOR UNO--------------------------
#----------------------------------------------------------------------
#----------------------------------------------------------------------

IP_REPLICATOR_ONE = '127.0.0.1' # ip del servidor replicador uno
PORT_REPLICATOR_ONE_SERVER = 1515 # puerto del replicador uno

# decorador que inicicializa el demonio de la funcion replicador uno
def thread_init(function):
    def wrapper(*args, **kwargs):
        thread = Thread(target=function, args=args, kwargs=kwargs)
        thread.daemon = True
        thread.start()
    return wrapper

@thread_init
def replicator_server_one():
    server = SimpleXMLRPCServer((IP_REPLICATOR_ONE, PORT_REPLICATOR_ONE_SERVER))
    server.register_function(replicate_accept_one, 'replicate_accept_one')
    server.register_function(envioXML_fumador, 'envioXML_fumador')
    server.register_function(deleteXml_log, 'deleteXml_log')
    server.serve_forever()

replicator_server_one()

