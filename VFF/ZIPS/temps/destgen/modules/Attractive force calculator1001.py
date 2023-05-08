import math


def main(inputs, outputs, parameters, synchronise):

    auto_enable = False
    try:
        enable = inputs.read_number('Enable')
    except Exception:
        auto_enable = True

    try:
        while auto_enable or inputs.read_number('Enable'):
        
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

                outputs.share_array("AttrForce", [1,0,0,0,0,y_rel*0.8])
                #outputs.share_array("AttrForce", [0,0,0,0,0,0])



            synchronise()
    except Exception as e:
        print('Error:', e)
        pass
    finally:
        print("Exiting")
        synchronise()