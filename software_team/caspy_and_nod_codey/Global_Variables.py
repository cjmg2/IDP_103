from Classes import Motor
from machine import Pin, PWM, I2C
from libs.tiny_code_reader.tiny_code_reader import TinyCodeReader

global rmotor 
rmotor = Motor(7, 6)

global lmotor 
lmotor = Motor(4, 5)

global level
level = 0

#global servo_pin
#servo_pin = PWM(Pin(15), 100)
#adc=ADC(Pin("""pin no.""")) #replace with pin connected to the servo's analogue output wire

#define line sensors
global FL
FL = Pin(16, Pin.IN, Pin.PULL_DOWN)
global L
L = Pin(17, Pin.IN, Pin.PULL_DOWN)
global R
R = Pin(20, Pin.IN, Pin.PULL_DOWN)
global FR
FR = Pin(21, Pin.IN, Pin.PULL_DOWN)

#define button
global Button
Button = Pin(22, Pin.IN, Pin.PULL_DOWN)

#define qr enable
global qr_enable
qr_enable = Pin(14, Pin.OUT)

#define LED
global led_enable
led_enable = Pin(10, Pin.OUT)

#define TOF sensors
global i2c_bus_0
i2c_bus_0 = I2C(id=0, scl=Pin(9), sda=Pin(8), freq=400000)

#define qr code reader
global i2c_bus_1
i2c_bus_1 = I2C(id=1, scl=Pin(19), sda=Pin(18), freq=400000)


global tiny_code_reader
tiny_code_reader = TinyCodeReader(i2c_bus_1)
