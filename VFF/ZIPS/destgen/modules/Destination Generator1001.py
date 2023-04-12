def main(inputs, outputs, parameters, synchronise):
    dest_arr = [[7,9],
                [10,15],
                [10,23],
                [5,26],
                [-1,23],
                [-1,8]]
    destination = [0,0,0]
    odom = []
    first = True
    margen = 0.2
    actual = -1
    while 1:
        odom = inputs.read_array("Odom")
        if odom is not None:
            if(first or 
                    (odom[0] > dest_arr[actual][0]-margen and 
                    odom[0] < dest_arr[actual][0]+margen and
                    odom[1] > dest_arr[actual][1]-margen and 
                    odom[1] < dest_arr[actual][1]+margen)):
                actual += 1
                if(actual > len(dest_arr)-1):
                    actual = 0 
                destination = dest_arr[actual]
                outputs.share_array("Destination", destination)
                first = False

    pass