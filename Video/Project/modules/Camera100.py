import cv2
import numpy as np
from time import sleep
from utils.wires.wire_img import share_image
from utils.wires.wire_str import read_string
from utils.tools.freq_monitor import monitor_frequency

def loop(block_name, input_wires, output_wires, parameters, flags):

    output_0 = share_image(output_wires[0])

    enabled = False
    try:
        enable_wire = read_string(input_wires[0])
    except IndexError:
        enabled = True

    required_frequency, update = float(parameters[0]), 1
    control_data = np.array([0.0,0.03])

    if flags[0] == 1:
        monitor_frequency(block_name, control_data, required_frequency, update)

    cap = cv2.VideoCapture(0)

    try:
    
        while True:
    
            if enabled or (update := bool(enable_wire.get()[0])):
                
                control_data[0] += 1 
                ret, frame = cap.read()
                output_0.add(frame)
                
            sleep(control_data[1])
            
    except KeyboardInterrupt:
    
        cap.release()
        enable_wire.release()
        output_0.release()