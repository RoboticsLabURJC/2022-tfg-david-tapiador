import math


def main(inputs, outputs, parameters, synchronise):


    maximo = 3

    try:
        while 1:     
            rep = inputs.read_number("RepForce")
            attr = inputs.read_number("AttrForce")
            if rep is not None and attr is not None:

                final_w = 1.4*rep + 0.4*attr
                if(final_w > maximo):
                    final_w = maximo
                elif(final_w < -maximo):
                    final_w = -maximo

                outputs.share_array("Vels", [1,0,0,0,0,final_w])



            synchronise()
    except Exception as e:
        print('Error:', e)
        pass
    finally:
        print("Exiting")
        synchronise()