from machine import Pin, PWM, SoftI2C, I2C
from utime import sleep
import Global_Variables as gv
from libs.tiny_code_reader.tiny_code_reader import TinyCodeReader

"""def get_servo_angle():
   """"""reads the analogue feedback of the servo to get the current angle""""""
   angle=gv.adc.read_u16()*0.47-33.4 #this is the function on the servo documentation to get the angle from the analogue output
   return angle"""

def change_height(target_level):
    servo_PWM = PWM(Pin(15), 100)
    u16_level = int(65535 * target_level / 100)
    servo_PWM.duty_u16(u16_level)

    #if target_level > current_level:
    #    direction = 1
    #if target_level < current_level:
    #    direction = -1
    #while current_level != target_level:
        
    #    u16_level = int(65535 * current_level / 100)
    #    servo_PWM.duty_u16(u16_level)
    
        #update level and sleep
    #    print(f"Level={current_level}, u16_level={u16_level}, direction={direction}")
    #    current_level += direction
    #    sleep(0.1)

def initialise_servo():
    change_height(6.2)

def lower_to_ground():
    change_height(6.2)

def lower_onto_rack():
    change_height(12)

def lift_block():
    change_height(14.5)




















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

#def get_f_distance():
#    """This function returns the forward distance"""
#    tof = DFRobot_TMF8701(i2c_bus=i2c_bus_0)
#
#    while(tof.begin() != 0):
#      counter += 1
#      if counter > 100:
#          break
#      sleep(0.5)
#    tof.start_measurement(calib_m = tof.eMODE_NO_CALIB, mode = tof.eCOMBINE)
    
#    while True:
#        if(tof.is_data_ready() == True):
#            return tof.get_distance_mm()
#        counter += 1
#        if counter > 100:
#            break
#    return tof.get_distance_mm()

#def detect_box():
#    """This function detects when within 5mm of a box"""
#    d = 5
#    if get_f_distance() < d:
#        return "at junction"

def get_qr_code():
    """This function gets a qr code"""
    gv.qr_enable.value(1)
    sleep(TinyCodeReader.TINY_CODE_READER_DELAY)
    sleep(0.1) #WE CAN SPEED THIS UP A BIT EXPERIMENTALLY
    code = gv.tiny_code_reader.poll()
    counter = 0
    while code == None and counter <= 10:
        sleep(TinyCodeReader.TINY_CODE_READER_DELAY)
        code = gv.tiny_code_reader.poll()
        counter += 1
    print(code)
    gv.qr_enable.value(0)
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


import Global_Variables as gv
import time

def button_to_start():
    while gv.Button.value() != 1:
        time.sleep(1)
    print("START!")

from machine import Pin, PWM

class Motor:
    def __init__(self, dirPin, PWMPin):
        self.mDir = Pin(dirPin, Pin.OUT)  # set motor direction pin
        self.pwm = PWM(Pin(PWMPin))  # set motor pwm pin
        self.pwm.freq(1000)  # set PWM frequency
        self.pwm.duty_u16(0)  # set duty cycle - 0=off
        
    def off(self):
        self.pwm.duty_u16(0)
        
    def Forward(self, speed=100):
        self.mDir.value(0)                     # forward = 0 reverse = 1 motor
        self.pwm.duty_u16(int(65535 * speed / 100))  # speed range 0-100 motor

    def Reverse(self, speed=30):
        self.mDir.value(1)
        self.pwm.duty_u16(int(65535 * speed / 100))
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

global junc_counter
junc_counter = 0
from machine import Pin, PWM
import time
import Box_Collection as bc
import Global_Variables as gv

def get_measurement_list():
    """"This function returns a list of light sensor reading"""
    
    return [gv.FL.value(), gv.L.value(), gv.R.value(), gv.FR.value()] # LOW = white HIGH = Black

def weight_measurement_list(measurement_list):
    """This function gives weights to a list of measurements equal to the sensor distances from the centre"""

    return [measurement_list[0] * -4, measurement_list[1] * -1.25, measurement_list[2] * 1.25, measurement_list[3] * 4] #update with weigtings equal to the distance of each sensor from the centre


