"""

"""
from pathlib import Path
from utils import open_dataset
import joblib
from collections import defaultdict

DATASET = Path('../humans.spol')
CLEAN_DATASET = Path('../data/cleand_humans.spol')


def classes_count(dataset_path: joblib):
    """

    :param dataset_path:
    :return:
    """
    properties_count = defaultdict()
    objects_count = defaultdict()

    print(joblib.load('../data/properties_objects.joblib'))
    properties, objects = joblib.load('../data/properties_objects.joblib')

    for p in properties:
        properties_count[p] += 1
    for o in objects:
        objects_count[o] += 1
    return properties_count, objects_count


if __name__ == '__main__':
    # generate the cleaned dataset
    # clean_dataset(DATASET, CLEAN_DATASET)
    classes_count(CLEAN_DATASET)
