import time
import requests
import board
import busio
import asyncio
import threading
import urllib.request
import RPi.GPIO as GPIO
import os
import subprocess
from subprocess import Popen
from pathlib import Path
import time
from omxplayer.player import OMXPlayer

#time.sleep(60.0)

GPIO.setup(26, GPIO.IN) # señal entrada
GPIO.setup(11, GPIO.OUT) #señal apagado entrada
GPIO.setup(13, GPIO.IN) #persona en entrada

GPIO.setup(6, GPIO.OUT) #señal apagado salida
GPIO.setup(5, GPIO.IN) #señal salida(arduino2)
GPIO.setup(19, GPIO.IN)#persona salida

GPIO.setup(10, GPIO.OUT) #apagado señal oportunidad
GPIO.setup(9, GPIO.IN) #señal oportunidad
oportunidad = GPIO.input(9)

GPIO.setup(6, GPIO.OUT) 
GPIO.output(6,GPIO.HIGH)
time.sleep(0.5)
GPIO.setup(6, GPIO.OUT) 
GPIO.output(6,GPIO.LOW)
señalSalida = GPIO.input(5)
personaSalida = GPIO.input(19)

GPIO.setup(11, GPIO.OUT)
GPIO.output(11,GPIO.HIGH)
time.sleep(0.5)
GPIO.setup(11, GPIO.OUT)
GPIO.output(11,GPIO.LOW)
personaEntrada = GPIO.input(13)
señalEntrada = GPIO.input(26)

def PostOport():
    url= 'http://143.198.132.112/smarthh/novaspost_oportunidades.php'
    status_code = 200
    try:
        status_code = requests.get(url, timeout = 10)
        
    except requests.exceptions.ConnectTimeout:
        #print ('time out')
        status_code = 3
    except requests.exceptions.ConnectionError:
        #print ('error de conexion')
        status_code = 3
        
    if status_code == 200:
        query = {'lat':'45','lon':'180'}
        response = requests.post('http://143.198.132.112/smarthh/novaspost_oportunidades.php',data = {'foo2':'bar2'})
        #print (response.text)
    else:
        pass
  
        
def PostEfect():
   
    url= 'http://143.198.132.112/smarthh/novaspost_efectivo.php'
    status_code = 200
    try:
        status_code = requests.get(url, timeout = 5)
        status_code.raise_for_status()
    except requests.exceptions.ConnectTimeout:
        #print ('time out')
        status_code = 3
    except requests.exceptions.ConnectionError:
       # print ('error de conexion')
        status_code = 3
    
    if status_code == 200:
        query = {'lat':'45','lon':'180'}
        response = requests.post('http://143.198.132.112/smarthh/novaspost_efectivo.php',data = {'foo2':'bar2'})
        #print (response.text)
    else:
        pass
        #print ('no fue posible entrar')
    #print("lavado de manos")
    
def apagarbomba():
    GPIO.output(10,GPIO.HIGH)
    time.sleep(0.4)
    GPIO.output(10,GPIO.LOW)
    time.sleep(0.1)

def apagarentrada():
    global k
    GPIO.setup(26, GPIO.IN)
    señalEntrada = GPIO.input(26)
    while(señalEntrada == 1):
        GPIO.setup(26, GPIO.IN)
        señalEntrada = GPIO.input(26)
        GPIO.setup(5, GPIO.IN)
        señalSalida = GPIO.input(5)
        GPIO.setup(6, GPIO.OUT)    
        GPIO.output(6,GPIO.HIGH)
        time.sleep(0.1)
        GPIO.setup(6, GPIO.OUT)
        GPIO.output(6,GPIO.LOW)
        time.sleep(0.1)
    k = 1
   

def apagarsalida():
    
    GPIO.setup(5, GPIO.IN)
    señalSalida = GPIO.input(5)
    global l
    while(señalSalida == 1):
        GPIO.setup(5, GPIO.IN)
        señalSalida = GPIO.input(5)
        GPIO.setup(11, GPIO.OUT)
        GPIO.output(11,GPIO.HIGH)
        time.sleep(0.1)
        GPIO.setup(11, GPIO.OUT)
        GPIO.output(11,GPIO.LOW)
        time.sleep(0.1)
    l = 1