def calc_error(weighted_measurement_list, setpoint=0):
    """This function calculates the distance from the centre then calculates the error from a setpoint"""

    temp = 0
    counter = 0 
    for value in weighted_measurement_list:
        if value != 0:
            temp += value
            counter += 1
    if counter != 0:
        measurement = temp / counter
    else:
        measurement = None
    return measurement

def calc_control_signal(error, prev_error, prev_integrator, prev_differentiator, Kp=40, Ki=0, Kd=0.1, tau=0.0005, T=0.05):
    """"This function calculates the control signal using a PID controller"""

    # To adjust first adjust Kp. Then adjust Ki. Then adjust Kd. If too much noise when Kd adjusted then adjust tau for more smoothing

    #calculate control signal
    proportional = Kp * error
    integrator = Ki * T/2 * (error + prev_error) + prev_integrator

    #consider differentiator on measurement rather than on error see video in notes
    differentiator = Kd * 2 * (error - prev_error)/(2*tau + T) + ((2 * tau - T)/(2 * tau + T)) * prev_differentiator
    control = proportional + integrator  + differentiator
    #print(control)
    #send control signal
    return control, integrator, differentiator

def motor_control(control_signal):
    """"This function controls motors proportionally to the control signal"""
    #print(measurement_list)
    k = 1
    if control_signal < 0:
        gv.lmotor.Forward(75 + k*control_signal)
        gv.rmotor.Forward(75 - k*control_signal)

    elif control_signal > 0:
        gv.rmotor.Forward(75 - k*control_signal)
        gv.lmotor.Forward(75 + k*control_signal)
    else:
        gv.lmotor.Forward(75)
        gv.rmotor.Forward(75)

    #else:
    #    gv.rmotor.Forward()
    #    gv.lmotor.Forward()
    #if measurement_list == [0, 1, 1, 0] or measurement_list == [0, 0, 0, 0]:
    #    gv.rmotor.Forward(80)
    #    gv.lmotor.Forward(80)
    #    return "not at junction"
    #if measurement_list == [1, 0, 0, 0]:
    #    gv.rmotor.Forward(100)
    #    gv.lmotor.Forward(60)
    #    return "not at junction"
    #if measurement_list == [0, 1, 0, 0]:
    #    gv.rmotor.Forward(100)
    #    gv.lmotor.Forward(40)
    #    return "not at junction"
    #if measurement_list == [0, 0, 1, 0]:
   #     gv.rmotor.Forward(40)
    #    gv.lmotor.Forward(100)
     #   return "not at junction"
    #if measurement_list == [0, 0, 0, 1]:
     #   gv.rmotor.Forward(60)
       # gv.lmotor.Forward(100)
      #  return "not at junction"
    #if measurement_list == [0, 0, 1, 1] or measurement_list == [1, 1, 1, 1]:
     #   gv.rmotor.off()
      #  gv.lmotor.off()
        #print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
       # return "at junction"
    #if measurement_list == [1, 1, 0, 0] or measurement_list == [1, 1, 1, 1]:
     #   gv.rmotor.off()
      #  gv.lmotor.off()
        #print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
       # return "at junction"

def detect_L_turn(measurement_list):
    """"This function detects if there is a left turn"""

    detection_list = [1*measurement_list[0], 1*measurement_list[1], 0*measurement_list[2], 0*measurement_list[3]]
    if detection_list == [1, 1, 0, 0]:
        return "at junction"

def detect_R_turn(measurement_list):
    """"This function detects if there is a right turn"""

    detection_list = [0*measurement_list[0], 0*measurement_list[1], 1*measurement_list[2], 1*measurement_list[3]]
    if detection_list == [0, 0, 1, 1]:
        return "at junction"

#def detect_dropoff(measurement_list):
#    """"This function detects if there is no line"""
#
#    if measurement_list == [0, 0, 0, 0]:
#        return "at junction"

#def detect_T_junction(measurement_list):             ### I believe this function is redundant due to detect_R_turn & detect_L_Turn
#    """"This function detects if there is a T junction"""
#
#    if measurement_list == [1, 1, 1, 1]:
#        return "at junction"

