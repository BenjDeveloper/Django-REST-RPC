import xml.etree.cElementTree as Xml
from datetime import datetime
from django.conf import settings

# Variables Globales
PATH_LOG =  settings.XML_FOLDER+'log.xml'


# Manejo Xml
def loadFile():
    contenido = None
    try:
        with open(PATH_LOG, 'r') as archivo:
            contenido = archivo.read()
            archivo.close()
    except Exception:
        createXml()
        with open(PATH_LOG, 'r') as archivo:
            contenido = archivo.read()
            archivo.close()
    return contenido

def safeFile(str):
    contenido = str
    try:
        with open(PATH_LOG, 'w') as archivo:
            archivo.write(contenido)
            archivo.close()
    except Exception:
        createXml()
        with open(PATH_LOG, 'w') as archivo:
            archivo.write(contenido)
            archivo.close()

def loadXml():
    root = None
    try:
        with open(PATH_LOG, 'rt') as f:
            root = Xml.parse(f).getroot()
    except Exception:
        createXml()
        with open(PATH_LOG, 'rt') as f:
            root = Xml.parse(f).getroot()
    return root


def addElement(root,dato):
    nodoP = Xml.SubElement(root,  "Event" )
    nodoH1 = Xml.SubElement(nodoP, "Action").text = dato.get("type") + " " + dato.get("bench")
    nodoH2 = Xml.SubElement(nodoP, "Answer").text = dato.get("answer")
    nodoH3 = Xml.SubElement(nodoP, "Date"  ).text = datetime.today().strftime('%Y/%m/%d:%H:%M:%S')
    nodoH4 = Xml.SubElement(nodoP, "Detail").text = dato.get("detail")
    nodoH4 = Xml.SubElement(nodoP, "Stock").text = dato.get("stock")
    return root


def saveXml(root):
    arbol = Xml.ElementTree(root) 
    arbol.write(PATH_LOG)


def createXml():
    arbol = Xml.ElementTree(Xml.Element("root"))
    arbol.write(PATH_LOG)


def deleteXml():
    try:
        os.remove(PATH_LOG)
    except Exception:
        pass


