"""

"""
from collections import defaultdict
from pathlib import Path

from joblib import load, dump

TOY_DATASET = Path('../data/toy_properties_object.joblib')


def classes_count(dataset_path: Path, save: bool = True):
    """

    :param dataset_path:
    :param save:
    :return:
    """
    properties_count = defaultdict(int)
    objects_count = defaultdict(int)

    properties, objects = load(dataset_path)

    for p in properties:
        properties_count[p] += 1
    for o in objects:
        objects_count[o] += 1

    if save:
        dump(properties_count, '../data/properties_count.joblib')
        dump(objects_count, '../data/objects_count.joblib')

    print(properties_count)
    print(objects_count)
    return properties_count, objects_count


if __name__ == '__main__':
    # generate the cleaned dataset
    # clean_dataset(DATASET, CLEAN_DATASET)
    classes_count(TOY_DATASET)
