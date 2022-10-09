import numpy as np
import math
from time import sleep

def main(inputs, outputs, parameters, synchronise):

    kp = parameters.read_number("Kp")
    ki = parameters.read_number("Ki")
    kd = parameters.read_number("Kd")

    previousError, I = 0, 0
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
    while(1):
        enable = inputs.read_number('Enable')
        results = inputs.read_array("Inp")
        if(enable != 0):
            try:

                if(enable == 1):
                    error = float(results[0]+results[2]/2) - width/2
                    prev_results = results
                else:
                    error = float(prev_results[0]+prev_results[2]/2) - width/2
                sleep(0.1)

                P = error
                I = I + error
                D = error - previousError
                PIDvalue = (kp*P)  + (kd*D)#+ (ki*I)
                previousError = error

                linear_velocity = 0.0
                angular_velocity = -PIDvalue

                print("LINEAR  ->" + str(linear_velocity) + "\nANGULAR ->" + str(angular_velocity) + "\nERROR   ->" + str(error) + "\nP\t->" + str(P) + "\nI\t->" + str(I) + "\nD\t->" + str(D))
                print()

                data = [linear_velocity, 0,0,0,0, angular_velocity]
                outputs.share_array("Out", data)

                synchronise()
            except Exception:
                synchronise()
                continue