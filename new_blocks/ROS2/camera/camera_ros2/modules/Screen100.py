import cv2
import numpy as np
from time import sleep
from utils.wires.wire_img import read_image
from utils.wires.wire_str import read_string
from utils.tools.freq_monitor import monitor_frequency

def loop(block_name, input_wires, output_wires, parameters, flags):

    input_0 = read_image(input_wires[0])

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
        
                control_data[0] += 1
                img = input_0.get()
                
                if img is not None:
                    cv2.imshow(block_name, img)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

            sleep(control_data[1])

    except KeyboardInterrupt:
    
        input_0.release()
        enable_wire.release()