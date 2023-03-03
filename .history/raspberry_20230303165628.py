from machine import Pin

import time
 
pir = Pin(22, Pin.IN, Pin.PULL_DOWN)
n = 0
#led = Pin(14,Pin.OUT)
buzzer = Pin(11, Pin.OUT)
 
print('ALARME ALLUMÉ')
time.sleep(1)
print('GO !')
 
while True:
     if pir.value() == 1:
          n = n+1
          print('ALARME ! MOUVEMENT DETECTÉ ',n)
          #led.toggle()
          buzzer.value(1)
          time.sleep(1)

     else:
        buzzer.value(0)
     time.sleep(3)