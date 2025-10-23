from machine import Pin, PWM, SoftI2C, I2C
from utime import sleep

from libs.DFRobot_TMF8x01 import DFRobot_TMF8801, DFRobot_TMF8701
from libs.tiny_code_reader.tiny_code_reader import TinyCodeReader

#find pin
pwm_pin_no = 28  # Pin 28 = GP28 (labelled 34 on the jumper), replace with correct pin
pwm_pin = PWM(Pin(pwm_pin_no), 100)

def lift():
    """This function lifts block 20mm off the ground"""
    while level<"""angle corresponding with displacement of 20mm""":
        direction=1
        u16_level = int(65535 * level / 100)
        pwm_pin.duty_u16(u16_level)
    sleep(0.1)
   
def raise_to_rack():
    """This function raises block to the height of the unloading rack"""
    while level<"""angle corresponding with displacement of 30mm""":
        direction=1
        u16_level = int(65535 * level / 100)
        pwm_pin.duty_u16(u16_level)
    sleep(0.1)

def lower():
    """This function lowers block onto rack"""
    while level>"""angle corresponding to displacement of 26mm""":
        direction=-1
        u16_level = int(65535 * level / 100)
        pwm_pin.duty_u16(u16_level)
    sleep(0.1)

def lower_to_ground():
    """This function lowers forks back to 0 displacement after a block has been placed"""
    while level>0:
        direction=-1
        u16_level = int(65535 * level / 100)
        pwm_pin.duty_u16(u16_level)
    sleep(0.1)

def get_f_distance():

    i2c_bus = I2C(id=0, sda=Pin(8), scl=Pin(9), freq=100000)
    tof = DFRobot_TMF8701(i2c_bus=i2c_bus)

#    while(tof.begin() != 0):
#      counter += 1
#      if counter > 100:
#          break
#      sleep(0.5)
    tof.start_measurement(calib_m = tof.eMODE_NO_CALIB, mode = tof.eCOMBINE)
    
    #   while True:
#     if(tof.is_data_ready() == True):
#       return tof.get_distance_mm()
#     counter += 1
#      if counter > 100:
#        break
    return tof.get_distance_mm()

def detect_box():
    """This function detects when within 5mm of a box"""
    d = 5
    if get_f_distance() < d:
        return "at junction"

def get_qr_code():
    i2c_bus = I2C(id=0, scl=Pin(17), sda=Pin(16), freq=400000) # I2C0 on GP16 & GP17
    tiny_code_reader = TinyCodeReader(i2c_bus)
    code = tiny_code_reader.poll()
    return code

def get_s_distance():
    """This function returns the side distance using TMF8801"""
    counter = 0

    i2c_bus = I2C(id=0, sda=Pin(8), scl=Pin(9), freq=100000)
    tof = DFRobot_TMF8801(i2c_bus=i2c_bus)
#    while(tof.begin() != 0):
#      counter += 1
#      if counter > 100:
#          break
#      sleep(0.5)
    tof.start_measurement(calib_m = tof.eMODE_NO_CALIB)
  
#   while True:
#     if(tof.is_data_ready() == True):
#       return tof.get_distance_mm()
#     counter += 1
#      if counter > 100:
#        break
    return tof.get_distance_mm()

#def findbox():