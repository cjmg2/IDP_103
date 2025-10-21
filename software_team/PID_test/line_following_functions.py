from machine import Pin, PWM
from time import sleep_us

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

        ##delete above when done

def weighted(measurement):
    #gives appropriate weights to sensor values from inputed list of light sensor values
    return [measurement[0] * -2, measurement[1] * -1, measurement[2] * 1, measurement[3] * 2]

def errorcalc(weighted_measurement):
    #calculates error from the line 
    #use o/p of weighted for i/p and use o/p for i/p for line following

    #initialise
    temp = 0

    #setpoint is [0, 0, 0, 0] hence values are just added
    for value in weighted_measurement:
        temp += value
    return temp

def get_line_measurement():
    FL = Pin(18, Pin.IN, Pin.PULL_DOWN)
    L = Pin(19, Pin.IN, Pin.PULL_DOWN)
    R = Pin(17, Pin.IN, Pin.PULL_DOWN)
    FR = Pin(16, Pin.IN, Pin.PULL_DOWN)
    
    return [FL.value(), L.value(), R.value(), FR.value()]

def line_following(error, prev_error, prev_integrator, prev_differentiator, Kp=1, Ki=0, Kd=0.5, tau=0.1, T=0.01):
    #returns control signal, integrator and differentiator
    # T is the sampling time of the discrete controller in seconds
    # tau is the derivative low pass filter time constant

    #calculate control signal
    proportional = Kp * error
    integrator = Ki * T/2 * (error + prev_error) + prev_integrator

    #consider differentiator on mearuent rather than on error see video in notes
    differentiator = Kd * 2/(2*tau + T) * (error - prev_error) + ((2 * tau - T)/(2 * tau + T)) * prev_differentiator
    control = proportional + integrator  + differentiator

    #send control signal
    return control, integrator, differentiator

def motor_control(control_signal):
    if control_signal < 0:
        lmotor.Forward()
        rmotor.off()

    elif control_signal > 0:
        lmotor.off()
        rmotor.Forward()

    else:
        rmotor.Forward()
        lmotor.Forward()
        
def motor_control2(control_signal):
    k = 5
    if control_signal < 0:
        lmotor.Forward(k*control_signal)
        rmotor.Forward(100 - k*control_signal)

    elif control_signal > 0:
        rmotor.Forward(k*control_signal)
        lmotor.Forward(100 - k*control_signal)

    else:
        rmotor.Forward()
        lmotor.Forward()
        

rmotor = Motor(4, 5)
lmotor = Motor(7, 6)

state = "line following"

#Initialise
control = 0
prev_error = 0
prev_integrator = 0
prev_differentiator = 0

#while state == "line following":

#    measurement = get_line_measurement()
    
#    temp_error = errorcalc(measurement)

#    results = line_following(temp_error, prev_error, prev_integrator, prev_differentiator)

    #parse results
 #   control = results[0]
  #  prev_error = temp_error
   # prev_integrator = results[1]
    #prev_differentiator = results[2]

   # print(control)

   # motor_control(control)

rmotor.off()
lmotor.off()

