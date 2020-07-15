from src.utils.Distance import *

from src.utils.algorithms.CardinalityMatching import *
from src.utils.algorithms.Graph import *
from src.utils.Distance import *
from collections import namedtuple

HAP = namedtuple('HAP', ['index', 'x', 'y', 'z'])

class BlossomBasedGreedy:
	def __init__(self, hap, RCloud):
		self.hap, self.RCloud = hap, RCloud
	def solve(self):
		hap, RCloud = self.hap, self.RCloud
		NHAP = len(hap)
		# Using blossom algorithm to find maximum matching
		g = Graph()
		hap_vertex = []
		for i in range(NHAP):
			hap_vertex.append(Vertex(hap[i][0]))
			g.add_vertex(hap_vertex[-1])
		for i in range(NHAP):
			for j in range(NHAP):
				if distance(hap[i], hap[j]) >= 2*RCloud:
					g.add_edge(hap_vertex[i], hap_vertex[j])
		m = blossomMatching(g)
		# Backup for HAP not been matched
		matching = dict()
		for v in m:
			w = m[v]
			matching[v.name] = w.name
		hapId = max([h[0] for h in hap])
		for i in range(NHAP):
			if hap[i][0] not in matching:
				hapId += 1
				newHap = HAP(hapId, hap[i][1] + 2 * RCloud, hap[i][2], 0)
				hap.append(newHap)
				matching[hap[i][0]] = newHap[0]
		return hap, matching