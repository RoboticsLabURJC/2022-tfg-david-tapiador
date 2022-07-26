import numpy as np

def main(inputs, outputs, parameters, synchronise):

    auto_enable = False
    try:
        enable = inputs.read_number('Enable')
    except Exception:
        auto_enable = True

    try:
        while auto_enable or inputs.read_number('Enable'):
            vels = [1,0,0,0,0,0]
            to_write = np.array(vels, dtype='<U64')
            outputs.share_array("Vels", to_write)   
            synchronise()
    
    except Exception as e:
        print("Error")