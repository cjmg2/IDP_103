from machine import Pin
from utime import sleep

led_pin = 10
led = Pin(led_pin, Pin.OUT)

while True:
    print("Blinking Off")
    led.value(0)
    sleep(1)
    print("Blinking On")
    led.value(1)
    sleep(20)    