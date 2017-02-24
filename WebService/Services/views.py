import sys
import os
import json
import random
import time
import requests
from django.core import serializers
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render
from datetime import datetime
from Services.domain import *
from Services.util import *
import xml.etree.cElementTree as Xml
from threading import Thread # new
from xmlrpc.server import SimpleXMLRPCServer # new
import xmlrpc.client as connect_rpc # new


# Variables Globales
IP_SELLER = "127.0.0.1" #
PUERTO_SELLER = "3030"  # puerto servidor web del vendedor
HOST_SELLER = IP_SELLER + ":" + PUERTO_SELLER
TIMER_DEFAULD = 5 #............................. delays for 'n' seconds
SIZE_ORDER = 2
BENCH_MATCH = Bench()
BENCH_PAPER = Bench()
BENCH_TOBACCO = Bench()
FLAG_LOG = 0
#BANDERAS
REPLICADOR_1_SOLICITO = False
REPLICADOR_2_ACEPTO = False


#Carga de ingredientes iniciales del servidor

BENCH_MATCH._stock = Bench.iniBench(random.randint(1, SIZE_ORDER),"MATCH")

BENCH_PAPER._stock = Bench.iniBench(random.randint(1, SIZE_ORDER),"PAPER")

BENCH_TOBACCO._stock = Bench.iniBench(random.randint(1, SIZE_ORDER),"TOBACCO")



#Service 0
def service(resquest):
    result = None
    datos = []
    diccionario = []
    datos = { "prueba" : PATH_LOG}
    diccionario.append(datos)
    result = json.dumps(diccionario)
    return HttpResponse(result)


#Service 1
def serviceTakeMaterial(resquest,bench):
    result = "NOOK"
    result_detail = "detalles de la respuesta"
    datos = []
    diccionario = []
    bilioteca = []
    global BENCH_MATCH
    global BENCH_PAPER
    global BENCH_TOBACCO
    global FLAG_LOG

    #BENCH OF MATCH 
    if (bench == "MATCH"): 
        if (BENCH_MATCH._flag == 0):
            BENCH_MATCH._flag = 1  # REGION CRITICA

            if (len(BENCH_MATCH._stock) > 0 ):
                BENCH_MATCH._stock.pop()
                time.sleep(TIMER_DEFAULD)
                result = "OK"
                result_detail = "succefull"

            else:
                result_detail = serviceAlertSeller(bench)
                result_detail = "empty, try later"

            BENCH_MATCH._flag = 0  # REGION CRITICA
        else:
            result_detail = "busy, try later"   

    #BENCH OF PAPER
    if (bench == "PAPER"):
        if (BENCH_PAPER._flag == 0):
            BENCH_PAPER._flag = 1  # REGION CRITICA

            if (len(BENCH_PAPER._stock) > 0 ):
                BENCH_PAPER._stock.pop()
                time.sleep(TIMER_DEFAULD)
                result = "OK"
                result_detail = "succefull" 

            else:
                result_detail = serviceAlertSeller(bench)
                result_detail = "empty, try later" 

            BENCH_PAPER._flag = 0  # REGION CRITICA
        else:
            result_detail = "busy, try later"   

    #BENCH OF TOBACO
    if (bench == "TOBACCO"): 
        if (BENCH_TOBACCO._flag == 0):
            BENCH_TOBACCO._flag = 1  # REGION CRITICA
            if (len(BENCH_TOBACCO._stock) > 0 ):
                BENCH_TOBACCO._stock.pop()
                time.sleep(TIMER_DEFAULD)
                result = "OK"
                result_detail = "succefull"  

            else:
                result_detail = serviceAlertSeller(bench)
                result_detail = "empty, try later"

            BENCH_TOBACCO._flag = 0   # REGION CRITICA
        else:
            result_detail = "busy, try later"  
    
    datos = {   "type" : "SEARCH",
               "bench" : bench,
              "answer" : result,
              "detail" : result_detail, 
               "stock" : "MATCH=" + str(len(BENCH_MATCH._stock)) + "  PAPER=" +str(len(BENCH_PAPER._stock)) + " TOBACCO=" +str(len(BENCH_TOBACCO._stock))}
    diccionario.append(datos)
    bilioteca = {"event":[diccionario]}
    whiteXml(datos)

    result = json.dumps(bilioteca)
    return HttpResponse(result)


#Service 2
def serviceViewXml(resquest,user):
    global FLAG_LOG
    result = "NOOK"
    datos = []

    datos = {   "type" : user+"-XML",
               "bench" : "",
              "answer" : "OK",
              "detail" : user + " requesting Xml", 
               "stock" : "",}
    whiteXml(datos)
    root = loadFile()

    result = str(root)
    return HttpResponse(result)


