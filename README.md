# Django-REST-RPC
Uso paralelo de servicios REST y RPC sobre 3 servidores Django
==========
Instalacion - Pasos
--------------------
+ 1) install python 3.4.4
+ 2) pip install Django==1.10.5
+ 3) pip install requests 

Servidores
--------------------
+ Servidor-1 (fumador    / Replicador 1)
+ Servidor-2 (Web Server / Coordinador de Replicas)
+ Servidor-3 (Provehedor / replicador 2)

Estructura
--------------------
Servidor-1    <<-REST/RPC->>    Servidor-2   <<-REST/RPC->>    Servidor-3

- Servicios REST para el manejo de funcionalidades de fumador, banquito y provehedor 
- Servidios RPC para el manejo de las replicas del Log.xml

Cualquier duda o comentario no duden en preguntar 
+ bvpenaloza.11@gmail.com
