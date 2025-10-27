from Classes import Motor
from machine import Pin, PWM

global rmotor 
rmotor = Motor(4, 5)

global lmotor 
lmotor = Motor(7, 6)

global level
level = 0

global servo_pin
servo_pin = PWM(Pin(28), 100)