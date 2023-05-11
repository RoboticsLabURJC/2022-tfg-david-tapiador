def main(inputs, outputs, parameters, synchronise):
    margen = 1
    changed = False
    while 1:
        try:
            Enable = inputs.read_number("Enable")
            if Enable == 1:
                odom = inputs.read_array("Odom")
                dest = inputs.read_array("Dest")
                if odom is not None and dest is not None:
                    if((odom[0] > dest[0]-margen and 
                            odom[0] < dest[0]+margen and
                            odom[1] > dest[1]-margen and 
                            odom[1] < dest[1]+margen)):
                        outputs.share_number("AutoEnable", 0)
                        outputs.share_number("Next", 1)
                        first = False
                        changed = True
                    else:
                        outputs.share_number("AutoEnable", 1)
                        outputs.share_number("Next", 0)
            else:
                changed = True
        except Exception:
            continue
    pass