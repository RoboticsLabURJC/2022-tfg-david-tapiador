import cv2

def main(inputs, outputs, parameters, synchronise):

    while 1:
        try:
            enable = inputs.read_number('Enable')
            if enable == 1:
                img = inputs.read_image("Img")
                if img is None:
                    continue
                    
                cv2.imshow("frame", img)
                cv2.waitKey(10)

                synchronise()
        except Exception:
            continue