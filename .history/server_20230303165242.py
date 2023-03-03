import network   
import urequests    
import utime    #import des fonction lier au temps
import ujson    #import des fonction lier aà la convertion en Json
from machine import Pin
import time
import socket
import select
 
pir = Pin(22, Pin.IN, Pin.PULL_DOWN)
n = 0
i=0
led = Pin(11, Pin.OUT)
buzer = Pin(7, Pin.OUT)
 
 
print('ALARME ALLUMÉ')
time.sleep(1)
print('GO !')

wlan = network.WLAN(network.STA_IF) # met la raspi en mode client wifi
wlan.active(True) # active le mode client wifi

# Configure le serveur WebSocket
server_socket = socket.socket()
server_socket.bind(('', 80))
server_socket.listen(1)
print('En attente de connexions WebSocket...')
 
# Enregistre les sockets en lecture et en écriture pour la fonction select()
inputs = [server_socket]
outputs = []

while True:
    # Utilise la fonction select() pour gérer plusieurs connexions simultanément
    readable, writable, exceptional = select.select(inputs, outputs, inputs)
 
    for s in readable:
        # Accepte une nouvelle connexion WebSocket
        if s is server_socket:
            conn, addr = s.accept()
            print('Nouvelle connexion WebSocket:', addr)
            inputs.append(conn)
            outputs.append(conn)
 
        # Reçoit des données sur une connexion WebSocket
        else:
            data = s.recv(1024)
            if data:
                print('Données reçues de la connexion WebSocket:', data)
 
    for s in exceptional:
        print('lol')
        print('Connexion WebSocket en erreur:', s)
        inputs.remove(s)
        outputs.remove(s)
        s.close()

    # Vérifie le capteur de mouvement PIR
    if pir.value() == 1:
        n = n + 1
        message = 'ALARME ! MOUVEMENT DETECTÉ ' + str(n)
        print(message)
 
        for i in range(5):
            led.on()
            time.sleep(1)
            led.off()
            time.sleep(1)
            i += 1
 
        # Envoie le message à toutes les connexions WebSocket
        for s in outputs:
            s.send(message.encode())
 
    time.sleep(3)
