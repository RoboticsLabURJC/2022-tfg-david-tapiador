from time import sleep

def main(inputs, outputs, parameters, synchronise):
    auto_enable = True
    try:
        enable = inputs.read_number("Enable")
    except Exception:
        auto_enable = True
    
    while(True):
        results = inputs.read_array("Results")
        try:
            if(results.any()):
                break
        except Exception:
            continue

    not_to_enable = 0
    to_enable = 1

    print("EMPEZAMOS")
    while(auto_enable or inputs.read_number('Enable')):
        results = inputs.read_array("Results")
        sleep(0.1)
        
        if(results[0] != -1):
            #print("A")
            outputs.share_number("Rotation", not_to_enable)
            outputs.share_number("Decision", 1) # Read the Follow input
            outputs.share_number("Follow", to_enable)
        else:
            #print("C")
            outputs.share_number("Rotation", to_enable)
            outputs.share_number("Decision", 0) # Read the Rotation input
            outputs.share_number("Follow", not_to_enable)
