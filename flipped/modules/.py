import cv2 as cv
import numpy as np
from time import sleep
from utils.wires.wire_img import share_image, read_image
from utils.wires.wire_str import read_string
from utils.tools.freq_monitor import monitor_frequency

def loop(block_name, input_wires, output_wires, parameters, flags):

    input_0 = read_image(input_wires[0])
    output_0 = share_image(output_wires[0])

    enabled = False
    try:
        enable_wire = read_string(input_wires[1])
    except IndexError:
        enabled = True

    
    required_frequency, update = float(parameters[0]), 1
    control_data = np.array([0.0,0.03])
    
    first_time = True
    if flags[0] == 1:
        monitor_frequency(block_name, control_data, required_frequency, update)

    try:
        while True:
        
            if enabled or (update := bool(enable_wire.get()[0])):
    
                frame = input_0.get()

                
                if frame is not None:
                    frame[:,:,0] = np.rot90(frame[:,:,0], k=2, axes=(0,1))
                    frame[:,:,1] = np.rot90(frame[:,:,1], k=2, axes=(0,1))
                    frame[:,:,2] = np.rot90(frame[:,:,2], k=2, axes=(0,1))

                    output_0.add(frame)
    
                control_data[0] += 1
                
            sleep(control_data[1])
            
    except KeyboardInterrupt: 
    
        input_0.release()
        enable_wire.release()
        output_0.release()