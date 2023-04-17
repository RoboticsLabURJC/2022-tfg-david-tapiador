def main(inputs, outputs, parameters, synchronise):
    dest_arr = [[7,9],
                [10,15],
                [10,23],
                [5,26],
                [-1,23],
                [-1,9]]
    destination = [0,0,0]
    odom = []
    first = True
    margen = 1
    actual = -1
    lap = 0
    while 1:
        odom = inputs.read_array("Odom")
        if odom is not None:
            if(first or 
                    (odom[0] > dest_arr[actual][0]-margen and 
                    odom[0] < dest_arr[actual][0]+margen and
                    odom[1] > dest_arr[actual][1]-margen and 
                    odom[1] < dest_arr[actual][1]+margen)):
                actual += 1
                if(first or actual > len(dest_arr)-1):
                    lap +=1
                    actual = 0    
                    print("LAP NUMBER " + str(lap)) 
                destination = dest_arr[actual]
                outputs.share_array("Destination", destination)
                print("NEW DESTINATION! " + str(destination))
                first = False
    pass
