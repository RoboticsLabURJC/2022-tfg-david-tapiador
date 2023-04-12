import random

destination = [0,0,0]
odom = []
first = True
margen = 3


def main(inputs, outputs, parameters, synchronise):
    
    while 1:
        odom = inputs.read_array("Odom")
        if odom is not None:
            print("abajo LEN -> " + str(len(odom)))
            print("abajo odom -> " + str(odom))
            if(first):
                destination = [random.randint(odom[0]-margen,odom[0]+margen),
                                random.randint(odom[1]-margen,odom[1]+margen)]
                first = False
    pass