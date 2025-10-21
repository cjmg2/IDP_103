#from machine import Pin, PWM

def get_measurement_list():
    FL = Pin(18, Pin.IN, Pin.PULL_DOWN)
    L = Pin(19, Pin.IN, Pin.PULL_DOWN)
    R = Pin(17, Pin.IN, Pin.PULL_DOWN)
    FR = Pin(16, Pin.IN, Pin.PULL_DOWN)
    
    return [FL.value(), L.value(), R.value(), FR.value()]

def weight_measurement_list(measurement_list):
    #gives appropriate weights to sensor values from inputed list of light sensor values
    return [measurement_list[0] * -2, measurement_list[1] * -1, measurement_list[2] * 1, measurement_list[3] * 2]


def calc_error(weighted_measurement_list, setpoint=0):

    temp = 0
    counter = 0 

    for value in weighted_measurement_list:
        if value != 0:
            temp += value
            counter += 1
    
    measurement = temp / counter

    return measurement - setpoint

def calc_control_signal(error, prev_error, prev_integrator, prev_differentiator, Kp=1, Ki=0, Kd=0.5, tau=0.1, T=0.01):

    #calculate control signal
    proportional = Kp * error
    integrator = Ki * T/2 * (error + prev_error) + prev_integrator

    #consider differentiator on mearuent rather than on error see video in notes
    differentiator = Kd * 2/(2*tau + T) * (error - prev_error) + ((2 * tau - T)/(2 * tau + T)) * prev_differentiator
    control = proportional + integrator  + differentiator

    #send control signal
    return control, integrator, differentiator

def motor_control(control_signal):
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

def Follow_line():
    state = "not at junction"
    
    while state == "not at junction":
        
        prev_error = 0
        prev_integrator = 0
        prev_differentiator = 0
        control_signal = 0
        
        
        measurement_list = get_measurement_list()

        weighted_measurement_list = weight_measurement_list(measurement_list)
    
        error = calc_error(weighted_measurement_list)

        results = calc_control_signal(error, prev_error, prev_integrator, prev_differentiator)

        control_signal = results[0]
        prev_error = error
        prev_integrator = results[1]
        prev_differentiator = results[2]

        motor_control(control_signal)
        #detect(junction)