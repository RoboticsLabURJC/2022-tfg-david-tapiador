def main(inputs, outputs, parameters, synchronise):
    
    first = True
    changed = False
    times = 0
    max_times = 3
    while 1:    
        try:
            enable = inputs.read_number("Enable")
            if(enable == 0):
                changed = False
            if (enable == 1 or first) and not changed:
                changed = True
                first = False
                odom = inputs.read_array("Odom")
                if odom[0] != None:
                    times += 1
                    if(times <= max_times):
                        x = input("Give the next X coord: ")
                        y = input("Now the next Y coord: ")
                        while(1):
                            try:
                                float(x)
                                float(y)
                                break
                            except Exception:
                                x = input("One or both coords where bad, use floats.\nGive the next X coord: ")
                                y = input("Now the next Y coord: ")
                        output.share_array("Dest", [x,y])
                        output.share_number("Next", 1)
                        output.share_number("Last", 0)
                    else:
                        output.share_number("Next", 0)
                        output.share_number("Last", 1)

        except Exception:
            first = True
            changed = False
            continue