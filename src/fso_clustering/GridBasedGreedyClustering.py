import sys, os

def __init__():
    cur_file_path = os.path.realpath(__file__) # Get current file abspath
    cur_file_location_path = os.path.dirname(cur_file_path) # Get current file's location abspath
    tmp_path = cur_file_location_path
    rel_path_list = []
    while True:
        tmp_path, x = os.path.split(tmp_path)
        if x == 'src':
            break
        rel_path_list.append('..')
    rel_path = os.path.join(cur_file_location_path, *rel_path_list)
    abs_path = os.path.abspath(rel_path)
    sys.path.append(abs_path)

__init__()

import math

from utils.Distance import *

from collections import namedtuple

HAP = namedtuple('HAP', ['index', 'x', 'y', 'z'])

class GridBasedGreedyClustering:
	def __init__(self, fso, R, W, fsoDemands, bwpwl):
		self.fso, self.R, self.W, self.fsoDemands, self.bwpwl = fso, R, W, fsoDemands, bwpwl
	def solve(self):
		fso, R, W, fsoDemands, bwpwl = list(self.fso), self.R, self.W, self.fsoDemands, self.bwpwl
		# Chieu canh o vuong
		L = R * math.sqrt(2)
		HL = L / 2
		# Tim mien chua FSO
		x = [float(c[1]) for c in fso]
		y = [float(c[2]) for c in fso]
		minX, maxX, minY,maxY = min(x), max(x), min(y), max(y)
		# Khoi tao cac lines
		lines = []
		noLines = int(math.ceil((maxY - minY) / L))
		for i in range(noLines):
			lines.append([])
		# Chia fso vao cac line
		fso.sort(key=lambda a : a[1])
		for f in fso:
			lines[int((f[2] - minY) / L)].append(f)
		# Phan cum tren tung line
		clusters = []
		covered = set()
		for i in range(noLines):
			j = 0
			while j < len(lines[i]):
				while (j < len(lines[i])) and (lines[i][j] in covered):
					j += 1
				if j >= len(lines[i]):
					break
				xLeft = xRight = lines[i][j][1]
				yBottom = lines[i][j][2]
				cluster = set()
				cluster.add(lines[i][j])
				j += 1
				while j <= len(lines[i]):
					if (j >= len(lines[i])) or (lines[i][j][1] - xLeft > L) or (len(cluster) >= W):
						# Them HAP moi
						xh, yh = (xLeft + xRight) / 2, yBottom + HL
						hap = HAP(len(clusters), xh, yh, 20)
						# Them cac FSO ma HAP moi bao phu vao cluster
						k = j
						while k < len(lines[i]) and (len(cluster) < W) and (lines[i][k][1] - xh <= R) and (lines[i][k] not in covered):
							if distance(hap[1:], lines[i][k][1:]) <= R:
								cluster.add(lines[i][k])
								covered.add(lines[i][k])
							k += 1
						if i + 1 < noLines:
							for k in range(len(lines[i+1])):
								if (lines[i+1][k][1] - xh > R) or (len(cluster) >= W):
									break
								if (distance(hap[1:], lines[i+1][k][1:]) <= R) and (lines[i+1][k] not in covered):
									cluster.add(lines[i+1][k])
									covered.add(lines[i+1][k])
						# Them HAP va cluster vao danh sach clusters
						clusters.append((hap, cluster))
						# Chuyen sang cluster moi
						break
					if lines[i][j] not in covered:
						yBottom = min(yBottom, lines[i][j][2])
						xRight = lines[i][j][1]
						cluster.add(lines[i][j])
						covered.add(lines[i][j])
					j += 1
		NHAP = len(clusters)
		hapDemands = np.zeros(shape=(NHAP, NHAP), dtype=int)
		for i in range(NHAP):
			for j in range(NHAP):
				if i == j:
					continue
				for fso_i in clusters[i][1]:
					for fso_j in clusters[j][1]:
						hapDemands[i, j] += fsoDemands[fso_i[0], fso_j[0]]
				hapDemands[i, j] = int(math.ceil(hapDemands[i, j] / bwpwl))
		return clusters, hapDemands
