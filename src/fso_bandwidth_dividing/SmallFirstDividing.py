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

from utils.DataReader import *
from collections import namedtuple

FLOW = namedtuple('FLOW', ['wavelength', 'nodes'])

def list_flow(flows, start, end):
    list_flows = []
    for flow in flows:
        if flow.nodes[0] == start and flow.nodes[-1] == end:
            list_flows.append(flow)
    return list_flows

class SmallFirstDividing:
    def __init__(self, fsoDemands, HAPs, clusters, flows):
        super().__init__()
        self.fsoDemands, self.HAPs, self.clusters, self.flows = fsoDemands, HAPs, clusters, flows

    def solve(self):
        fsoDemands, HAPs, clusters, flows = self.fsoDemands, self.HAPs, self.clusters, self.flows
        fsoFlows = []
        NFSO = len(fsoDemands)
        for i in range(NFSO):
            fsoFlows.append([])
            for j in range(NFSO):
                fsoFlows[-1].append(set())
        for ci in clusters:
            for cj in clusters:
                if ci[0].index == cj[0].index:
                    for fi in ci[1]:
                        for fj in cj[1]:
                            if fsoDemands[fi.index][fj.index] > 0:
                                fsoFlows[fi.index][fj.index].add((FLOW('None', (ci[0].index,)), fsoDemands[fi.index][fj.index]))
                else:
                    list_flows = list_flow(flows, ci[0].index, cj[0].index)
                    num_flows = len(list_flows)
                    list_demands = []
                    for fi in ci[1]:
                        for fj in cj[1]:
                            list_demands.append([fi.index, fj.index, fsoDemands[fi.index][fj.index]])
                    list_demands.sort(key=lambda x : x[2])
                    remain_bw = 1024
                    flow_idx = 0
                    for demand in list_demands:
                        if flow_idx >= num_flows:
                            break
                        res_dm = demand[2]
                        if res_dm == 0:
                            continue
                        flow = list_flows[flow_idx]
                        if remain_bw > 0:
                            fsoFlows[demand[0]][demand[1]].add((flow, min(res_dm, remain_bw)))
                        if remain_bw < res_dm:
                            res_dm -= remain_bw
                            flow_idx += 1
                            remain_bw = 1024
                            if flow_idx >= num_flows:
                                break
                            flow = list_flows[flow_idx]
                            fsoFlows[demand[0]][demand[1]].add((flow, min(res_dm, remain_bw)))
                            remain_bw -= res_dm
                        else:
                            remain_bw -= res_dm
        count = 0
        for i in range(NFSO):
            for j in range(NFSO):
                count += len(fsoFlows[i][j])
        print(count)
        return fsoFlows

if __name__ == '__main__':
    file = '../../data/gfso/gfso_47_0.txt'
    NFSO, FSOs, fsoDemands = readGroundFSOData(fileName=file)
    print(NFSO, FSOs, fsoDemands)
    # eq = EquallyDividing()