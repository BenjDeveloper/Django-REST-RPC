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
PUERTO_WEB_SERVICE = "2020"  #
HOST_WEB_SERVICE = IP_WEB_SERVICE + ":" + PUERTO_WEB_SERVICE
MATCH = PAPER = TOBACCO = "OK"
HTML_ELEMENT_XML = ''
HTML_REQUEST = ''
XML_SET = 0
USER = 'SELLER'
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

    context = { 'MATCH':MATCH ,'PAPER':PAPER, 'TOBACCO':TOBACCO , 'HTML_ELEMENT_XML':HTML_ELEMENT_XML_TEMP, 'HTML_REQUEST':HTML_REQUEST, 'VIEW_MODAL':VIEW_MODAL}
    VIEW_MODAL = False
    return render_to_response('index.html', context)


#Service 0
@csrf_exempt
def serviceView(resquest):
    global XML_SET

    if resquest.method == 'POST':
        CHOISE = resquest.POST['action']
        XML_SET = 0
        if (CHOISE == 'MATCH'):
            return HttpResponseRedirect('/serviceReloadMatch')
        if (CHOISE == 'PAPER'):
            return HttpResponseRedirect('/serviceReloadPaper')
        if (CHOISE == 'TOBACCO'):
            return HttpResponseRedirect('/serviceReloadTobacco')
        if (CHOISE == 'SMOKE'):
            return HttpResponseRedirect('/serviceSmokePlace')
        if (CHOISE == 'XML'):
            XML_SET = 1
            return HttpResponseRedirect('/serviceViewXml')
        # ---------------------------------
        if CHOISE == 'REPLICATE':
            replicate_solicitude()
        if CHOISE == 'RESTORE':
            restoreXml()
            
    return HttpResponseRedirect('/')

#Service 1
@csrf_exempt
def serviceReloadMatch(resquest):
    global MATCH
    global HTML_REQUEST

    url = 'http://' + HOST_WEB_SERVICE + '/serviceReloadMaterial/MATCH'
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
def serviceReloadPaper(resquest):
    global PAPER
    global HTML_REQUEST
    print("entro")
    url = 'http://' + HOST_WEB_SERVICE + '/serviceReloadMaterial/PAPER'
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
def serviceReloadTobacco(resquest):
    global TOBACCO
    global HTML_REQUEST

    url = 'http://' + HOST_WEB_SERVICE + '/serviceReloadMaterial/TOBACCO'
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
def serviceViewXml(resquest):
    global HTML_ELEMENT_XML
    global XML_SET 
    global USER

    url = 'http://' + HOST_WEB_SERVICE + '/serviceViewXml/'+USER
    r = requests.get(url)
    HTML_ELEMENT_XML = str(r.text)

    return HttpResponseRedirect('/')


#Service 2
def serviceAlertSeller(resquest,bench):
    global MATCH
    global PAPER
    global TOBACCO
    global HTML_REQUEST
    result = None
    print(bench)
    if bench == "MATCH":
        MATCH = "NOOK"
    
    if bench == "PAPER":
        PAPER = "NOOK"
    
    if bench == "TOBACCO":
        TOBACCO = "NOOK"

    HTML_REQUEST = HTML_REQUEST + "stock X bench X answer OK detail Server alert the seller type SERVER ALERT MATCH/" 

    result = "OK"
    return HttpResponse(result)
    
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
        msg = response.restoreXml_vendedor()
        safeFile(msg[0])
        HTML_REQUEST = HTML_REQUEST + msg[1]+"/"
        print(msg[1])
    except Exception as e:
        print(e)

def replicate_solicitude():
    try:
        response = connect_rpc.ServerProxy("http://"+IP_WEB_SERVICE+":"+PORT_COORDINATOR_SERVER+"/")
        response.replicate_coordinator_two('VOTE_COMMIT')
    except Exception as e:
        print(e)

def replicate_two(*args, **kwargs):
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
        msgXML = response.aceptar_replica_vendedor('VOTE_COMMIT')
        HTML_REQUEST = HTML_REQUEST + msgXML[1]+"/"
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
        HTML_REQUEST = HTML_REQUEST +" DUAL- VOTE_ABORT DOS /"
        response = connect_rpc.ServerProxy("http://"+IP_WEB_SERVICE+":"+PORT_COORDINATOR_SERVER+"/")
        print(response.cancelar_replica_vendedor('VOTE_ABORT'))
    except Exception as e:
        print(e)
    return HttpResponse(json.dumps(res), content_type='application/json')


def envioXML_vendedor(msg, accion=None): # Settea los atributos a string
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
    deleteXml()
    return accion

#----------------------------------------------------------------------
#----------------------------------------------------------------------
#---------------------SERVIDOR REPLICADOR DOS--------------------------
#----------------------------------------------------------------------
#----------------------------------------------------------------------

IP_REPLICATOR_TWO = '127.0.0.1' # ip del servidor replicador dos
PORT_REPLICATOR_TWO_SERVER = 3535 # puerto del replicador dos

# decorador que inicicializa el demonio de la funcion replicador dos
def thread_init(function):
    def wrapper(*args, **kwargs):
        thread = Thread(target=function, args=args, kwargs=kwargs)
        thread.daemon = True
        thread.start()
    return wrapper

@thread_init
def replicator_server_two():
    server = SimpleXMLRPCServer((IP_REPLICATOR_TWO, PORT_REPLICATOR_TWO_SERVER))
    server.register_function(replicate_two, 'replicate_two')
    server.register_function(envioXML_vendedor, 'envioXML_vendedor')
    server.register_function(respond_replicate, 'respond_replicate')
    server.register_function(deleteXml_log, 'deleteXml_log')
    server.serve_forever()

replicator_server_two()
