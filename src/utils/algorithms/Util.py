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

"""Util.py

Simple utility functions for PADS library.
D. Eppstein, April 2004.
"""

def arbitrary_item(S):
    """
    Select an arbitrary item from set or sequence S.
    Avoids bugs caused by directly calling iter(S).next() and
    mysteriously terminating loops in callers' code when S is empty.
    """
    try:
        return next(iter(S))
    except StopIteration:
        raise IndexError("No items to select.")

def map_to_constant(constant):
    """
    Return a factory that turns sequences into dictionaries, where the
    dictionary maps each item in the sequence into the given constant.
    Appropriate as the adjacency_list_type argument for Graphs.copyGraph.
    """
    def factory(seq):
        return dict.fromkeys(seq,constant)
    return factory
