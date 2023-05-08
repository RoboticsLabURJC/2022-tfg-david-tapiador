def main(inputs, outputs, parameters, synchronise):


    auto_enable = False
    try:
        enable = inputs.read_number('Enable')
    except Exception:
        auto_enable = True

    try:
        while auto_enable or inputs.read_number('Enable'):
        
            x_y_Yaw = inputs.read_array("Odom")
            if x_y_Yaw is not None:
                a = 0
                print("LEN -> " + str(len(x_y_Yaw)))
                print("x_y_Yaw -> " + str(x_y_Yaw))
            dest = inputs.read_array("Destination")
            if x_y_Yaw is not None:
                a = 0
                print("dest -> " + str(dest))

            synchronise()
    except Exception as e:
        print('Error:', e)
        pass
    finally:
        print("Exiting")
        synchronise()