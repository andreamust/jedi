"""

"""
import pickle
import sys
from pathlib import Path

import pandas as pd
from graphviz import Digraph

from node_py import Node


DATASET = Path.cwd().parent / 'data' / 'cleaned_humans_5k.csv'
sys.setrecursionlimit(10000)


def create_mapping(mapping_path: Path):
    """

    :param mapping_path:
    :return:
    """
    with open(mapping_path, "rb") as file:
        properties_mapping = pickle.load(file)
        tree.map_replace({}, {}, properties_mapping)


if __name__ == '__main__':
    # testing
    df = pd.read_csv(DATASET)
    tree = Node(df)
    # create_mapping(Path('../data/property_mapping.bin'))
    tree.right.print_stats()

    tree.right.print_graph(Digraph())
