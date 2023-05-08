def main(inputs, outputs, parameters, synchronise):
    a = 0
    while 1:
        a +=1
        outputs.share_number("O", a)