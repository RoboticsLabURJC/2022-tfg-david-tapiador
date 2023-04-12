import random




def main(inputs, outputs, parameters, synchronise):

    destination = [0,0,0]
    odom = []
    first = True
    margen = 3

    while 1:
        odom = inputs.read_array("Odom")
        if odom is not None:
            print("abajo LEN -> " + str(len(odom)))
            print("abajo odom -> " + str(odom))
            if(first):
                destination = [random.uniform(odom[0]-margen,odom[0]+margen),
                                random.uniform(odom[1]-margen,odom[1]+margen)]
                first = False
    pass