Kp =
Ki =
Kd =
tau = 
T = 
def line_following():

    #calculate error
    error = measurement - setpoint


    #calculate control signal
    proportional = Kp * error
    integrator = Ki * T/2 * (error + prev_error) + prev_integrator
    differentiator = Kd * 2/(2*tau + T) * (error - prev_error) + ((2 * tau - T)/(2 * tau + T)) * prev_differentiator
    control = proportional + integrator  + differentiator

    #send control signal
    

    return control, error, integrator, differentiator


while state == line_following:
    
    #Calculate control signal
    line_following(measurement, setpoint, prev_error, prev_integrator, prev_differentiator)

    #previous iteration
    prev_error = error
    prev_integrator = integrator
    prev_differentiator = differentiator