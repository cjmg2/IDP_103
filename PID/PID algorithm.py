def line_following(measurement, setpoint = [0, -1, 1, 0]):

    #needs to be adjusted
    Kp =

    #needs to be adjusted
    Ki = 0

    #needs to be adjusted
    Kd =

    #needs to be adjusted this is the derivative time constant
    tau = 

    #sampling rate of controller (I can choose)
    T = 

    #calculate list of errors
    errorlist = measurement - setpoint

    #calculate overall error
    for value in errorlist:
        error += value

    #calculate control signal
    proportional = Kp * error
    integrator = Ki * T/2 * (error + prev_error) + prev_integrator
    differentiator = Kd * 2/(2*tau + T) * (error - prev_error) + ((2 * tau - T)/(2 * tau + T)) * prev_differentiator
    control = proportional + integrator  + differentiator

    #send control signal
    return control, error, integrator, differentiator


#Move this section into a file with all the different states?

while state == line_following:
    
    #Calculate control signal
    temp = line_following(measurement, setpoint, prev_error, prev_integrator, prev_differentiator)

    #previous iteration
    prev_error = temp[1]
    prev_integrator = temp[2]
    prev_differentiator = temp[3]

    #get control signal
    signal = temp[0]