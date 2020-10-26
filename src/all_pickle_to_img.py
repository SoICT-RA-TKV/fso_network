import sys, os
import pickle

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

from utils.DataReader import *
from fso_clustering.GridBasedGreedyClustering import *
from hap_routing.Naive import *
from backup_pairing.BlossomBasedGreedy import BlossomBasedGreedy
from fso_bandwidth_dividing.EquallyDividing import EquallyDividing
from fso_bandwidth_dividing.SmallFirstDividing import SmallFirstDividing
from utils.ResultWriter import  *
from utils.demandReduction import *
from utils.String import *
from visualization.visualizer import *
import time

berDict, resolution = readBERDictionary(fileName='../config/ber.txt')
berThreshold, _R, W, C, Rc = readHAPConfig(fileName='../config/capacity.txt')

import os

dir = '../data'

folders  = set(os.listdir(dir))
files = []

for folder in folders:
    if os.path.isfile(dir + '/' + folder) or folder.find('result') != 0:
        pass
    else:
        files += [dir + '/' + folder + '/' + file for file in os.listdir(dir + '/' + folder)]

print(files)

for file in files:

    with open(file, 'rb') as f:
        W, NFSO, FSOs, fsoDemands, HAPs, clusters, hapDemands, matching, usedEdges, usedLinks, flows, fsoFlows = pickle.load(f)

    R = 7.5

    xmin = min([hap.x for hap in HAPs]) - R * 1.2
    xmax = max([hap.x for hap in HAPs]) + R * 1.2
    ymin = min([hap.y for hap in HAPs]) - R * 1.2
    ymax = max([hap.y for hap in HAPs]) + R * 1.2
    axes = [xmin, xmax, ymin, ymax]

    visualizeGroundFSO(file.replace('.pickle', '_gfso.png'), FSOs, *axes)
    visualizeClusters(file.replace('.pickle', '_clusters.png'), clusters, FSOs, HAPs, R, *axes)
    visualizeHAP(file.replace('.pickle', '_hap.png'), HAPs, clusters, *axes)
    visualizeHAPTopology(file.replace('.pickle', '_haptopo.png'), HAPs, clusters, matching, usedLinks, *axes)