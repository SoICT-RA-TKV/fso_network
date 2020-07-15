from src.utils.DataReader import *
from src.fso_clustering.GridBasedGreedyClustering import *
from src.hap_routing.Naive import *
from src.backup_pairing.BlossomBasedGreedy import BlossomBasedGreedy
from src.utils.ResultWriter import  *

berDict, resolution = readBERDictionary(fileName='../config/ber.txt')
berThreshold, R, W, C = readHAPConfig(fileName='../config/capacity.txt')

import os
dir = "../data/gfso/"
files = os.listdir(dir)

synthesisFile = '../data/synthesis/synthesis_d15.csv'
files = [dir + file for file in files]
# files = ["../data/gfso/gfso_475_0.txt"]

for file in files:
    print(file + ':')
    NFSO, FSOs, fsoDemands = readGroundFSOData(fileName=file)
    # print(NFSO)
    # print(FSOs)
    # print(fsoDemands)

    gbgc = GridBasedGreedyClustering(FSOs, R, W, fsoDemands, 1024)
    clusters, hapDemands = gbgc.solve()
    # print(clusters)
    # print('Number of clusters:', len(clusters))

    HAPs = [cluster[0] for cluster in clusters]
    n_origin_hap = len(HAPs)
    bbg = BlossomBasedGreedy(HAPs, R)
    HAPs, matching = bbg.solve()
    # print('Number of HAP after backup pairing:', len(hap))
    # print(hap)
    # print(matching)

    nr = NaiveRouting(berDict, berThreshold, W, C, HAPs, hapDemands)
    for m in matching:
        nr.forbid_link(m, matching[m])
    for ih in range(len(HAPs)):
        nr.decrease_capacity(ih, 1)
    for ih in range(n_origin_hap):
        nr.decrease_capacity(ih, 1)
    # print(nr.used_links)
    # print(nr.capacities)
    flows, usedEgdes, usedLinks = nr.solve()
    # print(flows)
    # print(len(flows), end=' ')
    # print(sum(sum(hapDemands)))

    resultFile = file.replace('gfso', 'result')
    writeResult(resultFile, NFSO, FSOs, fsoDemands, HAPs, clusters, hapDemands, matching, usedLinks, flows)

    if sum(sum(hapDemands)) > 0:
        updateSynthesis(synthesisFile, W, NFSO, FSOs, fsoDemands, HAPs, clusters, hapDemands, matching, usedLinks, usedEgdes, flows)