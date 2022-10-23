def main(inputs, outputs, parameters, synchronise):
    while(1):
        try:
            read = inputs.read_array("I1")
            print("UP   -> " + str(read))
        except Exception:
            a = 0
        try:
            read = inputs.read_array("I2")
            print("MID -> " + str(read))
        except Exception:
            a = 0
        try:
            read = inputs.read_array("I3")
            print("DOWN -> " + str(read))
        except Exception:
            a = 0
    pass