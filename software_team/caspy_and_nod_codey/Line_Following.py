from machine import Pin, PWM
import time
import Box_Collection as bc

def get_measurement_list():
    """"This function returns a list of light sensor reading"""

    FL = Pin(18, Pin.IN, Pin.PULL_DOWN)
    L = Pin(19, Pin.IN, Pin.PULL_DOWN)
    R = Pin(17, Pin.IN, Pin.PULL_DOWN)
    FR = Pin(16, Pin.IN, Pin.PULL_DOWN)
    
    return [FL.value(), L.value(), R.value(), FR.value()] # LOW = white HIGH = Black

def weight_measurement_list(measurement_list):
    """This function gives weights to a list of measurements equal to the sensor distances from the centre"""

    return [measurement_list[0] * -2, measurement_list[1] * -1, measurement_list[2] * 1, measurement_list[3] * 2] #update with weigtings equal to the distance of each sensor from the centre


def calc_error(weighted_measurement_list, setpoint=0):
    """This function calculates the distance from the centre then calculates the error from a setpoint"""

    temp = 0
    counter = 0 
    for value in weighted_measurement_list:
        if value != 0:
            temp += value
            counter += 1
    measurement = temp / counter
    return measurement - setpoint

def calc_control_signal(error, prev_error, prev_integrator, prev_differentiator, Kp=1, Ki=0, Kd=0.5, tau=0.1, T=0.01):
    """"This function calculates the control signal using a PID controller"""

    #calculate control signal
    proportional = Kp * error
    integrator = Ki * T/2 * (error + prev_error) + prev_integrator

    #consider differentiator on measurement rather than on error see video in notes
    differentiator = Kd * 2/(2*tau + T) * (error - prev_error) + ((2 * tau - T)/(2 * tau + T)) * prev_differentiator
    control = proportional + integrator  + differentiator

    #send control signal
    return control, integrator, differentiator

def motor_control(control_signal):
    """"This function controls motors proportionally to the control signal"""

    k = 8
    if control_signal < 0:
        lmotor.Forward(k*control_signal)
        rmotor.Forward(100 - k*control_signal)

    elif control_signal > 0:
        rmotor.Forward(k*control_signal)
        lmotor.Forward(100 - k*control_signal)

    else:
        rmotor.Forward()
        lmotor.Forward()

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

def detect_dropoff(measurement_list):
    """"This function detects if there is no line"""

    if measurement_list == [0, 0, 0, 0]:
        return "at junction"

def detect_T_junction(measurement_list):
    """"This function detects if there is a T junction"""

    if measurement_list == [1, 1, 1, 1]:
        return "at junction"

def detect_junction(measurement_list):
    """"This function detects any junction excluding pickup"""

    detect_L_turn(measurement_list)
    detect_R_turn(measurement_list)
    detect_T_junction(measurement_list)

def line_following(pickup = False, dropoff = False):
    """This function follows a line until a junction is detected"""
    
    state = "not at junction"   
    prev_error = 0
    prev_integrator = 0
    prev_differentiator = 0
    control_signal = 0

    while state == "not at junction":

        measurement_list = get_measurement_list()
        weighted_measurement_list = weight_measurement_list(measurement_list)
        error = calc_error(weighted_measurement_list)
        results = calc_control_signal(error, prev_error, prev_integrator, prev_differentiator)

        control_signal = results[0]
        prev_error = error
        prev_integrator = results[1]
        prev_differentiator = results[2]

        motor_control(control_signal)
        detect_junction(measurement_list)

        if dropoff == True:
            detect_dropoff(measurement_list)
        
        if pickup == True:
            bc.detect_box()

def turn_clockwise():
    """"This function turns the robot 90 degrees clockwise"""

    rmotor.stop()
    lmotor.forward()
    time.sleep(1)
    lmotor.stop()

def turn_anticlockwise():
    """"This function turns the robot 90 degrees anticlockwise"""

    rmotor.forward()
    lmotor.stop()
    time.sleep(1)
    rmotor.stop()