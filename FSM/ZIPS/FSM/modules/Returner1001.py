def main(inputs, outputs, parameters, synchronise):
    
    dest = [2,10]
    changed = False
    try:
        while 1:
            enable = inputs.read_number("Enable")
            if enable == 1:
                outputs.share_array("Dest", dest)
                outputs.share_number("Next", 0)
                changed = False

            else:
                if not changed:
                    outputs.share_number("Next", 0)
                    changed = True
    
    
    except Exception:
        pass