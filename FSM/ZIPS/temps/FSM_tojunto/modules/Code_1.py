import cv2
import numpy as np
import math

def main(inputs, outputs, parameters, synchronise):

    x = [0,30]
    y = [0,30]

    w = 900
    h = 900

    img = np.zeros([h,w,3],dtype=np.uint8)
    img.fill(255)
    lines = 30
    for i in range(lines+1):
        cv2.line(img, (int(img.shape[1]/(lines))*i, 0), (int(img.shape[1]/lines)*i, img.shape[0]), color=(50, 50, 50), thickness=1)
        cv2.line(img, (0, int(img.shape[1]/(lines))*i), (img.shape[0], int(img.shape[1]/lines)*i), color=(50, 50, 50), thickness=1)

    #Down left (-2,0)
    cv2.putText(img, str(x[0]), (int(w/(lines)*0.1),h-int(h/(lines)*0.5)), cv2.FONT_ITALIC, 0.4, (255, 0, 0), 1)
    cv2.putText(img, str(y[0]), (int(w/(lines)*0.6),h-int(h/(lines)*0.2)), cv2.FONT_ITALIC, 0.4, (0, 0, 255), 1)

    #Down right (-2,30)
    cv2.putText(img, str(x[0]), (w-int(w/(lines)*0.4),h-int(h/(lines)*0.5)), cv2.FONT_ITALIC, 0.4, (255, 0, 0), 1)
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
        laser = inputs.read_array("Laser")
        rep = inputs.read_number("RepForce")
        attr = inputs.read_number("AttrForce")
        try:
            if odom[0] != None and dest[0] != None and rep != None and attr != None:
                attr = attr*0.4
                rep = rep*1.4
                final_w = rep + attr
                if(final_w > 3):
                    final_w = 3
                elif(final_w < -3):
                    final_w = -3

                # Display vels, attr and rep in grid
                cv2.putText(temp, "V = 1.0",(w-int(w/(lines)*5),h-int(h/(lines)*2)), cv2.FONT_ITALIC, 0.7, (255, 0, 0), 2)
                cv2.putText(temp, "W = " + str(round(final_w[0],2)),(w-int(w/(lines)*5),h-int(h/(lines)*1)), cv2.FONT_ITALIC, 0.7, (255, 0, 0), 2)

                cv2.putText(temp, "Attr = "+ str(round(attr[0],2)),(w-int(w/(lines)*5),h-int(h/(lines)*4)), cv2.FONT_ITALIC, 0.7, (0, 0, 255), 2)
                cv2.putText(temp, "Rep = " + str(round(rep[0],2)),(w-int(w/(lines)*5),h-int(h/(lines)*3)), cv2.FONT_ITALIC, 0.7, (100, 0, 100), 2)


                #Display Robot position and coords
                cv2.putText(temp, str([round(odom[0],2),round(odom[1],2)]), (int((odom[0]-x[0])*(w/lines)+(w/lines/2)),int(h-(odom[1]-y[0])*(h/lines)-(h/lines/2))), cv2.FONT_ITALIC, 0.7, (255, 0, 0), 2)
                cv2.circle(temp, (int((odom[0]-x[0])*(w/lines)),int(h-(odom[1]-y[0])*(h/lines))), 7, (255, 0, 0), -1)

                #Display arrows for robot x direction (black)
                cv2.arrowedLine(temp, (int((odom[0]-x[0])*(w/lines)),int(h-(odom[1]-y[0])*(h/lines))), (int(math.cos(math.radians(odom[2]))*20+(odom[0]-x[0])*(w/lines)), int(math.sin(-math.radians(odom[2]))*20+h-(odom[1]-y[0])*(h/lines))), (0, 0, 0), 3, 8, 0, 0.3)

                #Display destination position and coords
                cv2.putText(temp, str([round(dest[0],2),round(dest[1],2)]), (int((dest[0]-x[0])*(w/lines)+(w/lines/2)),int(h-(dest[1]-y[0])*(h/lines)-(h/lines/2))), cv2.FONT_ITALIC, 0.7, (0, 0, 255), 2)
                cv2.circle(temp, (int((dest[0]-x[0])*(w/lines)),int(h-(dest[1]-y[0])*(h/lines))), 7, (0, 0, 255), -1)

                #Display arrows for attractive and repuslive forces (red and brown)
                cv2.arrowedLine(temp,
                                (int((odom[0]-x[0])*(w/lines)),
                                    int(h-(odom[1]-y[0])*(h/lines))),
                                (int(math.cos(math.radians(odom[2]+90))*attr*40+(odom[0]-x[0])*(w/lines)),
                                    int(math.sin(-math.radians(odom[2]+90))*attr*40+h-(odom[1]-y[0])*(h/lines))),
                                (0, 0, 255), 3, 8, 0, 0.3)


                cv2.arrowedLine(temp,
                                (int((odom[0]-x[0])*(w/lines)),
                                    int(h-(odom[1]-y[0])*(h/lines))),
                                (int(math.cos(math.radians(odom[2]+90))*rep*40+(odom[0]-x[0])*(w/lines)),
                                    int(math.sin(-math.radians(odom[2]+90))*rep*40+h-(odom[1]-y[0])*(h/lines))),
                                (100, 0, 100), 3, 8, 0, 0.3)


                for i in range(len(laser)):
                    if(laser[i] < 10):
                        cv2.circle(temp,
                                    (int(math.cos(math.radians(odom[2]+i))*laser[i]*(w/lines)+(odom[0]-x[0])*(w/lines)),
                                        int(math.sin(-math.radians(odom[2]+i))*laser[i]*(w/lines)+h-(odom[1]-y[0])*(h/lines))),
                                    2, (0, 0, 0), -1)


                outputs.share_image("Img", temp)
        except Exception:
            continue

