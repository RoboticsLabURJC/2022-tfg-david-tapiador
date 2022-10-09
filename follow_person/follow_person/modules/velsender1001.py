import numpy as np

def main(inputs, outputs, parameters, synchronise):

    try:
        while 1:
            if(inputs.read_number('Enable')):
                print("ROT")
                vels = [0,0,0,0,0,0.05]
                to_write = np.array(vels, dtype='<U64')
                outputs.share_array("Vels", to_write)   
                synchronise()
    
    except Exception as e:
        print("Error")