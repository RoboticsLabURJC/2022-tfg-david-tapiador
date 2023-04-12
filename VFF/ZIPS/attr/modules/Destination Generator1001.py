import random




def main(inputs, outputs, parameters, synchronise):
    
    destination = [0,0,0]
    odom = []
    first = True
    margen = 3

    while 1:
        odom = inputs.read_array("Odom")
        if odom is not None:
            print("ODOM ->>>> " + str(odom))
            if(first):
                destination = [random.uniform(odom[0]-margen,odom[0]+margen),
                                random.uniform(odom[1]-margen,odom[1]+margen)]
                destination = [10,-10]
                outputs.share_array("Destination", destination)
                first = False
    pass