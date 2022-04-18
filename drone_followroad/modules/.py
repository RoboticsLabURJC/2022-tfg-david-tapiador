import cv2 as cv
import numpy as np
import math
from time import sleep
from utils.wires.wire_img import read_image
from utils.wires.wire_str import share_string
from utils.tools.freq_monitor import monitor_frequency

def loop(block_name, input_wires, output_wires, parameters, flags):

    input_0 = read_image(input_wires[0])
    output_0 = share_string(output_wires[0])

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
        center = 0
        cx = 0
        cy = 0
        while True:
        
            if enabled or (update := bool(enable_wire.get()[0])):

                img = input_0.get()
                center = (img.shape)[1]/2
                
                if msg is not None and msg[0] is not None:

                    mascara = cv2.morphologyEx(mascara,cv2.MORPH_OPEN,kernel)
                    mascara = cv2.morphologyEx(mascara,cv2.MORPH_CLOSE,kernel)


                    contours, hierarchy = cv2.findContours(mascara, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

                    if len(contours)>0:
                        mayor_contorno=max(contours, key=cv2.contourArea)

                        momentos = cv2.moments(mayor_contorno)
                        cx = float(momentos['m10']/momentos['m00'])


                    to_write = String(center - cx)
                    output_0.add(to_write)
                    control_data[0] += 1
                    
            sleep(control_data[1])

    except KeyboardInterrupt:
    
        input_0.release()
        output_0.release()
        enable_wire.release()