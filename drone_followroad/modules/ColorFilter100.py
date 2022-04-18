import cv2 as cv
import numpy as np
from time import sleep
from utils.wires.wire_img import share_image, read_image
from utils.wires.wire_str import read_string
from utils.tools.freq_monitor import monitor_frequency

def loop(block_name, input_wires, output_wires, parameters, flags):

    input_0 = read_image(input_wires[0])
    output_0 = share_image(output_wires[0])
    lower_range = np.array([int(x.strip()) for x in parameters[1].split(',')])
    upper_range = np.array([int(x.strip()) for x in parameters[2].split(',')])

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
    
                frame = input_0.get()
                
                if frame is not None:
        
                    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
                    mask = cv.inRange(hsv, lower_range, upper_range)
                    filtered = cv.bitwise_and(frame,frame, mask= mask)
    
                    output_0.add(filtered)
    
                control_data[0] += 1
                
            sleep(control_data[1])
            
    except KeyboardInterrupt: 
    
        input_0.release()
        enable_wire.release()
        output_0.release()