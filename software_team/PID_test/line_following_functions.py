from machine import Pin, PWM

##need to write proper import command
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

rmotor = Motor(4, 5)
lmotor = Motor(6, 7)

##Delete above once implemented properly





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
    L2 = Pin(16, Pin.IN, Pin.PULL_DOWN)
    L = Pin(17, Pin.IN, Pin.PULL_DOWN)
    R = Pin(18, Pin.IN, Pin.PULL_DOWN)
    R2 = Pin(19, Pin.IN, Pin.PULL_DOWN)
    
    
    return [L2.value(), L.value(), R.value(), R2.value()]

def motor_control(control_signal):
    if control_signal < 0:
        lmotor.Forward
        rmotor.off

    elif control_signal > 0:
        lmotor.off
        rmotor.Forward

    else:
        rmotor.Forward
        lmotor.Forward