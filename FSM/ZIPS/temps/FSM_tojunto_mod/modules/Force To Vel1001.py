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


    max_v = 2
    min_v = 0.5
    max_w = 3

    alpha_V = 1
    beta_V = 1
    alpha_W = 0.7
    beta_W = 1.4

    try:
        while 1:
            rep = inputs.read_array("RepForce")
            attr = inputs.read_array("AttrForce")
            if rep is not None and attr is not None:

                attr_x, attr_y = test_max(attr[0],attr[1])
                rep_x, rep_y = test_max(rep[0],rep[1])


                final_v = alpha_V*attr_x + beta_V*rep_x
                final_w = alpha_W*attr_y + beta_W*rep_y
                # final_w = alpha_W*attr_y
                # final_w = beta_W*rep_y

                if(final_v < 0 and final_w < 0.3 and final_w > 0.3):
                    # Rotar en el sitio hasta que no sea sentido opuesto
                    final_v = 0
                    final_w = max_w/3
                elif(final_v > max_v):
                    final_v = max_v
                elif(final_v < min_v):
                    final_v = min_v

                if(final_w > max_w):
                    final_w = max_w
                elif(final_w < -max_w):
                    final_w = -max_w



                # print("ATTR -> " + str([round(attr_x,2), round(attr_y,2)]))
                # print(" -- REEP -> " + str([round(rep_x,2), round(rep_y,2)]))
                # print(" -- FINAL -> " + str([round(final_v,2), round(final_w,2)]))

                outputs.share_array("Vels", [final_v,0,0,0,0,final_w])
                # outputs.share_array("Vels", [0,0,0,0,0,0])



            synchronise()
    except Exception as e:
        print('Error:', e)
        pass
    finally:
        print("Exiting")
        synchronise()