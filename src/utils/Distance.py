import sys, os
import numpy as np

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

import numpy as np
import math

def distance(o1, o2):
    try:
        return np.linalg.norm([o1.x - o2.x, o1.y - o2.y])
    except:
        print(o1)
        print(o2)
        raise Exception("Errorrrrrrrr")
        return float('inf')

def hap_ber(dist, berDict):
    try:
        return berDict[math.ceil(dist * 1e4)]
    except:
        return 1