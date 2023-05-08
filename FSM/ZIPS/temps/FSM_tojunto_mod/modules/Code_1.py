import cv2
import numpy as np
import math


def test_max(x, y):
    ret_x = x
    ret_y = y
    angulo = 0
    max = 2
    if(x > max or y > max or x < -max or y < -max):
        if(x == 0):
            if(y > 0):
                ret_y = max*math.sin(math.pi/2)
            elif(y < 0):
                ret_y = max*math.sin(math.pi*3/2)
            ret_x = 0
        else:
            angulo = math.atan(y/x)
            if(x > 0):
                ret_x = max*math.cos(angulo)
            else:
                ret_x = max*math.cos(angulo+math.pi)
            if(y > 0):
                ret_y = max*abs(math.sin(angulo))
            else:
                ret_y = max*abs(math.sin(angulo))*y/abs(y)
    return ret_x, ret_y


def main(inputs, outputs, parameters, synchronise):

    x = [0,30]
    y = [0,30]

    w = 900
    h = 900

    max_v = 2
    min_v = 0.5
    max_w = 3
    final_v = 0
    final_w = 0

    alpha_V = 1
    beta_V = 1
    alpha_W = 0.7
    beta_W = 1.4

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
        try:
            odom = inputs.read_array("Odom")
            dest = inputs.read_array("Dest")
            laser = inputs.read_array("Laser")
            rep = inputs.read_array("RepForce")
            attr = inputs.read_array("AttrForce")
            if odom[0] != None and dest[0] != None and rep[0] != None and attr[0] != None and laser[0] != None :


                attr_x, attr_y = attr[0],attr[1]
                # rep_x, rep_y = rep[0],rep[1]
                attr_x_print, attr_y_print = test_max(attr[0],attr[1])
                rep_x, rep_y = test_max(rep[0],rep[1])


                final_v = alpha_V*attr_x_print + beta_V*rep_x
                final_w = alpha_W*attr_y_print + beta_W*rep_y


                if(final_v < 0):
                    # Rotar en el sitio hasta que no sea sentido opuesto
                    final_v = 0
                    final_w = max_w/3
                if(final_v > max_v):
                    final_v = max_v
                elif(final_v < min_v):
                    final_v = min_v

                if(final_w > max_w):
                    final_w = max_w
                elif(final_w < -max_w):
                    final_w = -max_w


                # Display vels, attr and rep in grid
                cv2.putText(temp, "V = " + str(round(final_v,2)),(w-int(w/(lines)*5),h-int(h/(lines)*2)), cv2.FONT_ITALIC, 0.7, (255, 0, 0), 2)
                cv2.putText(temp, "W = " + str(round(final_w,2)),(w-int(w/(lines)*5),h-int(h/(lines)*1)), cv2.FONT_ITALIC, 0.7, (255, 0, 0), 2)

                cv2.putText(temp, "Attr = " + str(round(attr_y_print,2)),(w-int(w/(lines)*5),h-int(h/(lines)*4)), cv2.FONT_ITALIC, 0.7, (0, 0, 255), 2)
                cv2.putText(temp, "Rep  = " + str(round(-rep_y,2)),(w-int(w/(lines)*5),h-int(h/(lines)*3)), cv2.FONT_ITALIC, 0.7, (100, 0, 100), 2)

                #Display Robot position and coords
                cv2.putText(temp, str([round(odom[0],2),round(odom[1],2)]), (int((odom[0]-x[0])*(w/lines)+(w/lines/2)),int(h-(odom[1]-y[0])*(h/lines)-(h/lines/2))), cv2.FONT_ITALIC, 0.7, (255, 0, 0), 2)
                cv2.circle(temp, (int((odom[0]-x[0])*(w/lines)),int(h-(odom[1]-y[0])*(h/lines))), 7, (255, 0, 0), -1)

                #Display arrows for robot x direction (black)
                cv2.arrowedLine(temp, (int((odom[0]-x[0])*(w/lines)),int(h-(odom[1]-y[0])*(h/lines))),(int(math.cos(math.radians(odom[2]))*20+(odom[0]-x[0])*(w/lines)),int(math.sin(-math.radians(odom[2]))*20+h-(odom[1]-y[0])*(h/lines))), (0, 0, 0), 3, 8, 0, 0.3)

                #Display destination position and coords
                cv2.putText(temp, str([round(dest[0],2),round(dest[1],2)]), (int((dest[0]-x[0])*(w/lines)+(w/lines/2)),int(h-(dest[1]-y[0])*(h/lines)-(h/lines/2))), cv2.FONT_ITALIC, 0.7, (0, 0, 255), 2)
                cv2.circle(temp, (int((dest[0]-x[0])*(w/lines)),int(h-(dest[1]-y[0])*(h/lines))), 7, (0, 0, 255), -1)

                cv2.arrowedLine(temp, 
                    (int((odom[0]-x[0])*(w/lines)),int(h-(odom[1]-y[0])*(h/lines))),
                    (int(math.cos(math.radians(odom[2]))*20+(odom[0]-x[0])*(w/lines)),
                        int(math.sin(-math.radians(odom[2]))*20+h-(odom[1]-y[0])*(h/lines))), (0, 0, 0), 3, 8, 0, 0.3)



                #Display arrows for attractive force (red)
                cv2.arrowedLine(temp,
                        (int((odom[0]-x[0])*(w/lines)),
                            int(h-(odom[1]-y[0])*(h/lines))),
                        (int(math.cos(math.pi/2-((dest[0]-odom[0])/math.sqrt(pow(attr_x,2)+pow(attr_y,2))))
                                * math.sqrt(pow(attr_x,2)+pow(attr_y,2))
                                * 20 * beta_W
                                + (odom[0]-x[0])*(w/lines)),
                            int(math.sin(-(dest[1]-odom[1])/math.sqrt(pow(attr_x,2)+pow(attr_y,2)))
                                * math.sqrt(pow(attr_x,2)+pow(attr_y,2))
                                * 20 * beta_W
                                + h-(odom[1]-y[0])*(h/lines))),
                        (0, 0, 255), 3, 8, 0, 0.3)














                #Display arrows for repuslive force (brown)
                if(rep_x != 0 and rep_y != 0):
                    cv2.arrowedLine(temp,
                            (int((odom[0]-x[0])*(w/lines)),
                                int(h-(odom[1]-y[0])*(h/lines))),
                            (int(math.cos(math.radians(odom[2]))
                                    * rep_x
                                    * 40 * alpha_W
                                    + (odom[0]-x[0])*(w/lines)),
                                int(math.sin(math.radians(odom[2]))
                                    * rep_y
                                    * 40 * alpha_W
                                    + h-(odom[1]-y[0])*(h/lines))),
                            (100, 0, 100), 3, 8, 0, 0.3)


                # #Display arrows for repuslive force (brown)
                # if(rep_x != 0 and rep_y != 0):
                #     cv2.arrowedLine(temp,
                #             (int((odom[0]-x[0])*(w/lines)),
                #                 int(h-(odom[1]-y[0])*(h/lines))),
                #             (int(math.cos(math.radians(odom[2]))
                #                     * math.sqrt(pow(rep_x,2)+pow(rep_y,2))
                #                     * 40 * alpha_W
                #                     + (odom[0]-x[0])*(w/lines)),
                #                 int(math.sin(math.radians(odom[2]))
                #                     * math.sqrt(pow(rep_x,2)+pow(rep_y,2))
                #                     * 40 * alpha_W
                #                     + h-(odom[1]-y[0])*(h/lines))),
                #             (100, 0, 100), 3, 8, 0, 0.3)














                #Draw laser dots
                for i in range(len(laser)):
                    if(laser[i] < 10):
                        cv2.circle(temp,
                                    (int(math.cos(math.radians(odom[2]+i))*laser[i]*(w/lines)+(odom[0]-x[0])*(w/lines)),
                                        int(math.sin(-math.radians(odom[2]+i))*laser[i]*(w/lines)+h-(odom[1]-y[0])*(h/lines))),
                                    2, (0, 0, 0), -1)

                outputs.share_image("Img", temp)
        except Exception:
            continue

