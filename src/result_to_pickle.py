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
dir = "../data/gfso/"

result_path = 'result'
synthesis_path = '../data/synthesis/synthesis'
offload_ratio = [0.7, 0.5, 0.3]
offload = [None, 'reduce', 'remove']
backup = [False, True]
diameter = [15, 30]

def create_generalization_script(d, sb):
    script = dict()
    script['diameter'] = d
    script['radius'] = d / 2
    if sb == 'co_du_phong':
        script['backup'] = True
    else:
        script['backup'] = False
    script_name = ['d' + str(d), sb]
    return script, script_name

def add_script_path(script, script_name):
    script_name = joinany(script_name, '_')
    script['synthesis_path'] = synthesis_path + '_' + script_name + '.csv'
    script['result_path'] = result_path + '_' + script_name

def generate_scripts():
    scripts = []
    for d in diameter:
        for b in backup:
            sb = 'co_du_phong'
            if not b:
                sb = 'chua_du_phong'
            for o in offload:
                if o == None:
                    script, script_name = create_generalization_script(d, sb)
                    add_script_path(script, script_name)
                    scripts.append(script)
                    continue
                else:
                    for r in offload_ratio:
                        script, script_name = create_generalization_script(d, sb)
                        script[o] = True
                        script['offload_ratio'] = r
                        script_name.append(o)
                        script_name.append(str(r))
                        add_script_path(script, script_name)
                        scripts.append(script)
    return scripts

scripts = generate_scripts()
print('# Number of scripts:', len(scripts))

for script in scripts:
    print('\n------------------------------------\n')
    synthesisFile = script.get('synthesis_path', './synthesis.csv')
    ratio = script.get('offload_ratio', 0)
    resultDir = script.get('result_path', './result')
    print('# Synthesis file:', synthesisFile)
    print('# Result directory:', resultDir)

    try:
        os.mkdir('../data/' + resultDir)
    except:
        pass
    files = os.listdir(dir)
    files = [dir + file for file in files]

    for file in files:
        print('\n')
        print('# Data', file + ':')
        start = time.time()
        NFSO, FSOs, fsoDemands = readGroundFSOData(fileName=file)
        if script.get('reduce'):
            fsoDemands = reduceByRatio(fsoDemands, ratio)
        if script.get('remove'):
            fsoDemands = randomRemove(fsoDemands, ratio)
        R = _R
        if 'radius' in script:
            R = script['radius']
        print('# Reading time:', time.time() - start)

        gbgc = GridBasedGreedyClustering(FSOs, R, W, fsoDemands, 1024)
        clusters, hapDemands = gbgc.solve()
        print('# Clustering:', time.time() - start)

        HAPs = [cluster[0] for cluster in clusters]
        n_origin_hap = len(HAPs)
        bbg = BlossomBasedGreedy(HAPs, Rc)
        matching = {}
        if script.get('backup', False) == True:
            HAPs, matching = bbg.solve()
        print('# Matching:', time.time() - start)

        nr = NaiveRouting(berDict, berThreshold, W, C, HAPs, hapDemands)
        for m in matching:
            nr.forbid_link(m, matching[m])
        for ih in range(len(HAPs)):
            nr.decrease_capacity(ih, 1)
        for ih in range(n_origin_hap):
            nr.decrease_capacity(ih, 1)
        flows, usedEdges, usedLinks = nr.solve()
        print('# Routing:', time.time() - start)

        bwd = SmallFirstDividing(fsoDemands, HAPs, clusters, flows)
        fsoFlows = bwd.solve()

        resultFile = file.replace('gfso', resultDir)

        with  open(resultFile.replace('.txt', '.pickle'), 'wb') as f:
            pickle.dump([W, NFSO, FSOs, fsoDemands, HAPs, clusters,
                hapDemands, matching, usedEdges, usedLinks, flows, fsoFlows],
                f)
        print('# Writing:', time.time() - start)