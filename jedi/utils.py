"""
Utility functions for supporting the implement
"""
from pathlib import Path

from joblib import dump


def clean_dataset(dataset_path: Path, output_path: Path) -> None:
    """
    Utility function that takes the original dataset and clean
    it by removing all triples containing literals and removing
    all subjects in the triples
    :param dataset_path: Path
        The absolute path of the original dataset
    :param output_path: Path
        The absolute path where the cleaned dataset is saved
    :return: None
        It save
    """
    with open(output_path, 'w') as cleaned:
        with open(dataset_path, 'r') as dataset:
            for line in dataset:
                split_line = line.split('\t')
                if split_line[2] != '0':
                    cleaned.write('\t'.join(split_line[1:]))


def open_dataset(dataset_path: Path, save: bool = True) -> tuple:
    """

    :param dataset_path:
    :param save:
    :return:
    """
    properties, objects = [], []
    with open(dataset_path, 'r') as dataset:
        for line in dataset:
            property, object = line.split('\t')[:2]
            properties.append(int(property))
            objects.append(int(object))
    if save:
        dump((properties, objects), '../data/properties_objects.joblib')
    return properties, objects
