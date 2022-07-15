import numpy as np
from time import sleep
from utils.wires.wire_str import read_string, share_string
from utils.tools.freq_monitor import monitor_frequency

def loop(block_name, input_wires, output_wires, parameters, flags):

    output_0 = share_string(output_wires[0])

    enabled = False
    try:
        enable_wire = read_string(input_wires[0])
    except IndexError:
        enabled = np.True_

    required_frequency, update = float(parameters[0]), 1
    control_data = np.array([0.0,0.03])

    if flags[0] == 1:
        monitor_frequency(block_name, control_data, required_frequency, update)

    try:

        while True:

            if enabled or (update := bool(enable_wire.get()[0])):
                vels = [0,0,0,0,0,1]
                to_write = np.array(vels, dtype='<U64')
                output_0.add(to_write)
                control_data[0] += 1
            
            sleep(control_data[1])       
    
    except KeyboardInterrupt:
        enable_wire.release()
        output_0.release()