def apply_weight(measurement):
    #Scale the list of mesurments to get a weighted list (left defined as negative and right side positive)
    wmm = [measurement[0] * (-2), measurement[1] * (-1), measurement[2] * 1, measurement[3] * 2]
    return wmm

measurement = [1, 1, 1, 0]

#print(apply_weight(measurement))

error = 0
errorlist = apply_weight(measurement)

for value in errorlist:
        error += value


print(error)