def junc_detection(measurement_list):
    if detect_R_turn(measurement_list) == "at junction" or detect_L_turn(measurement_list) == "at junction":
        gv.junc_counter += 1
        if gv.junc_counter > 5:
            return "at junction"
    else:
        return "not at junction"

def line_following(pickup = False, dropoff = False, blind=False, blind_time=0):
    """This function follows a line until a junction is detected"""
    
    gv.junc_counter = 0
    state = "not at junction"   
    prev_error = 0
    prev_integrator = 0
    prev_differentiator = 0
    control_signal = 0
    #qr_code_detected = False
    
    time_remaining = blind_time
    
    counter = 0
    
    while state == "not at junction":
        start_time = time.time_ns()
        time.sleep(0.05)
        measurement_list = get_measurement_list()
        counter += 1
        #print(measurement_list)
        #print(counter)
        weighted_measurement_list = weight_measurement_list(measurement_list)
        error = calc_error(weighted_measurement_list)
        if error == None:
            error = prev_error
        results = calc_control_signal(error, prev_error, prev_integrator, prev_differentiator)

        control_signal = results[0]
        prev_error = error
        prev_integrator = results[1]
        prev_differentiator = results[2]
        
        state = junc_detection(measurement_list)
        
        end_time = time.time_ns()
        
        #print(control_signal)

        motor_control(control_signal)
        #detect_R_turn(measurement_list)
        #detect_L_turn(measurement_list) # Do not need a detect T junction
        #print(state)
        #if dropoff == True:
         #   detect_dropoff(measurement_list)
        
        
        if blind == True:
            time_elapsed = end_time - start_time
            time_remaining = time_remaining - time_elapsed
            if time_remaining < 0:
                state = "blind finished"
        
    gv.rmotor.off()
    gv.lmotor.off()
        
        #if pickup == True:
            
        #    if qr_code_detected == False:
        #        qr_code = bc.get_qr_code()
        #        if qr_code is not None:
        #            qr_code_detected = True
            #bc.detect_box()
    
    #if pickup == True and qr_code_detected == True:
     #   return qr_code

def turn_clockwise(speed):
    """"This function turns the robot 90 degrees clockwise"""

    gv.rmotor.off()
    gv.lmotor.off()
    gv.rmotor.Reverse(speed)
    gv.lmotor.Forward(speed)
    if speed == 100:
        time.sleep(0.57)
    elif speed == 70:
        time.sleep(1.2)
    gv.rmotor.off()
    gv.lmotor.off()

def turn_anticlockwise(speed):
    """"This function turns the robot 90 degrees anticlockwise"""

    gv.rmotor.off()
    gv.lmotor.off()
    gv.rmotor.Forward(speed)
    gv.lmotor.Reverse(speed)
    if speed == 100:
        time.sleep(0.57)
    elif speed == 70:
        time.sleep(1.2)
    gv.rmotor.off()
    gv.lmotor.off()

def blind_forward(distance_wanted):
    """This function makes the robot move forwards a certain distance without taking into account the light sensors"""
    gv.rmotor.Forward(100)
    gv.lmotor.Forward(100)
    time.sleep(distance_wanted) #1cm goes to 18cm
    gv.rmotor.off()
    gv.lmotor.off()

def blind_reverse(distance_wanted):
    """This function makes the robot move forwards a certain distance without taking into account the light sensors"""
    gv.rmotor.Reverse(100)
    gv.lmotor.Reverse(100)
    time.sleep(distance_wanted) # 1s goes to 18cm
    gv.rmotor.off()
    gv.lmotor.off()

import Box_Collection
import Line_Following
import Button
import Global_Variables as gv
import time

SMALL = 3/20
CLOCK_SMALL = 4/20
TEMP_BLIND = 9/20
OUT_OF_HOME = 20/20
OUT_OF_BAY = 10/20
STEP_FWD = 40
TINY_QR_FWD = 1/20
OUT_OF_COLORED_BAYS = 10/20