#Service 3
def serviceReloadMaterial(resquest):
    result = None
    datos = []
    diccionario = []
    datos = {   "name" : "Web Service",
                "tipo" : "REPONER",
                "action" : "Reponer Materiales de la mesa" }
    diccionario.append(datos)
    result = json.dumps(diccionario)

    return HttpResponse(result)

#Service 4
def serviceSmokePlace(resquest,user):
    global FLAG_LOG
    result = "NOOK"
    datos = []
    diccionario = []
    bilioteca = []
    datos = {   "type" : "SMOKE PLACE",
               "bench" : "None",
              "answer" : "OK",
              "detail" : user+" smoking", 
               "stock" : "",}
    diccionario.append(datos)
    bilioteca = {"event":[diccionario]}
    time.sleep(TIMER_DEFAULD)
    whiteXml(datos)
    
    result = json.dumps(bilioteca)
    return HttpResponse(result)


#Service 5
def serviceReloadMaterial(resquest,bench):
    result = "NOOK"
    result_detail = "detalles de la respuesta"
    datos = []
    diccionario = []
    bilioteca = []
    global BENCH_MATCH
    global BENCH_PAPER
    global BENCH_TOBACCO
    global FLAG_LOG
    global SIZE_ORDER

    #BENCH OF MATCH 
    if (bench == "MATCH"): 
        if (BENCH_MATCH._flag == 0):
            BENCH_MATCH._flag = 1  # REGION CRITICA

            BENCH_MATCH._stock = Bench.iniBench(SIZE_ORDER,bench)
            time.sleep(TIMER_DEFAULD)
            result = "OK"
            result_detail = "succefull"
            print(len(BENCH_MATCH._stock))
            BENCH_MATCH._flag = 0  # REGION CRITICA
        else:
            result_detail = "busy, try later"   

    #BENCH OF PAPER
    if (bench == "PAPER"):
        if (BENCH_PAPER._flag == 0):
            BENCH_PAPER._flag = 1  # REGION CRITICA

            BENCH_PAPER._stock = Bench.iniBench(SIZE_ORDER,bench)
            time.sleep(TIMER_DEFAULD)
            result = "OK"
            result_detail = "succefull"

            BENCH_PAPER._flag = 0  # REGION CRITICA
        else:
            result_detail = "busy, try later"   

    #BENCH OF TOBACO
    if (bench == "TOBACCO"): 
        if (BENCH_TOBACCO._flag == 0):
            BENCH_TOBACCO._flag = 1  # REGION CRITICA

            BENCH_TOBACCO._stock = Bench.iniBench(SIZE_ORDER,bench)
            time.sleep(TIMER_DEFAULD)
            result = "OK"
            result_detail = "succefull"  

            BENCH_TOBACCO._flag = 0   # REGION CRITICA
        else:
            result_detail = "busy, try later"  
    
    datos = {   "type" : "RELOAD",
               "bench" : bench,
              "answer" : result,
              "detail" : result_detail, 
               "stock" : "MATCH=" + str(len(BENCH_MATCH._stock)) + "  PAPER=" +str(len(BENCH_PAPER._stock)) + "  TOBACCO=" +str(len(BENCH_TOBACCO._stock))}
    diccionario.append(datos)
    bilioteca = {"event":[diccionario]}
    whiteXml(datos)

    result = json.dumps(bilioteca)
    return HttpResponse(result)

#Service 6
def serviceAlertSeller(bench):
    result = None
    global FLAG_LOG

    url = 'http://' + HOST_SELLER + '/serviceAlertSeller/'+bench
    r = requests.get(url)
    datos = {   "type"   : "SERVER ALERT",
                "bench"  : bench,
                "answer" : "OK",
                "detail" : "Server alert the seller", 
                "stock"  : "X"}
    whiteXml(datos)

    result = "empty, reload bench, try later"

    return result


#service 7   
def whiteXml(datos):
    global FLAG_LOG

    while True:
        if ( FLAG_LOG == 0 ):
            FLAG_LOG = 1 # REGION CRITICA

            root = loadXml()
            root = addElement(root,datos)
            saveXml(root)

            FLAG_LOG = 0 # REGION CRITICA
            break

#----------------------------------------------------------------------
#----------------------------------------------------------------------
#----------------METODOS COMUNICACION CON EL REPLICADOR UNO------------
#----------------------------------------------------------------------
#----------------------------------------------------------------------

IP_COORDINATOR_SERVICE = '127.0.0.1'
PORT_COORDINATOR_SERVICE = 2525

IP_REPLICATOR_TWO = '127.0.0.1' # ip del servidor replicador dos
PORT_REPLICATOR_TWO_SERVER = '3535' # puerto del replicador dos
IP_REPLICATOR_ONE = '127.0.0.1' # ip del servidor replicador uno
PORT_REPLICATOR_ONE_SERVER = '1515' # puerto del replicador uno

