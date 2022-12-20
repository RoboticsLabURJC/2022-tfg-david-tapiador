import numpy as np
import math
from time import sleep

def main(inputs, outputs, parameters, synchronise):

    auto_enable = True
    try:
        enable = inputs.read_number("Enable")
    except Exception:
        auto_enable = True

    kp = parameters.read_number("Kp")
    ki = parameters.read_number("Ki")
    kd = parameters.read_number("Kd")

    previousError, I = 0, 0

    while(auto_enable or inputs.read_number('Enable')):
        msg = inputs.read_number("Inp")
        if msg is None:
            continue

        error = float(msg) - 1.5
        sleep(0.01)

        P = error
        I = I + error
        D = error - previousError
        PIDvalue = (kp*P) + (kd*D) #(ki*I) + 
        previousError = error

        linear_velocity = PIDvalue



        

        if msg == 0:
            linear_velocity = 0



        print("LINEAR  ->" + str(linear_velocity) +
                "\nERROR   ->" + str(error) +
                "\nP\t->" + str(kp*P) +
                "\nI\t->" + str(ki*I) +
                "\nD\t->" + str(kd*D))
        print()






        outputs.share_number("Out", linear_velocity)
        synchronise()