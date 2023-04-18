import cv2
import numpy as np
import math

def main(inputs, outputs, parameters, synchronise):

    x = [-3,27]
    y = [0,30]

    w = 900
    h = 900

    img = np.zeros([h,w,3],dtype=np.uint8)
    img.fill(255)
    lines = 30
    for i in range(lines+1):
        cv2.line(img, (int(img.shape[1]/(lines))*i, 0), (int(img.shape[1]/lines)*i, img.shape[0]), color=(0, 0, 0), thickness=2)
        cv2.line(img, (0, int(img.shape[1]/(lines))*i), (img.shape[0], int(img.shape[1]/lines)*i), color=(0, 0, 0), thickness=2)

    #Down left (-2,0)
    cv2.putText(img, str(x[0]), (-int(w/(lines)*0.1),h-int(h/(lines)*0.5)), cv2.FONT_ITALIC, 0.4, (255, 0, 0), 1)
    cv2.putText(img, str(y[0]), (int(w/(lines)*0.6),h-int(h/(lines)*0.2)), cv2.FONT_ITALIC, 0.4, (0, 0, 255), 1)

    #Down right (-2,30)
    cv2.putText(img, str(x[0]), (w-int(w/(lines)*0.7),h-int(h/(lines)*0.5)), cv2.FONT_ITALIC, 0.4, (255, 0, 0), 1)
    cv2.putText(img, str(y[1]), (w-int(w/(lines)*0.9),h-int(h/(lines)*0.2)), cv2.FONT_ITALIC, 0.4, (0, 0, 255), 1)

    #Top left (28,0)
    cv2.putText(img, str(x[1]), (int(w/(lines)*0.1),int(h/(lines)*0.9)), cv2.FONT_ITALIC, 0.4, (255, 0, 0), 1)
    cv2.putText(img, str(y[0]), (int(w/(lines)*0.6),int(h/(lines)*0.4)), cv2.FONT_ITALIC, 0.4, (0, 0, 255), 1)

    #Top right (28,30)
    cv2.putText(img, str(x[1]), (w-int(w/(lines)*0.7),int(h/(lines)*0.9)), cv2.FONT_ITALIC, 0.4, (255, 0, 0), 1)
    cv2.putText(img, str(y[1]), (w-int(w/(lines)*0.9),int(h/(lines)*0.4)), cv2.FONT_ITALIC, 0.4, (0, 0, 255), 1)

    while True:
        temp = img.copy()
        odom = inputs.read_array("Odom")
        dest = inputs.read_array("Dest")
        rep = inputs.read_number("RepForce")
        attr = inputs.read_number("AttrForce")
        try:
            if odom[0] != None and dest[0] != None and rep != None and attr != None:
                cv2.putText(temp, str([round(odom[0],2),round(odom[1],2)]), (int((odom[0]-x[0])*(w/lines)),int(h-(odom[1]-y[0])*(h/lines))), cv2.FONT_ITALIC, 0.7, (255, 0, 0), 2)
                
                cv2.circle(temp, (int((odom[0]-x[0])*(w/lines)),int(h-(odom[1]-y[0])*(h/lines))), 10, (255, 0, 0), -1)

                cv2.putText(temp, str([round(dest[0],2),round(dest[1],2)]), (int((dest[0]-x[0])*(w/lines)),int(h-(dest[1]-y[0])*(h/lines))), cv2.FONT_ITALIC, 0.7, (0, 0, 255), 2)
                cv2.circle(temp, (int((dest[0]-x[0])*(w/lines)),int(h-(dest[1]-y[0])*(h/lines))), 10, (0, 0, 255), -1)

                cv2.arrowedLine(temp, (int((odom[0]-x[0])*(w/lines)),int(h-(odom[1]-y[0])*(h/lines))), (int(math.cos(math.radians(odom[2]+90))*rep*40*1.4+(odom[0]-x[0])*(w/lines)), int(math.sin(-math.radians(odom[2]+90))*rep*40*1.4+h-(odom[1]-y[0])*(h/lines))), (100, 0, 100), 3, 8, 0, 0.3)
                cv2.arrowedLine(temp, (int((odom[0]-x[0])*(w/lines)),int(h-(odom[1]-y[0])*(h/lines))), (int(math.cos(math.radians(odom[2]+90))*attr*40*0.4+(odom[0]-x[0])*(w/lines)), int(math.sin(-math.radians(odom[2]+90))*attr*40*0.4+h-(odom[1]-y[0])*(h/lines))), (0, 0, 255), 3, 8, 0, 0.3)

                outputs.share_image("Img", temp)
        except Exception:
            continue

