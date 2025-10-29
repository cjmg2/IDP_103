import Line_Following as lf
import Global_Variables as gv

def test_line_following():
    while True:
        measurement_list = lf.get_measurement_list
        if measurement_list == [0, 1, 1, 0]:
            gv.rmotor.Forward(100)
            gv.lmotor.Forward(100)
        elif measurement_list == [0, 1, 0, 0]:
            gv.rmotor.Forward(75)
            gv.lmotor.Forward(100)
        elif measurement_list == [0, 0, 1, 0]:
            gv.rmotor.Forward(100)
            gv.lmotor.Forward(75)
        elif measurement_list == [1, 0, 0, 0]:
            gv.rmotor.Forward(50)
            gv.lmotor.Forward(75)
        elif measurement_list == [0, 0, 0, 1]:
            gv.rmotor.Forward(75)
            gv.lmotor.Forward(50)
        else:
            pass

        if lf.detect_junction() == "at junction":
            gv.rmotor.off()
            gv.lmotor.off()

if __name__ == "__main__":
    test_line_following()