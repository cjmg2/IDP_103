from Classes import Motor
from machine import Pin, PWM

global rmotor 
rmotor = Motor(7, 6)

global lmotor 
lmotor = Motor(4, 5)

global level
level = 0

#global servo_pin
#servo_pin = PWM(Pin(15), 100)
#adc=ADC(Pin("""pin no.""")) #replace with pin connected to the servo's analogue output wire

global FL
FL = Pin(19, Pin.IN, Pin.PULL_DOWN)
global L
L = Pin(20, Pin.IN, Pin.PULL_DOWN)
global R
R = Pin(21, Pin.IN, Pin.PULL_DOWN)
global FR
FR = Pin(18, Pin.IN, Pin.PULL_DOWN)

global qr_enable
qr_enable = Pin(14, Pin.OUT)

global led_enable
led_enable = Pin(10, Pin.OUT)
