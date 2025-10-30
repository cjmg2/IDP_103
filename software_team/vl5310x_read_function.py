from machine import Pin, I2C
from libs.VL53L0X.VL53L0X import VL53L0X

def test_vl53l0x():
    #these lines can be in a seperate "initialise" function
    # config I2C Bus
    i2c_bus = I2C(id=0, sda=Pin(8), scl=Pin(9)) # I2C0 on GP8 & GP9
    # print(i2c_bus.scan())  # Get the address (nb 41=0x29, 82=0x52)
    
    # Setup vl53l0 object
    vl53l0 = VL53L0X(i2c_bus)
    vl53l0.set_Vcsel_pulse_period(vl53l0.vcsel_period_type[0], 18)
    vl53l0.set_Vcsel_pulse_period(vl53l0.vcsel_period_type[1], 14)

    #these lines should be in the function
    # Start device
    vl53l0.start()

    # Read one sample
    distance = vl53l0.read()
    print(f"Distance = {distance}mm")  # this is useful for testing but not necessary
    #sleep(0.5)
        
    # Stop device
    vl53l0.stop()
    return distance

if __name__ == "__main__":

    test_vl53l0x()
