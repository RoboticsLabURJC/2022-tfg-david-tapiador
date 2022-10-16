def main(inputs, outputs, parameters, synchronise):
    a = 1
    # while(1):
    # outputs.share_number("O", a)
    a = 0
    # outputs.share_number("O", a)
    while 1:
        a +=1
        outputs.share_number("O", a)
    # outputs.share_number("O", None)
    # pass