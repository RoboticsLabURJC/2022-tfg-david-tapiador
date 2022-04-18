import numpy as np
import math
from time import sleep
from utils.wires.wire_str import read_string, share_string
from utils.tools.freq_monitor import monitor_frequency

def loop(block_name, input_wires, output_wires, parameters, flags):

    input_0 = read_string(input_wires[0])
    output_0 = share_string(output_wires[0])

    kp = float(parameters[1])
    ki = float(parameters[2])
    kd = float(parameters[3])
    previousError, I = 0, 0

    enabled = False
    try:
        enable_wire = read_string(input_wires[1])
    except IndexError:
        enabled = True

    required_frequency, update = float(parameters[0]), 1
    control_data = np.array([0.0,0.03])

    if flags[0] == 1:
        monitor_frequency(block_name, control_data, required_frequency, update)

    try:
    
        while True:
        
            if enabled or (update := bool(enable_wire.get()[0])):

                msg = input_0.get()
                
                if msg is not None and msg[0] is not None:
                
                    error = float(msg[0])
                    sleep(0.01)
                    
                    # PID Control Logic
                    
                    P = error
                    I = I + error
                    D = error-previousError
                    PIDvalue = (kp*P) + (ki*I) + (kd*D)
                    previousError = error
            
                    linear_velocity = 5.0
            
                    angular_velocity = -PIDvalue
                    
                    data = []
                    data.extend((str(linear_velocity), str(angular_velocity)))
                    to_write = np.array(data, dtype='<U6')
                    output_0.add(to_write)
                    control_data[0] += 1
                    
            sleep(control_data[1])

    except KeyboardInterrupt:
    
        input_0.release()
        output_0.release()
        enable_wire.release()