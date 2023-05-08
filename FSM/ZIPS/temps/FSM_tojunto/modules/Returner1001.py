def main(inputs, outputs, parameters, synchronise):
    
    dest = [2,10]
    first = True
    going = False
    try:
        while 1:
            enable = inputs.read_number("Enable")
            if enable == 1 and first:
                    print("VOLVEMOS AL ORIGEN -> " + str(dest))
                    outputs.share_array("Dest", dest)
                    outputs.share_number("Next", 1)
                    first = False
            if enable == 0 and not first:
                going = True
            if enable == 1 and going:
                print("HEMOS LLEGADO AL ORIGEN!!")
                outputs.share_number("Next", 0)
    except Exception:
        pass