import math
import time


def parse_laser_data (laser_data):
    laser = []
    for i in range(180):
        dist = laser_data[i] /1000.0
        angle = math.radians (i)
        laser += [(dist, angle)]
    return laser

def getObs_xy(laser):
    laser2 = parse_laser_data(laser)
    laser_vectorized = []
    for d, a in laser2:
        # (4.2.1) laser into GUI reference system
        x = d * math.cos (a) * -1
        y = d * math.sin (a) * -1
        v = (x, y)
        laser_vectorized += [v]
    
    obsx = 0
    obsy = 0
    amortiguacion = 6     # Cuanto mas amortiguacion, mas valen los valores lejanos
    pico = 5            # Cuanto mas pico, mas valen los valores cercanos a cero
    for i in range(len(laser_vectorized)):
        if(laser_vectorized[i][0] != 0):
            obsx -= pico*abs(math.atan(amortiguacion/(10000*laser_vectorized[i][0])))
        if(laser_vectorized[i][1] == 0):
            obsy += 0
        elif(i<90):
            obsy -= pico*abs(math.atan(amortiguacion/(10000*laser_vectorized[i][1])))
        else:
            obsy += pico*abs(math.atan(amortiguacion/(10000*laser_vectorized[i][1])))
    return obsx, obsy



def main(inputs, outputs, parameters, synchronise):


    auto_enable = False
    try:
        enable = inputs.read_number('Enable')
    except Exception:
        auto_enable = True

    try:
        while auto_enable or inputs.read_number('Enable'):
        
            measures = inputs.read_array("Laser")
            if measures is not None:
                obsX, obsY = getObs_xy(measures)
                #print("LEN -> " + str(len(measures)))
                #print("X -> " + str(obsX))
                #print("Y -> " + str(obsY))
                #print()
                outputs.share_array("RepForce", [obsX, obsY])  

            synchronise()
    except Exception as e:
        print('Error:', e)
        pass
    finally:
        print("Exiting")
        synchronise()