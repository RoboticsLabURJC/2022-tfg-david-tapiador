from distutils.command.install_egg_info import to_filename
import cv2
import numpy as np
import time

className = []
classIds = []
bbox = []
classesFile = 'utils/models/yolov3/yolov3.txt'

with open(classesFile,'rt') as f:
    className = f.read().rstrip('\n').split('\n')

def findObjects(outputs, img):
    
    global classIds
    global bbox

    classIds = []
    bbox = []

    confThreshold = 0.3
    nmsThreshold = 0.3
    hT, wT, cT = img.shape
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
    
    for i in range(len(indices)):
        box = bbox[i]
        x,y,w,h = box[0],box[1],box[2],box[3]
        cv2.rectangle(img,(x,y),(x+w, y+h),(255,0,255),2)
        cv2.putText(img,f'{className[classIds[i]].upper()} {int(confs[i]*100)}%',
                    (x,y-10),cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,0,255),2)
           
def main(inputs, outputs, parameters, synchronise):
    auto_enable = True
    try:
        enable = inputs.read_number("Enable")
    except Exception:
        auto_enable = True
    
    whT = 320

    modelConfiguration = 'utils/models/yolov3/yolov3-tiny.cfg'
    modelWeights = 'utils/models/yolov3/yolov3-tiny.weights'

    net = cv2.dnn.readNetFromDarknet(modelConfiguration,modelWeights)
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

    while(1):
        try:
            frame = inputs.read_image("Img IN")
        except Exception:
            continue
    
        if frame is None:
            continue

        #converting img to blob
        blob = cv2.dnn.blobFromImage(frame, 1/255,(whT,whT),[0,0,0],1, crop = False)

        #Passing blob to network
        net.setInput(blob)

        layerNames = net.getLayerNames()
        outputNames = []
        outLayers = net.getUnconnectedOutLayers()
        
        for i in range(len(outLayers)):
            outputNames.append(layerNames[outLayers[i] - 1])

        #forward Pass
        results = net.forward(outputNames)
        findObjects(results,frame)

        #print("results -> ")

        is_person = False
        for i in classIds:
            #print(className[i])
            if(className[i] == "person"):
                is_person = True
                break
        to__send = [-1,-1,-1,-1]
        if(is_person):
            to__send = bbox[i]

        outputs.share_image("Img OUT", frame)
        outputs.share_array("Results1", to__send)
        outputs.share_array("Results2", to__send)
        synchronise()
