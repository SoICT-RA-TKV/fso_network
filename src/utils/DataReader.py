import numpy as np
from collections import namedtuple

FSO = namedtuple('FSO', ['index', 'x', 'y', 'z'])

def readHAPConfig(fileName):
	data = open(fileName).read().split('\n')
	ld = len(data)
	i = 0
	# BER threshold
	berThreshold = 0
	while i < ld:
		try:
			berThreshold = float(data[i].split(' ')[0])
			i += 1
			break
		except:
			i += 1
	# Radius
	R = 0
	while i < ld:
		try:
			R = float(data[i].split(' ')[0])
			i += 1
			break
		except:
			i += 1
	# Number of wavelengths
	W = 0
	while i < ld:
		try:
			W = int(data[i].split(' ')[0])
			i += 1
			break
		except:
			i += 1
	# HAP payload
	C = 0
	while i < ld:
		try:
			C = int(data[i].split(' ')[0])
			i += 1
			break
		except:
			i += 1
	return berThreshold, R, W, C

def readBERDictionary(fileName):
	data = open(fileName).read().split('\n')
	ld = len(data) - 1
	resolution = 100 / (ld - 1)
	berDict = np.zeros(shape=(ld,), dtype=float)
	for i in range(ld):
		try:
			berDict[i] = max(data[i - 1], float(data[i].split(' ')[1]))
		except:
			berDict[i] = float(data[i].split(' ')[1])
	return berDict, resolution

def readGroundFSOData(fileName):
	data = open(fileName).read().split('\n')
	ld = len(data)
	i = 0
	# Number of Ground FSOs
	NFSO = 0
	while i < ld:
		try:
			NFSO = int(data[i].split(' ')[0])
			i += 1
			break
		except:
			i += 1
	FSOs = np.ndarray(shape=(NFSO,), dtype=object)
	fsoDemands = np.zeros(shape=(NFSO, NFSO), dtype=int)
	# Coordinates of Ground FSOs
	while i < ld:
		try:
			_ = float(data[i].split(' ')[0])
			break
		except:
			i += 1
	for j in range(NFSO):
		FSOs[j] = FSO(j, *[float(x) for x in data[i].split(' ')])
		i += 1
	# Demands
	while i < ld:
		try:
			_ = int(data[i].split(' ')[0])
			break
		except:
			i += 1
	while i < ld:
		try:
			d = [int(x) for x in data[i].split(' ')]
			fsoDemands[d[0], d[1]] = d[2]
			i += 1
		except:
			break
	return NFSO, FSOs, fsoDemands