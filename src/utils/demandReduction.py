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

import random

def reduceByRatio(demands, ratio):
    return (demands * (1 - ratio)).astype(int)

def randomRemove(demands, ratio, seed=7):
    random.seed(seed)
    for i in range(demands.shape[0]):
        for j in range(demands.shape[1]):
            remove = random.random() < ratio
            if remove:
                demands[i, j] = 0
    return demands