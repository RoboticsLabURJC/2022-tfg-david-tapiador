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

                dx = dest[1] - x_y_Yaw[0]
                dy = dest[0] - x_y_Yaw[1]

                # Rotate with current angle
                x_rel = dx * math.cos (-x_y_Yaw[2]) - dy * math.sin (-x_y_Yaw[2])
                y_rel = dx * math.sin (-x_y_Yaw[2]) + dy * math.cos (-x_y_Yaw[2])
                #print( "X - Y --> " + str(x_rel) + " - " + str(y_rel))
                outputs.share_array("AttrForce", [2,0,0,0,0,y_rel*0.5])



            synchronise()
    except Exception as e:
        print('Error:', e)
        pass
    finally:
        print("Exiting")
        synchronise()