import cv2
import time
import numpy as np
from time import sleep
from utils.wires.wire_img import share_image, read_image
from utils.wires.wire_str import read_string
from utils.tools.freq_monitor import monitor_frequency

className = []
classesFile = 'utils/models/yolov3/yolov3.txt'

with open(classesFile,'rt') as f:
        className = f.read().rstrip('\n').split('\n')

def findObjects(outputs, img):

    confThreshold = 0.3
    nmsThreshold = 0.3
    hT, wT, cT = img.shape
    bbox = []
    classIds = []
    confs = []

    for output in outputs:
    
        for det in output:
            scores = det[5:]
            classId = np.argmax(scores)
            confidence = scores[classId]
            if confidence > confThreshold:
                w,h = int(det[2] * wT), int(det[3] * hT)
                x,y = int((det[0]*wT) - w/2), int((det[1]*hT) - h/2)
                bbox.append([x,y,w,h])
                classIds.append(classId)
                confs.append(float(confidence))
    
    indices = cv2.dnn.NMSBoxes(bbox, confs, confThreshold, nmsThreshold)
    for i in indices:
        box = bbox[i]
        x,y,w,h = box[0],box[1],box[2],box[3]
        cv2.rectangle(img,(x,y),(x+w, y+h),(255,0,255),2)
        cv2.putText(img,f'{className[classIds[i]].upper()} {int(confs[i]*100)}%',
                    (x,y-10),cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,0,255),2)
                
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
    
    if flags[0] == 1:
        monitor_frequency(block_name, control_data, required_frequency, update)
    
    whT = 320

    modelConfiguration = 'utils/models/yolov3/yolov3-tiny.cfg'
    modelWeights = 'utils/models/yolov3/yolov3-tiny.weights'

    net = cv2.dnn.readNetFromDarknet(modelConfiguration,modelWeights)
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    net.setPreferableTarget(cv2.dnn. DNN_TARGET_CPU)

    try:
    
        while True:
        
            if enabled or (update := bool(enable_wire.get()[0])):

                frame = input_0.get()
                
                if frame is not None:    

                    #converting img to blob
                    blob = cv2.dnn.blobFromImage(frame, 1/255,(whT,whT),[0,0,0],1, crop = False)
            
                    #Passing blob to network
                    net.setInput(blob)

                    layerNames = net.getLayerNames()
                    outputNames = [layerNames[i-1] for i in net.getUnconnectedOutLayers()]
            
                    #forward Pass
                    outputs = net.forward(outputNames)
                    findObjects(outputs,frame)

                    output_0.add(frame)
                    control_data[0] += 1

            sleep(control_data[1])
            
    except KeyboardInterrupt: 
    
        input_0.release()
        enable_wire.release()
        output_0.release()