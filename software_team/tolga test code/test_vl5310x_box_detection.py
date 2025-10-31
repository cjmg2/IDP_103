from machine import Pin, I2C
from libs.VL53L0X.VL53L0X import VL53L0X
from utime import sleep
import Global_Variables as gv

def test_vl53l0x():
    #Store previous values
    previous_values = [0,0,0,0,0,0,0,0,0,0]
    new_object_cutoff = 0.95
    # config I2C Bus
    i2c_bus = I2C(id=0, sda=Pin(8), scl=Pin(9), freq=400000) # I2C0 on GP8 & GP9
    print(i2c_bus.scan())  # Get the address (nb 41=0x29, 82=0x52)
    
    # Setup vl53l0 object
    vl53l0 = VL53L0X(i2c_bus)
    vl53l0.set_Vcsel_pulse_period(vl53l0.vcsel_period_type[0], 18)
    vl53l0.set_Vcsel_pulse_period(vl53l0.vcsel_period_type[1], 14)


    while True:
        # Start device
        vl53l0.start()

        # Read fifty samples
        for _ in range(50):
            distance = vl53l0.read()
            if distance <= ( sum(previous_values[0:(len(previous_values)//2)]) / (len(previous_values)//2) )*new_object_cutoff:
                print("Box Detected")
                
            for i in range(len(previous_values)-1):
                previous_values[i] = previous_values[i+1]
                previous_values[len(previous_values) - 1] = ultrasonic_value
            
            print(f"Distance = {distance}mm")  # Check calibration!
            sleep(0.2)
        
        # Stop device
        vl53l0.stop()


if __name__ == "__main__":
    test_vl53l0x()