def replicate_coordinator(*args, **kwargs):
    global REPLICADOR_1_SOLICITO
    print("VOTE_COMMIT - UNO")
    REPLICADOR_1_SOLICITO = True # se asigna True a la bandera para validar que el replicador 1 solicito
    response = connect_rpc.ServerProxy("http://"+IP_REPLICATOR_TWO+":"+PORT_REPLICATOR_TWO_SERVER+"/")
    response.replicate_two('VOTE_COMMIT')
    return True

def aceptar_replica_fumador(*args, **kwargs):
    print('COMMIT')
    root = str(loadFile())
    print(root)
    response0 = connect_rpc.ServerProxy("http://"+IP_REPLICATOR_TWO+":"+PORT_REPLICATOR_TWO_SERVER+"/")
    return str(response0.envioXML_vendedor(root, 'COMMIT - GLOBAL_REPLICA ')), "COMMIT - GLOBAL_REPLICA "

def cancelar_replica_fumador(*args, **kwargs):
    print('DUAL')
    response0 = connect_rpc.ServerProxy("http://"+IP_REPLICATOR_TWO+":"+PORT_REPLICATOR_TWO_SERVER+"/")
    response0.respond_replicate('DUAL - VOTE_ABORT UNO ')

#----------------------------------------------------------------------
#----------------------------------------------------------------------
#----------------METODOS COMUNICACION CON EL REPLICADOR DOS------------
#----------------------------------------------------------------------
#----------------------------------------------------------------------

def replicate_coordinator_two(*args, **kwargs):
    global REPLICADOR_1_SOLICITO
    print("VOTE_COMMIT - DOS")
    REPLICADOR_1_SOLICITO = True # se asigna True a la bandera para validar que el replicador 1 solicito
    response = connect_rpc.ServerProxy("http://"+IP_REPLICATOR_TWO+":"+PORT_REPLICATOR_ONE_SERVER+"/")
    response.replicate_accept_one('VOTE_COMMIT')
    return True

def aceptar_replica_vendedor(*args, **kwargs):
    print('COMMIT')
    root = str(loadFile())
    print(root)
    response0 = connect_rpc.ServerProxy("http://"+IP_REPLICATOR_ONE+":"+PORT_REPLICATOR_ONE_SERVER+"/")
    return str(response0.envioXML_fumador(root, 'COMMIT - GLOBAL_REPLICA ')), "COMMIT - GLOBAL_REPLICA "

def cancelar_replica_vendedor(*args, **kwargs):
    print('DUAL')
    response0 = connect_rpc.ServerProxy("http://"+IP_REPLICATOR_ONE+":"+PORT_REPLICATOR_ONE_SERVER+"/")
    response0.respond_replicate('DUAL - VOTE_ABORT DOS')


def restoreXml_fumador(*args, **kwargs):
    root = str(loadFile())
    response0 = connect_rpc.ServerProxy("http://"+IP_REPLICATOR_ONE+":"+PORT_REPLICATOR_ONE_SERVER+"/")
    print(response0.deleteXml_log("BORRADO"))
    return root , "RESTORE XML - SUCCEFULL"

def restoreXml_vendedor(*args, **kwargs):
    root = str(loadFile())
    response0 = connect_rpc.ServerProxy("http://"+IP_REPLICATOR_TWO+":"+PORT_REPLICATOR_TWO_SERVER+"/")
    print(response0.deleteXml_log("BORRADO"))
    return root , "RESTORE XML - SUCCEFULL"

#----------------------------------------------------------------------
#----------------------------------------------------------------------
#---------------------SERVIDOR COORDINADOR-----------------------------
#----------------------------------------------------------------------
#----------------------------------------------------------------------

# decorador que inicicializa el demonio de la funcion coordinador
def thread_init(function):
    def wrapper(*args, **kwargs):
        thread = Thread(target=function, args=args, kwargs=kwargs)
        thread.daemon = True
        thread.start()
    return wrapper

@thread_init
def coordinator_server():
    server = SimpleXMLRPCServer((IP_COORDINATOR_SERVICE, PORT_COORDINATOR_SERVICE))
    server.register_function(replicate_coordinator, 'replicate_coordinator')
    server.register_function(aceptar_replica_fumador, 'aceptar_replica_fumador')
    server.register_function(cancelar_replica_fumador, 'cancelar_replica_fumador')
    server.register_function(aceptar_replica_vendedor, 'aceptar_replica_vendedor')
    server.register_function(cancelar_replica_vendedor, 'cancelar_replica_vendedor')
    server.register_function(replicate_coordinator_two, 'replicate_coordinator_two')
    server.register_function(restoreXml_fumador, 'restoreXml_fumador')
    server.register_function(restoreXml_vendedor, 'restoreXml_vendedor')
    server.serve_forever()
    
coordinator_server()