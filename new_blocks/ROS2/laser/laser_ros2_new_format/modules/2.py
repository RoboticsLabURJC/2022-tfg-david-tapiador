def main(inputs, outputs, parameters, synchronise):


    auto_enable = False
    try:
        enable = inputs.read_number('Enable')
    except Exception:
        auto_enable = True

    try:
        while auto_enable or inputs.read_number('Enable'):
        
            measures = inputs.read_array("Laser")
            if measures is not None:
                print("LEN -> " + str(len(measures)))
                print(measures)

            synchronise()
    except Exception as e:
        print('Error:', e)
        pass
    finally:
        print("Exiting")
        synchronise()