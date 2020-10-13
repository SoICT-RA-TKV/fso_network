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

from utils.String import *
from utils.Distance import *

def writeResult(fileName, NFSO, FSOs, fsoDemands, HAPs, clusters, hapDemands, matching, usedLinks, flows, fsoFlows):
    f = open(fileName, 'w')
    f.write('# Number of ground FSO:\n')
    f.write(str(NFSO) + '\n')
    f.write('# Ground FSO coordinates:\n')
    for fso in FSOs:
        f.write(joinany(fso[:], ' ') + '\n')
    f.write('# FSO demands in Mbps:\n')
    for i in range(NFSO):
        for j in range(NFSO):
            if fsoDemands[i, j] <= 0:
                continue
            f.write(joinany([i, j, fsoDemands[i, j]], ' ') + '\n')
    f.write('# Number of HAPs:\n')
    f.write(str(len(HAPs)) + '\n')
    f.write('# HAP coordinates:\n')
    for hap in HAPs:
        f.write(joinany(hap[:], ' ') + '\n')
    f.write('# Number of clusters:\n')
    f.write(str(len(clusters)) + '\n')
    f.write('# Cluster\'s FSOs:\n')
    f.write('# First of each two-lines is HAP index\n')
    f.write('# Second of each two-lines is cluster\'s ground FSO index\n')
    for i in range(len(clusters)):
        f.write(str(clusters[i][0].index) + '\n')
        for fso in clusters[i][1]:
            f.write(str(fso.index) + ' ')
        f.write('\n')
    f.write('# HAP demands in number of flows:\n')
    for i in range(hapDemands.shape[0]):
        for j in range(hapDemands.shape[1]):
            if hapDemands[i, j] <= 0:
                continue
            f.write(joinany([i, j, hapDemands[i, j]], ' ') + '\n')
    f.write('# Backup Matching:\n')
    for hap in matching:
        f.write(joinany([hap, matching[hap]], ' ') + '\n')
    f.write('# Links\n')
    for link in usedLinks:
        f.write(str(link))
        f.write('\n')
    f.write('# Flows\n')
    for flow in flows:
        f.write(str(flow))
        f.write('\n')
    f.write('# FSO Flows\n')
    for i in range(NFSO):
        for j in range(NFSO):
            if len(fsoFlows[i][j]) == 0:
                continue
            f.write(joinany([i, j], ' ') + ':\n')
            for fsoFlow in fsoFlows[i][j]:
                f.write(str(fsoFlow) + '\n')
    f.close()

def updateSynthesis(fileName, W, NFSO, FSOs, fsoDemands, HAPs, clusters, hapDemands, matching, usedLinks, usedEgdes, flows, fsoFlows):
    keys = ['# FSO', 'Height' , 'Width' , '# Demand (in Flow)',
            '# Cluster', '# HAP', '# Used Link', '# Used Edge',
            '# Remain Demand (in Flow)', '% Responsed',
            'Mean Degree', '% Used Edge', '# FSO per Cluster',
            '# Demand per HAP', 'Mean Link Length']
    res = dict()
    res['# FSO'] = NFSO
    res['Height'] = max([fso.x for fso in FSOs]) - min([fso.x for fso in FSOs])
    res['Width'] = max([fso.y for fso in FSOs]) - min([fso.y for fso in FSOs])
    res['# Demand (in Flow)'] = sum(sum(hapDemands))
    res['# Cluster'] = len(clusters)
    res['# HAP'] = len(HAPs)
    res['# Used Link'] = len(usedLinks) / 2
    res['# Used Edge'] = len(usedEgdes)
    res['# Remain Demand (in Flow)'] = res['# Demand (in Flow)'] - len(flows)
    try:
        res['% Responsed'] = len(flows) / res['# Demand (in Flow)']
    except:
        res['% Responsed'] = 1
    res['Mean Degree'] = len(usedLinks) / len(HAPs)
    try:
        res['% Used Edge'] = len(usedEgdes) / (len(usedLinks) * W)
    except:
        res['% Used Edge'] = 1
    res['# FSO per Cluster'] = NFSO / len(clusters)
    res['# Demand per HAP'] = res['# Demand (in Flow)'] / len(clusters)
    res['Mean Link Length'] = 0
    for link in usedLinks:
        res['Mean Link Length'] += distance(HAPs[link[0]], HAPs[link[1]])
    try:
        res['Mean Link Length'] /= len(usedLinks)
    except:
        res['Mean Link Length'] = 0
    synthesis_file = open(fileName, 'a')
    # synthesis_file.write(joinany([file.split('_')[1], max(h.x for h in hap) - min(h.x for h in hap),
    #                               max(h.y for h in hap) - min(h.y for h in hap),
    #                               sum(sum(hapDemands)), NHAP, NHAP_w, len(used_links), len(used_edges),
    #                               sum(sum(remains)),
    #                               1 - sum(sum(remains)) / sum(sum(hapDemands)), len(used_edges) / NHAP_w,
    #                               len(used_edges) / (len(used_links) * 128),
    #                               int(file.split('_')[1]) / NHAP, sum(sum(demands)) / NHAP,
    #                               sum(sum(dists)) / (NHAP * NHAP)], ',') + '\n')
    for key in keys:
        if key not in res:
            res[key] = None
        synthesis_file.write(str(res[key]) + ',')
    synthesis_file.write('\n')
    synthesis_file.close()