connections = {
    "Home": {"Yellow": 270, "Green": 90},
    "Yellow": {"Red": 270, "Home": 90},
    "Green": {"Home": 270, "Blue": 90},
    "Red": {"L_purple": 180, "Yellow": 90},
    "Blue": {"L_orange": 180, "Green": 270},
    "L_orange": {"Blue": 0, "J_L_orange": 180},
    "L_purple": {"Red": 0, "J_L_purple": 180},
    "J_L_orange": {"L_orange": 0, "Ramp": 270},
    "J_L_purple": {"L_purple": 0, "Ramp": 90},
    "Ramp": {"U_T": 0, "J_L_orange": 90, "J_L_purple": 270},
    "U_T": {"J_U_orange": 90, "Ramp": 180, "J_U_purple": 270},
    "J_U_orange": {"U_orange": 180, "U_T": 270},
    "J_U_purple": {"U_purple": 180, "U_T": 90},
    "U_orange": {"J_U_orange": 0},
    "U_purple": {"J_U_purple": 0}
    }

path_det = {
    "Home": 5,
    "Yellow": 6,
    "Green": 4,
    "Red": 7,
    "Blue": 3,
    "L_purple": 8,
    "L_orange": 2,
    "Ramp": None
}

class State:
    """
    global class containing all information about the state of the robot
    self.loc: location of the robot
    self.orien: orientation of the robot, with 0 degrees meaning the robot points towards the side of the map with the four colored loading/unloading bays
    self.destination: destination of the robot at the moment, which of the four shelf the robot will be depositing the box it is carrying
    self.bay: which exact bay, out of six, does the box belong to within each row of shelves
    self.remaining_boxes: contains the bays which still have not yet been unloaded in phase 1
    """

    def __init__(self, loc, orien):
        self.loc = loc
        self.orien = orien
        self.destination = None
        self.bay = None
        self.remaining_boxes = ["Red", "Blue", "Green", "Yellow"]
        self.phase = 1
        

global state
state = State("Home", 180)

def crashed(phase):
    state.loc = "Home"
    state.orien = 180
    state.phase = phase

def mini_path_find(start, dest, min_max):
    """
    pathfinds a route from loading/unloading bay to a desired shelf by finding the shortest path.
    The shortest path is determined by the starting position, and from this the robot decides to go clockwise or anticlockwise
    """

    queue = [start]
    while start != dest:
        branches = list(connections[start].keys())
        if min_max == "min":
            start = min(branches, key = lambda branches: path_det[branches])
        elif min_max == "max":
            start = max(branches, key = lambda branches: path_det[branches])
            
        queue.append(start)
    print(queue)
    return queue

def path_find(start, dest):
    """
    pathfinds from a loading/unlaoding bay to the desired shelf
    outputs an array with all the nodes to pass
    """

    if dest == "L_orange":
        return mini_path_find(start, dest, "min")
    elif dest == "L_purple":
        return mini_path_find(start, dest, "max")
    elif dest == "U_purple" or dest == "U_orange":
        if start == "Red" or start == "Yellow":
            queue = mini_path_find(start, "L_purple", "max")
            queue.append("J_L_purple")
        elif start == "Green" or start == "Blue":
            queue = mini_path_find(start, "L_orange", "min")
            queue.append("J_L_orange")
        else:
            raise Exception("error 2, elifs ran out")
        queue.append("Ramp")
        queue.append("U_T")
        queue.append("J_" + dest)
        queue.append(dest)
        return queue
        
    else:
        raise Exception("error 1, elifs ran out")
    



def fwd_until_junc():
    Line_Following.line_following(pickup=False, dropoff=False)

def clockwise(complete=False, speed = 100):
    Line_Following.turn_clockwise(speed)
    if complete == False:
        Line_Following.blind_forward(CLOCK_SMALL)

def anticlockwise(complete=False, speed = 100):
    Line_Following.turn_anticlockwise(speed)
    if complete == False:
        Line_Following.blind_forward(CLOCK_SMALL)

def load_fork():
    Box_Collection.lift_block()

def unload_fork():
    if state.destination == "U_orange" or state.destination == "U_purple":
        Box_Collection.lower_to_ground()
    elif state.destination == "L_orange" or state.destination == "L_purple":
        Box_Collection.lower_onto_rack()

def fwd_until_black():
    Line_Following.line_following(blind = True, blind_time = 2 * 1000000000)

