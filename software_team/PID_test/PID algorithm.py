import software_team.PID_test.line_following_functions as lff

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




##temporary remove
state = "line_following"


##remove above



#initialise variables
control = 0
prev_error = 0
prev_integrator = 0
prev_differentiator = 0



#while state == "line_following":
    
#mm = lff.get_line_measurement()
###mm = [1,1,0,0]

    #calculate weighted
###wm = lff.weighted(mm)
    #calculate error
###error = lff.errorcalc(wm)
    #Calculate control signal
###results = line_following(error, prev_error, prev_integrator, prev_differentiator)

    #parse results
###control = results[0]
###prev_error = error
###prev_integrator = results[1]
###prev_differentiator = results[2]

    #use control signal
#lff.motor_control(control)

