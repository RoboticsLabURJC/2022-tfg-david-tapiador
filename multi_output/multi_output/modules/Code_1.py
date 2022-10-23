def main(inputs, outputs, parameters, synchronise):
    a = [1,2,3,4]
    while 1:
        a[0] += 1
        outputs.share_array("O", a)