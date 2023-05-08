def main(inputs, outputs, parameters, synchronise):
    
    first = True
    changed = False
    times = 0
    max_times = 3
    while 1:
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
        print("X -> " + str(x))
        print("Y -> " + str(y))
