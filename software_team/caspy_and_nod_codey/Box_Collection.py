from machine import Pin, PWM, SoftI2C, I2C
from utime import sleep
import Global_Variables as gv
from libs.tiny_code_reader.tiny_code_reader import TinyCodeReader
    

"""def get_servo_angle():
   """"""reads the analogue feedback of the servo to get the current angle""""""
   angle=gv.adc.read_u16()*0.47-33.4 #this is the function on the servo documentation to get the angle from the analogue output
   return angle"""

def change_height(target_level, current_level):
    led_pin = 15  # Pin 28 = GP28 (labelled 34 on the jumper)
    led_PWM = PWM(Pin(15), 100)

    if target_level > current_level:
        direction = 1
    if target_level < current_level:
        direction = -1
    while current_level != target_level:
        
        u16_level = int(65535 * current_level / 100)
        led_PWM.duty_u16(u16_level)
    
        #update level and sleep
        print(f"Level={current_level}, u16_level={u16_level}, direction={direction}")
        current_level += direction
        sleep(0.1)

def initialise_servo():
    change_height(0)
def lower_to_ground():
    change_height(0)
def lower_onto_rack():
    change_height(30)
def raise_to_rack():
    change_height(30)
def lift_block():
    change_height(40)



















# def initalise_servo():
#     """This function initialises the servo motor"""
#     gv.level = 0 #or a different level if this is too low for the forks to insert into the pallet
     
#     #select pin
#     pwm_pin_no = 28  # Pin 28 = GP28 (labelled 34 on the jumper), replace with correct pin
#     gv.servo_pin = PWM(Pin(pwm_pin_no), 100)

#     #level-to-height ratio is 0.8836

#     #the initial level should be added to the other levels if it is not zero
#     u16_level = int(65535 * gv.level / 100)
#     gv.servo_pin.duty_u16(u16_level)

# def lift_block():
#     """lifts block 20mm off the ground"""
#     while gv.level<23: #or 34, if the block can be raised to 30mm right away
#         direction=1
#         gv.level += direction
#         u16_level = int(65535 * gv.level / 100)
#         gv.servo_pin.duty_u16(u16_level)
   
# def raise_to_rack(): #this is not needed if the block can be raised to 30mm right away
#     """raises block to the height of the unloading rack"""
#     while gv.level<34:
#         direction=1
#         gv.level += direction
#         u16_level = int(65535 * gv.level / 100)
#         gv.servo_pin.duty_u16(u16_level)

# def lower_onto_rack():
#     """lowers block onto rack"""
#     while gv.level>28:
#         direction=-1
#         gv.level += direction
#         u16_level = int(65535 * gv.level / 100)
#         gv.servo_pin.duty_u16(u16_level)

# def lower_to_ground():
#     """lowers forks back to 0 displacement after a block has been placed"""
#     while gv.level>0:
#         direction=-1
#         gv.level += direction
#         u16_level = int(65535 * gv.level / 100)
#         gv.servo_pin.duty_u16(u16_level)

def get_f_distance():
    """This function returns the forward distance"""
    i2c_bus = I2C(id=0, sda=Pin(8), scl=Pin(9), freq=100000)
    tof = DFRobot_TMF8701(i2c_bus=i2c_bus)

    while(tof.begin() != 0):
      counter += 1
      if counter > 100:
          break
      sleep(0.5)
    tof.start_measurement(calib_m = tof.eMODE_NO_CALIB, mode = tof.eCOMBINE)
    
    while True:
        if(tof.is_data_ready() == True):
            return tof.get_distance_mm()
        counter += 1
        if counter > 100:
            break
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

#def get_s_distance():
    """This function returns the side distance using TMF8801"""
#    counter = 0

#    i2c_bus = I2C(id=0, sda=Pin(8), scl=Pin(9), freq=100000)
#    tof = DFRobot_TMF8801(i2c_bus=i2c_bus)
#    while(tof.begin() != 0):
#      counter += 1
#      if counter > 100:
#          break
#      sleep(0.5)
#    tof.start_measurement(calib_m = tof.eMODE_NO_CALIB)
  
#   while True:
#     if(tof.is_data_ready() == True):
#       return tof.get_distance_mm()
#     counter += 1
#      if counter > 100:
#        break
#    return tof.get_distance_mm()

#def findbox():
