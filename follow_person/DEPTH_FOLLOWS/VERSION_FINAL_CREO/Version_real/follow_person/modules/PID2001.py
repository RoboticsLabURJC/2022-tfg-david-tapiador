from ssl import ALERT_DESCRIPTION_UNEXPECTED_MESSAGE
import numpy as np
import math
from time import sleep

def main(inputs, outputs, parameters, synchronise):

    kp = parameters.read_number("Kp")
    ki = parameters.read_number("Ki")
    kd = parameters.read_number("Kd")

    previousError = 0
    I = 0
    max_rotation = 1
    enable = inputs.read_number('Enable')
    results = inputs.read_array("Inp")
    prev_results = results

    while(1):
        try:
            width = inputs.read_number("Width")
            if(width != None):
                break
        except Exception:
            continue

    print("WIDTH -> " + str(width))

    size_integral = 5       # Length of integral part of PID 
    Is = [None]*(size_integral+1)
    Is[-1] = 0

    while(1):
        enable = inputs.read_number('Enable')
        results = inputs.read_array("Inp")
        if(enable != 0):
            try:

                if(enable == 1):
                    error = float(results[0]+results[2]/2) - width/2
                    prev_results = results
                # sleep(0.1)

                P = error

                if(Is[size_integral] != size_integral):
                    Is[Is[size_integral]] = error
                    Is[size_integral] += 1
                    print("Hola xd")
                else:
                    for j in range(size_integral-1):
                        Is[j] = Is[j+1]
                        I =+ Is[j] / (size_integral-j) 
                    Is[size_integral-1] = error
                    I =+ Is[size_integral]
                    # This makes the latests errors the most significant ones, as
                    #   those are divided by the lowest numbers, being the actual one
                    #   divided by 0.
                



                # I = I + error
                D = float(error) - float(previousError)
                PIDvalue = (kp*P)  + (kd*D)#+ (ki*I)
                # PIDvalue = (kp*P)#  + (kd*D)#+ (ki*I)
                previousError = float(error)

                linear_velocity = 0.0
                angular_velocity = -PIDvalue
                if(angular_velocity > max_rotation or angular_velocity < -max_rotation):
                    angular_velocity = max_rotation*angular_velocity/abs(angular_velocity)

                data = [linear_velocity, 0,0,0,0, angular_velocity]
                outputs.share_array("Out", data)

                synchronise()
            except Exception:
                synchronise()
                continue