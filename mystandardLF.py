

import RPi.GPIO as GPIO, sys, threading, time

#use physical pin numbering
GPIO.setmode(GPIO.BOARD)

#set up digital line detectors as inputs
GPIO.setup(12, GPIO.IN)
GPIO.setup(13, GPIO.IN)
GPIO.setup(7, GPIO.IN)
GPIO.setup(11,GPIO.IN)
GPIO.setup(22, GPIO.IN)

#Assigning names to line sensors
farright = 7
right = 11
middle = 22
left = 13
farleft = 12

#Define global variables
globalstop=0
finished=False
fast=18
turnspeed=30
turnspeed2=15
slow=10

#use pwm on inputs so motors don't go too fast
GPIO.setup(19, GPIO.OUT)
p=GPIO.PWM(19, 20)
p.start(0)
GPIO.setup(21, GPIO.OUT)
q=GPIO.PWM(21, 20)
q.start(0)
GPIO.setup(24, GPIO.OUT)
a=GPIO.PWM(24,20)
a.start(0)
GPIO.setup(26, GPIO.OUT)
b=GPIO.PWM(26,20)
b.start(0)

def stopAll():
       a.ChangeDutyCycle(0)
       b.ChangeDutyCycle(0)
       p.ChangeDutyCycle(0)
       q.ChangeDutyCycle(0)

def turnAround():
       #while GPIO.input(middle)==0:
       p.ChangeDutyCycle(10)
       q.ChangeDutyCycle(0)
       a.ChangeDutyCycle(0)
       b.ChangeDutyCycle(13)
       print ('turn around')

       
def sharpRight():
       p.ChangeDutyCycle(0)
       q.ChangeDutyCycle(10)
       a.ChangeDutyCycle(25)
       b.ChangeDutyCycle(0)
       time.sleep(.27)
##       stopAll()
       print ('sharp right')
##       if GPIO.input(22)==1 and GPIO.input(7)==0 and GPIO.input(12)==0:
##           stopAll()


def followLine():
       if GPIO.input(right)==0 and GPIO.input(left)==0:
              p.ChangeDutyCycle(fast)
              q.ChangeDutyCycle(0)
              a.ChangeDutyCycle(fast)
              b.ChangeDutyCycle(0)

       elif GPIO.input(right)==1:
              p.ChangeDutyCycle(0)
              q.ChangeDutyCycle(slow)
              a.ChangeDutyCycle(slow)
              b.ChangeDutyCycle(0)

       elif GPIO.input(left)==1:
              p.ChangeDutyCycle(slow)
              q.ChangeDutyCycle(0)
              a.ChangeDutyCycle(0)
              b.ChangeDutyCycle(slow)

def fwd():
       p.ChangeDutyCycle(10)
       q.ChangeDutyCycle(0)
       a.ChangeDutyCycle(10)
       b.ChangeDutyCycle(0)
       #time.sleep(.3)


try:
       while True:
#                  if GPIO.input(12)==1 and GPIO.input(13)==1 or globalstop==1:

              if GPIO.input(farright)==0 and GPIO.input(farleft)==0 and GPIO.input(middle):
               #follow a straight line
                     followLine()

              #elif GPIO.input(right)==1 and GPIO.input(middle)==1:
              #       followLine()
                     
              elif GPIO.input(farright)==1:# and GPIO.input(right)==1:
              #turn right
                     sharpRight()
              
              elif GPIO.input(right)==0 and GPIO.input(left)==0 and GPIO.input(middle)==0 and GPIO.input(farright)==0 and GPIO.input(farleft)==0:
                     turnAround()

              
              elif GPIO.input(left)==1 and GPIO.input(middle)==1:#and GPIO.input(farright)==0:
                     while GPIO.input(farright)==0 and GPIO.input(farleft)==1:
                            if GPIO.input(right)==1:
                                   sharpRight()

                            
                            else:
                                   fwd()
                                   print('fwd')

              #elif (GPIO.input(left)==1 and GPIO.input(right)==1 and GPIO.input(middle)==0) or (GPIO.input(left)==0 and GPIO.input(middle)==1 and GPIO.input(farleft)==1):
              #       stopAll()

           

     
                            
             

       

             


except KeyboardInterrupt:
       finished = True  # stop other loops
       GPIO.cleanup()
       sys.exit()
