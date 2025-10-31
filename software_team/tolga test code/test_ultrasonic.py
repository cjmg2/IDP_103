from machine import Pin, ADC
from time import sleep

#ultrasonic sensor initialization
ultrasonic = ADC(Pin(26))

#Store previous values
previous_values = [0,0,0,0,0,0,0,0,0,0]
new_object_cutoff = 0.95

while True:
    ultrasonic_value = ultrasonic.read_u16() # read value, 0-65535 across voltage range 0.0v - 3.3v
    
    #Check to see if the current value is less than new_object_cutoff times the average of the first half of the previous stored values
    #this way if there a constant change past the cutoff, it should return that there is a new value for 5 iterations before the average starts rising
    if ultrasonic_value <= ( sum(previous_values[0:(len(previous_values)//2)]) / (len(previous_values)//2) )*new_object_cutoff:
        print("Box Detected")
    
    #Shift all the previous values by one
    for i in range(len(previous_values)-1):
        previous_values[i] = previous_values[i+1]
    previous_values[len(previous_values) - 1] = ultrasonic_value
    
    print(ultrasonic_value)
    
    sleep(0.1)