def screen():
	global screen_status
	url= 'http://143.198.132.112/smarthh/pantalla.php'
	status_code = 200
	try:
		status_code = requests.get(url,timeout = 10)
		#print(status_code)

	except requests.exceptions.ConnectTimeout:
		status_code = 3
	except requests.exceptions.ConnectionError:
		status_code = 3
	if status_code == 200 or "[200]":
		query = {'lat':'45','lon':'180'}
		r = requests.post('http://143.198.132.112/smarthh/pantalla.php')
		screen_status = r.text
		#print(r.text)
		#print('request realizado')
	else:print('no hubo request')
def imagen(j):
    if(j == 1):
        img = pygame.image.load('/home/pi/Downloads/hnd/2.jpg')
        img = pygame.transform.rotate(img,-90)
        img = pygame.transform.scale(img,(720,600))
    elif(j == 2):
        img = pygame.image.load('/home/pi/Downloads/hnd/3.jpg')
        img = pygame.transform.rotate(img,-90)
        img = pygame.transform.scale(img,(720,600))
    else:
        img = pygame.image.load('/home/pi/Downloads/hnd/5.jpg')
        img = pygame.transform.rotate(img,-90)
        img = pygame.transform.scale(img,(720,600))
        
    game.blit(img,(0,0))	

def imagenes_inicio():

    while True:
    
            screen()

            if((screen_status == '1') and (a != 'omx1')):

                if (a == 'no video'):
                        player = OMXPlayer(video,dbus_name = 'org.mpris.MediaPlayer2.player', args = '--loop --no-osd')
                        a = 'omx1'
                        b = 'omx1'
                        i = 0
                else:
                        i = 1
                        a = 'omx1'
                        player = OMXPlayer(video,dbus_name = 'org.mpris.MediaPlayer2.player', args = '--loop --no-osd')
                        player.hide_video
         
                                    
            elif((screen_status == '2') and (a != 'omx2')):
                    
                if (a == 'no video'):                
                        omx2 = OMXPlayer(video2, dbus_name = 'org.mpris.MediaPlayer2.omx2', args = '--loop --no-osd')
                        a = 'omx2'
                        b = 'omx2'
                        i = 0
                else:

                        i = 1                
                        a = 'omx2'   
                        omx2 = OMXPlayer(video2,dbus_name = 'org.mpris.MediaPlayer2.omx2', args ='--loop --no-osd')
                        omx2.hide_video()

            elif((screen_status == '3') and (a != 'omx3')):
                    
                if (a == 'no video'):                
                        omx3 = OMXPlayer(video3, dbus_name = 'org.mpris.MediaPlayer2.omx3', args = '--loop --no-osd')
                        a = 'omx3'
                        b = 'omx3'
                        i = 0
                else:

                        i = 1                
                        a = 'omx3'   
                        omx3 = OMXPlayer(video3,dbus_name = 'org.mpris.MediaPlayer2.omx3', args ='--loop --no-osd')
                        omx3.hide_video()

            elif((screen_status == '4') and (a != 'omx4')):
                    
                if (a == 'no video'):                
                        omx4 = OMXPlayer(video4, dbus_name = 'org.mpris.MediaPlayer2.omx4', args = '--loop --no-osd')
                        a = 'omx4'
                        b = 'omx4'
                        i = 0
                else:

                        i = 1                
                        a = 'omx4'   
                        omx4 = OMXPlayer(video4,dbus_name = 'org.mpris.MediaPlayer2.omx4', args ='--loop --no-osd')
                        omx4.hide_video()
                
            elif(screen_status == '11'):
                os.system('sudo killall omxplayer.bin')
                a = 'no video'
                b = 'no video'
                i = 0
            else:
                i = 0
                pass

            if (b == 'omx1') and (i == 1):
                    player.pause()
                    player.hide_video()
                    time.sleep(2.5)
                    player.quit()
                    i = 0
                    b = a
            elif (b == 'omx2') and (i == 1):
                    omx2.pause()
                    omx2.hide_video()
                    time.sleep(2.5)
                    omx2.quit()
                    i = 0
                    b = a
            elif (b == 'omx3') and (i == 1):
                    omx3.pause()
                    omx3.hide_video()
                    time.sleep(2.5)
                    omx3.quit()
                    i = 0
                    b = a
            elif (b == 'omx4') and (i == 1):
                    omx4.pause()
                    omx4.hide_video()
                    time.sleep(2.5)
                    omx4.quit()
                    i = 0
                    b = a
            else:
                    pass
    
