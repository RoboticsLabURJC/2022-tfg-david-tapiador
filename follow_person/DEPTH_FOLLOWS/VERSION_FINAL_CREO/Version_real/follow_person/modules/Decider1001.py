def main(inputs, outputs, parameters, synchronise):
    auto_enable = True
    try:
        enable = inputs.read_number("Enable")
    except Exception:
        auto_enable = True

    not_to_enable = 0
    to_enable = 1
    lowpass_filter = 2
    counter = 0

    print("EMPEZAMOS")
    while(auto_enable or inputs.read_number('Enable')):
        results = inputs.read_array("Results")
        if results is None:
            continue

        
        if(results[0] != -1):
            # Follow
            #print("A")
            counter = 0
            outputs.share_number("Decision", 1)
        elif(counter < 10):
            # Follow but low-pass filter
            #print("B")
            counter += 1
            outputs.share_number("Decision", 2)
        else:
            # Rotation
            #print("C")
            outputs.share_number("Decision", 0)
