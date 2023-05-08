from random import randint

def main(inputs, outputs, parameters, synchronise):
    
    first = True
    changed = False
    times = 0
    max_times = 4
    margen = 3

    uno = 1
    zero = 0

    x = [0,30]
    y = [0,30]



    while 1:    
        try:
            enable = inputs.read_number("Enable")
            if(enable == 0):
                changed = False
            if (enable == 1 or first) and not changed:
                odom = inputs.read_array("Odom")
                if odom[0] != None:
                    changed = True
                    first = False
                    times += 1

                    if(times < max_times):
                        dest = [randint(x[0]+1, x[1]-1),
                                    randint(y[0]+1,y[1]-1)]

                        while dest[0] > int(odom[0]-margen) and dest[0] < int(odom[0]+margen):
                            dest[0] = randint(x[0]+1, x[1]-1)
                        while dest[1] > int(odom[1]-margen) and dest[1] < int(odom[1]+margen):
                            dest[1] = randint(y[0]+1,y[1]-1)

                        print("NUEVO DESTINO -> " + str(dest))
                        outputs.share_array("Dest", dest)
                        outputs.share_number("Next", uno)
                        outputs.share_number("Last", zero)

                    else:
                        outputs.share_number("Next", zero)
                        outputs.share_number("Last", uno)

        except Exception:
            continue