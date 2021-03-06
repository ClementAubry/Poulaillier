# Import des modules
import os
import time
import ephem
import RPi.GPIO as GPIO

#Inspired from http://stephane.lavirotte.com/perso/rov/esc_brushless_raspberry.html
# with GPIO mapping here : http://deusyss.developpez.com/tutoriels/RaspberryPi/PythonEtLeGpio/#LII-D
#Servo mapping:
#0 on P1-7 GPIO-4
#1 on P1-11 GPIO-17
#2 on P1-12 GPIO-18
#3 on P1-13 GPIO-21
#4 on P1-15 GPIO-22
#5 on P1-16 GPIO-23
#6 on P1-18 GPIO-24
#7 on P1-22 GPIO-25

pinHallDoorHigh=14
pinHallDoorLow=15
GPIO.setmode(GPIO.BCM)     # set up BCM GPIO numbering  
GPIO.setup(pinHallDoorHigh, GPIO.IN)
GPIO.setup(pinHallDoorLow, GPIO.IN)

#in milliseconds
minDuty=1
meanDuty=1.5
maxDuty=2

sens=True
dutyStep=0.5
lastValue=meanDuty 

o=ephem.Observer()
o.lat='48.395574'
o.long='-4.333449'
o.horizon = '-6'
etatPorte = 'fermee'

def echoPWM(highValueMs):
  os.system("echo 0={0} > /dev/servoblaster".format(highValueMs*100))
  lastValue = highValueMs*100

def callbackHallDoorHigh(channel):
  print "callbackHallDoorHigh"
  if GPIO.input(pinHallDoorHigh):  
    print "La porte se ferme"
  else:  
    print "La porte est ouverte"
    emergencyBreakDoor()
    etatPorte='ouverte'

def callbackHallDoorLow(channel):
  print "callbackHallDoorLow"
  if GPIO.input(pinHallDoorLow):  
    print "La porte s'ouvre"
  else:  
    print "La porte est fermee"
    breakDoor()
    etatPorte='fermee'

def openDoor():
  os.system("echo 0=180 > /dev/servoblaster")

def closeDoor():
  os.system("echo 0=120 > /dev/servoblaster")

def emergencyBreakDoor():
  os.system("echo 0=150 > /dev/servoblaster")

#USAGE : 
# openDoor() activate PWM smoothly in one direction
# closeDoor() activate PWM smoothly in the other direction
# breakDoor() smoothly stop PWM
# emergencyBreakDoor() stop PWM not smoothly

#GPIO.add_event_detect(pinHallDoorHigh, GPIO.BOTH, callback=callbackHallDoorHigh) 
#GPIO.add_event_detect(pinHallDoorLow, GPIO.BOTH, callback=callbackHallDoorLow) 
emergencyBreakDoor()
# menu info
print "s = Stop door"
print "o = Open door"
print "c = Close door"
try:
  while True:
     # Now the program asks for the direction the servo should turn.
    input = raw_input("Selection: ")
    if(input == "s"):
      emergencyBreakDoor()
    if(input == "o"):
      etatPorte = 'fermee'
      openDoor()
      while not(etatPorte == 'ouverte'):
        if (GPIO.input(pinHallDoorHigh)):
          print "Atente porte ouverte"
        else:
          print "Porte ouverte"
          emergencyBreakDoor()
          etatPorte = 'ouverte'
    if(input == "c"):
      etatPorte = 'ouverte'
      closeDoor()
      while not(etatPorte == 'fermee'):
        if (GPIO.input(pinHallDoorLow)):
          print "Atente porte fermee"
        else:
          print "Porte fermee"
          emergencyBreakDoor()
          etatPorte = 'fermee'
    time.sleep(0.25)
except (KeyboardInterrupt, SystemExit):
  GPIO.cleanup()
  print "Arret du programme par Ctrl+c"
  raise 
finally:
  GPIO.cleanup()
  emergencyBreakDoor()
  print "Arret du programme..."
  raise 