def fwd_until_box():
    Line_Following.line_following(pickup=True, dropoff=False)

def fwd(distance):
    Line_Following.blind_forward(distance_wanted = distance)

def is_RHS_lidar_pos():
    pass

def is_LHS_lidar_pos():
    pass

def rvs(distance):
    Line_Following.blind_reverse(distance_wanted = distance)

def parse_qr(text):

    translator = {
        "A": "orange",
        "B": "purple",
        "upper": "U",
        "lower": "L"
    }

    # Split the string by commas and strip any extra spaces
    parts = [part.strip() for part in text.split(',')]

    # Extract the required parts
    rack = parts[0].split()[1]
    level = parts[1]
    position = parts[2]

    destination = translator[level.lower()] + "_" + translator[rack.upper()]
    return destination, int(position)

def count_unload_return():
    """
    counts how many bays it has moved past and turns into the desired bay.
    tells robot to unload and return back to original position
    """
    print(state.bay)
    counter = 0
    if state.destination == "U_purple" or state.destination == "L_orange":
        dest_general = 7 - state.bay
    else:
        dest_general = state.bay
    print(dest_general)
    while counter < dest_general:
        fwd_until_junc()
        fwd(SMALL)
        print(counter)
        counter += 1
    turn_unload_return(dest_general)

def execute_travel(route):
    """
    Tells the robot to move according to the route provided.
    Contains code to ignore loading bay lines on the bottom floor is the target destination is on the top floor
    """
    destination = route[-1]
    output = route.copy()
    next_node = route.pop(0)
    while route:
        current_node = next_node
        next_node = route.pop(0)
        print(current_node, next_node)
        wanted_orien = connections[current_node][next_node]
        #clockwise is positive
        turn_angle = wanted_orien - state.orien
        if turn_angle == 90 or turn_angle == -270:
            clockwise()
            state.orien = (state.orien + 90) % 360
        elif turn_angle == -90 or turn_angle == 270:
            anticlockwise()
            state.orien = (state.orien - 90) % 360
        elif turn_angle == 180 or turn_angle == -180:
            clockwise(complete = True)
            clockwise()
            state.orien = (state.orien + 180) % 360
        elif turn_angle == 0 or turn_angle == 360 or turn_angle == -360:
            fwd(SMALL)
        if {current_node, next_node} in [{"Blue", "L_orange"}, {"Red", "L_purple"}] and not state.destination in ["L_purple", "L_orange"]:
            for i in range(7):
                fwd_until_junc()
                fwd(SMALL)
        fwd_until_junc()
        state.loc = next_node
        print(turn_angle)
    # print("\n\n\n\n")
    return output

def return_to_color(path_fwd):
    """
    instructs the robot to move back to the colored loading/unloading bays from its current location
    """
    path_rvs = path_fwd[::-1]
    while path_rvs[-2] in ["Red", "Yellow", "Green", "Blue"]:
        print(path_rvs)
        path_rvs.pop()
    execute_travel(path_rvs)


def phase_1_find_box():
    """
    starting at either Red or Blue pointing to 0 degrees, make the robot go to the nearest bay with a box and turn to face the box
    """
    color_order = ["Red", "Yellow", "Green", "Blue"]
    if state.loc == "Red":
        i = 0
        while not state.loc in state.remaining_boxes:
            if i == 0:
                clockwise()
            fwd_until_junc()
            color_order.pop(0)
            state.loc = color_order[0]
            i += 1
        if i != 0:
            anticlockwise()

    elif state.loc == "Blue":
        color_order = color_order[::-1]
        i = 0
        while not state.loc in state.remaining_boxes:
            if i == 0:
                anticlockwise()
            fwd_until_junc()
            color_order.pop(0)
            state.loc = color_order[0]
            i += 1
        if i != 0:
            clockwise()
    else:
        raise Exception("error sth, elifs ran out")

