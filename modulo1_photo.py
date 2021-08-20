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
import pygame

time.sleep(60.0)
os.environ["DISPLAY"] = ":0"
pygame.display.init()
#game = pygame.display.set_mode((200,300))
game = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
#game = pygame.display.set_mode((0,0),0,32,pygame.NOFRAME)
#game = pygame.display.set_mode((0,0),pygame.NOFRAME)
pygame.display.set_caption('picture')
img = pygame.image.load('/home/pi/Downloads/hnd/5.jpg')
img = pygame.transform.scale(img,(400,300))
white =(255,255,255)


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

def start_img():
    j = 0   
    crash = False 
    while not crash:    
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    pygame.quit()
                    crash = True
                elif event.key == pygame.K_RIGHT:
                    j = 1
                elif event.key == pygame.K_LEFT:
                    j = 2
            #print('dentro del for')
                    
        game.fill(white)
        imagen(j)
        pygame.display.update()
    
    
flag = 1
video = Path("/home/pi/Downloads/hnd/camalion.mp4")
video2 = Path("/home/pi/Downloads/AnimatedSF.mp4")
global a
os.environ['DISPLAY']= ":0"
global screen_status
screen_status = ''
a = 'no video'
flag = 1
print("Iniciando...")
i = 1

s = threading.Thread(target = start_img)
s.start()

while True:


    
    
    GPIO.setup(26, GPIO.IN)
    señalEntrada = GPIO.input(26)
    GPIO.setup(5, GPIO.IN)
    señalSalida = GPIO.input(5)
    #print("señal entrada:")
    #print(señalEntrada)
    #print("señal salida:")
    #print(señalSalida)
        
    if(señalEntrada == 1):
        GPIO.setup(13, GPIO.IN) 
        personaEntrada = GPIO.input(13)
        GPIO.setup(19, GPIO.IN)
        personaSalida = GPIO.input(19)
        oportunidad = GPIO.input(9)
        #print("alguien en la puerta")
         #print(personaEntrada)
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
        i = i + 1
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
 


