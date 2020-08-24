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

class EquallyDividing:
    def __init__(self, fsoDemands, HAPs, clusters, flows):
        super().__init__()
        print(fsoDemands)
        print(HAPs)
        print(clusters)
        print(flows)

if __name__ == '__main__':
    file = '../../data/gfso/gfso_47_0.txt'
    NFSO, FSOs, fsoDemands = readGroundFSOData(fileName=file)
    print(NFSO, FSOs, fsoDemands)
    # eq = EquallyDividing()