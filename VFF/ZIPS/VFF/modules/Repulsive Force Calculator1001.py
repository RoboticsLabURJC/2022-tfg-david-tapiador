import math
import time


def parse_laser_data (laser_data):
	laser = []
	for i in range(len(laser_data)):
		dist = laser_data[i]
		angle = math.radians (i)
		laser += [(dist, angle)]
	return laser

def getObs_xy(laser):
	laser2 = parse_laser_data(laser)
	laser_vectorized = []
	for d, a in laser2:
		if(a == 0):
			x = 10
			y = 10
		else:
			x = d * math.cos (a) * -1
			y = d * math.sin (a) * -1
		v = (x, y)
		laser_vectorized += [v]
	
	obsx = 0
	obsy = 0	
	amortiguacion = 1   # Cuanto mas amortiguacion, mas valen los valores lejanos
	pico = 1			# Cuanto mas pico, mas valen los valores cercanos a cero
	for i in range(int(len(laser_vectorized)/2)):
		if(i<90):
			if((laser_vectorized[i][1] > 0 or laser_vectorized[i][1] < 0) and laser_vectorized[i][1] < 10):
				obsy -= pico*abs(math.atan(amortiguacion/(laser_vectorized[i][1])))
		else:
			if((laser_vectorized[180+i][1] > 0 or laser_vectorized[180+i][1] < 0) and laser_vectorized[180+i][1] < 10):
				obsy += pico*abs(math.atan(amortiguacion/(laser_vectorized[180+i][1])))
	return obsx, obsy



def main(inputs, outputs, parameters, synchronise):


	auto_enable = False
	try:
		enable = inputs.read_number('Enable')
	except Exception:
		auto_enable = True
	reduction = 1/50
	try:
		while auto_enable or inputs.read_number('Enable'):
		
			measures = inputs.read_array("Laser")
			if measures is not None:
				obsX, obsY = getObs_xy(measures)
				outputs.share_number("RepForce", obsY*reduction) 

			synchronise()
	except Exception as e:
		print('Error:', e)
		pass
	finally:
		print("Exiting")
		synchronise()