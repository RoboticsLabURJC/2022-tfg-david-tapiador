import math


def main(inputs, outputs, parameters, synchronise):


    try:
        while 1:
            enable = inputs.read_number('Enable')
            if enable == 1:
                x_y_Yaw = inputs.read_array("Odom")
                dest = inputs.read_array("Destination")
                if x_y_Yaw is not None and dest is not None:

                    dx = dest[0] - x_y_Yaw[0]
                    dy = dest[1] - x_y_Yaw[1]

                    # Rotate with current angle
                    y_rel = dx * math.sin (math.radians(-x_y_Yaw[2])) + dy * math.cos (math.radians(-x_y_Yaw[2]))

                    if(y_rel > 2):
                        y_rel = 2
                    elif(y_rel < -2):
                        y_rel = -2

                    outputs.share_number("AttrForce", y_rel)



                synchronise()
    except Exception as e:
        print('Error:', e)
        pass
    finally:
        print("Exiting")
        synchronise()