global screen_status
#player = []
screen_status = ''
flag = 1
global video
global video2

video = Path("/home/pi/Downloads/hnd02vd/NOVAS1.mp4")
video2 = Path("/home/pi/Downloads/hnd02vd/NOVAS2.mp4")
video3 = Path("/home/pi/Downloads/hnd02vd/NOVAS3.mp4")
video4 = Path("/home/pi/Downloads/hnd02vd/NOVAS4.mp4")
video5 = Path("/home/pi/Downloads/hnd02vd/NOVAS4.mp4")
spc_video = Path("/home/pi/Downloads/spc.mp4")
global a
global i
global player
global omx2
global omx3
global omx4
i = 0
a = 'no video'
b = 'no video'


print("Iniciando...")
#i = 1

s = threading.Thread(target = imagenes_inicio)
s.start()

while True:

    
    
    
    GPIO.setup(26, GPIO.IN)
    señalEntrada = GPIO.input(26)
    GPIO.setup(5, GPIO.IN)
    señalSalida = GPIO.input(5)

    if(señalEntrada == 1):
        GPIO.setup(13, GPIO.IN) 
        personaEntrada = GPIO.input(13)
        GPIO.setup(19, GPIO.IN)
        personaSalida = GPIO.input(19)
        oportunidad = GPIO.input(9)

        if(oportunidad == 1):
            flag = 1;
        else:
            flag = 0;
        while(personaEntrada == 1 or personaSalida == 1):
            personaEntrada = GPIO.input(13)
            personaSalida = GPIO.input(19)
            #print("alguien en la puerta")
            #print(personaEntrada)
            
        if(flag ==1):
            b = threading.Thread(target = apagarbomba)
            b.start()
            e = threading.Thread(target = PostEfect)
            e.start()
            f = threading.Thread(target = PostOport)
            f.start()
            #print('realizar peticion http oportunidad con lavado de manos')
        else:
            b = threading.Thread(target = apagarbomba)
            b.start()
            f = threading.Thread(target = PostOport)
            f.start()
            #i = ventana(i)
            
            #print('realizar peticion http oportunidad sin lavado de manos')
            
        greenflag = 1
        global k
        global l
        k = 0
        l = 0
        while(k == 0):
            
            if(greenflag ==1):
                es = threading.Thread(target = apagarentrada)
                es.start()
                greenflag = 0
                #print("valor de k es:")
                #print(k)
            else:
                pass
            
        greenflag = 1
        #print(k)
        
        while(l == 0):
            
            if(greenflag ==1):
                ec = threading.Thread(target = apagarsalida)
                ec.start()
                greenflag = 0
                
            else:
                pass  
        greenflag = 1

            
  #############################################################          
        #print("apagando... entrada")  
        #print("señal apagada")
        #i = i + 1
        #print(i)

    elif (señalSalida == 1):

        GPIO.setup(13, GPIO.IN) 
        personaEntrada = GPIO.input(13)
        GPIO.setup(19, GPIO.IN)
        personaSalida = GPIO.input(19)
        while(personaEntrada == 1 or personaSalida == 1):
            personaEntrada = GPIO.input(13)
            personaSalida = GPIO.input(19)
            #print("alguien en la puerta")
            #print(personaEntrada)
    
        greenflag = 1
        
        k = 0
        l = 0
                
        while(l == 0):
            
            if(greenflag ==1):
                er = threading.Thread(target = apagarsalida)
                er.start()
                greenflag = 0
                
            else:
                pass  
        greenflag = 1
            
        while(k == 0):
            
            if(greenflag ==1):
                ee = threading.Thread(target = apagarentrada)
                ee.start()
                greenflag = 0
                #print("valor de k es:")
                #print(k)
            else:
                pass
            
        greenflag = 1
        #print(k)
            
        #print("salida")
        

    else:
        
        GPIO.output(6,GPIO.LOW)
        GPIO.setup(11, GPIO.OUT)
        GPIO.output(11,GPIO.LOW)
        #print("no hay nadie")
 


