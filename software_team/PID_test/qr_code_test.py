from machine import Pin, PWM, SoftI2C, I2C
from caspy_and_nod_codey.libs.tiny_code_reader.tiny_code_reader import TinyCodeReader
import time

def qr_test():

    pin = 14
    led = Pin(pin, Pin.OUT)
    led.value(1)

    i2c_bus = I2C(id=0, scl=Pin(17), sda=Pin(16), freq=400000) # I2C0 on GP16 & GP17
    tiny_code_reader = TinyCodeReader(i2c_bus)
    while True:
        time.sleep(TinyCodeReader.TINY_CODE_READER_DELAY)
        code = tiny_code_reader.poll()
        if code is not None:
            print(f"Code found: {code}")

if __name__ == "__main__":
    qr_test()