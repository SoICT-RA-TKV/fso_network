import numpy as np
import math

def distance(o1, o2):
	try:
		return np.linalg.norm([o1.x - o2.x, o1.y - o2.y])
	except:
		return -1

def hap_ber(dist, berDict):
	try:
		return berDict[math.ceil(dist * 1e4)]
	except:
		return float('inf')