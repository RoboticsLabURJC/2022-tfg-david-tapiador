def main(inputs, outputs, parameters, synchronise):
    auto_enable = True
    try:
        enable = inputs.read_number("Enable")
    except Exception:
        auto_enable = True
    
    while(auto_enable or inputs.read_number('Enable')):
        a=1
        #results = inputs.read_array("Results")
        #print("results -> ")
        #print(results)
        #one = 1
        #zero = 0
        #if(1 == 1):
        #    outputs.share_number("Rotation", one)
        #    outputs.share_number("Follow", zero)
        #else:
        #    outputs.share_number("Rotation", zero)
        #    outputs.share_number("Follow", one)