def go_in_for_the_box_readqr():
    """
    with the bot facing the box, go straight in for the box, scan the qr code, lift the box, and move back to initial position
    """
    fwd(SMALL)
    text = None
    counter = 0
    while text == None and counter < 50:
        counter += 1
        text = Box_Collection.get_qr_code()
        Line_Following.line_following(blind = True, blind_time = 0.2 * 1000000000)
    Line_Following.line_following()
    destination, bay = parse_qr(text)
    Line_Following.blind_forward(TEMP_BLIND)
    load_fork()
    time.sleep(0.3)
    rvs(OUT_OF_COLORED_BAYS)
    if state.loc == "Red" or state.loc == "Yellow":
        clockwise(complete = True, speed = 70)
        clockwise(speed = 70)
    elif state.loc == "Blue" or state.loc == "Green":
        anticlockwise(complete = True, speed = 70)
        anticlockwise(speed = 70)
    
    fwd_until_junc()
    state.orien = 180
    state.remaining_boxes.remove(state.loc)
    return destination, bay

def phase_2_detect_boxes():
    """
    moves from bay to bay, using the lidar sensor to detect whether a box is present in that bay
    """

    color_order = ["Red", "Yellow", "Green", "Blue"]
    if state.loc == "Red":
        clockwise()
        while not is_LHS_lidar_pos():
            color_order.pop(0)
            if not color_order:
                print("NO BOXES DETECTED")
                anticlockwise()
                phase_2_detect_boxes()
            fwd_until_junc()
            state.loc = color_order[0]
        anticlockwise()

    elif state.loc == "Blue":
        color_order = color_order[::-1]
        anticlockwise()
        while not is_RHS_lidar_pos():
            color_order.pop(0)
            if not color_order:
                print("NO BOXES DETECTED")
                anticlockwise()
                phase_2_detect_boxes()
            fwd_until_junc()
            state.loc = color_order[0]
        clockwise()
    else:
        raise Exception("error sth, elifs ran out")


def turn_unload_return(bay):
    """
    Instructs the robot to turn, move towards the shelf, unload and return to the initial position
    """
    
    if state.destination == "U_purple" or state.destination == "L_orange":
        clockwise()
    elif state.destination == "L_purple" or state.destination == "U_orange":
        anticlockwise()
    else:
        raise Exception("error 3, elifs ran out")
    fwd_until_black()
    unload_fork()

    rvs(OUT_OF_BAY)
    clockwise(complete = True)
    clockwise()
    fwd_until_junc()
    if state.destination == "U_purple" or state.destination == "L_orange":
        anticlockwise()
    elif state.destination == "L_purple" or state.destination == "U_orange":
        clockwise()
    else:
        raise Exception("error 3, elifs ran out")
    state.orien = 0
    if bay != 1:
        for i in range(bay-1):
            fwd_until_junc()
    fwd(SMALL)
    #this is a very fragile part of the code, the bot has to turn quite accurately

def start_at_yellow():
    """
    Instructs the robot to move from home to yellow, the first loading bay
    """

    fwd_until_junc()
    gv.led_enable.value(1)
    fwd(SMALL)
    fwd_until_junc()
    clockwise()
    fwd_until_junc()
    clockwise()
    state.loc = "Yellow"
    state.orien = 0


def main():
    """
    Runs the entire program, telling the robot to do phase 1 (boxes in all 4 bays)
    then phase 2 (boxes only added one by one to a random loading bay)
    """
    
    gv.rmotor.off()
    gv.lmotor.off()

    Button.button_to_start()
    
    Box_Collection.initialise_servo()

    for q in range(4):
        if q == 0:
            start_at_yellow()
        else:
            phase_1_find_box()
        try:
            state.destination, state.bay = go_in_for_the_box_readqr()
        except:
            crashed()
            break
        route = path_find(state.loc, state.destination)
        try:
            route = execute_travel(route)
            count_unload_return()
            return_to_color(route)
        except:
            crashed()
            break
        
        

    for p in range(90):
        try:
            phase_2_detect_boxes()
        except:
            crashed()
            break
        try:
            state.destination, state.bay = go_in_for_the_box_readqr()
        except:
            crashed()
            break
        try:
            route = path_find(state.loc, state.destination)
            route = execute_travel(route)
            count_unload_return()
            return_to_color(route)
        except:
            crashed()
            break

import logic_algorithm as la
import Line_Following as lf

la.main()
#lf.line_following()

