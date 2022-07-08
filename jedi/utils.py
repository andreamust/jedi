"""
Utility functions for supporting the implement
"""
import csv
from pathlib import Path

from joblib import dump

DATASET = Path('../humans.spol')
CSV_DATASET = Path('../data/cleaned_humans_8k.csv')
CLEAN_DATASET = Path('../data/cleaned_humans.spol')


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
        writer = csv.writer(cleaned, delimiter=',')
        writer.writerow(['s', 'p', 'o'])
        with open(dataset_path, 'r') as data:
            dataset = data.readlines()
            for line in dataset[:20000]:
                split_line = line.split('\t')
                split_line.pop(3)
                if split_line[2] != '0':
                    writer.writerow(split_line)
                    # cleaned.write('\t'.join(split_line))


def process_dataset(dataset_path: Path,
                    filename: str | None = None,
                    save: bool = True,
                    size: int | None = None) -> list[list]:
    """
    Utility function that processes the dataset in a text
    format by returning properties and classes contained
    in it
    :param dataset_path: the path of the dataset
    :param filename: the name of the output file that is
    generated if the save parameter is set to True
    :param save: a boolean defining whether the result of
    the function has to be solved or not
    :param size: the size of the generated file expressed
    in lines, if the save parameter is set to True
    :return: a list of list containing all the properties and
    all the objects contained in the dataset, respectively
    """
    properties, objects = [], []
    with open(dataset_path, 'r') as data:
        dataset = data.readlines()
        for line in dataset[:size]:
            property, object = line.split('\t')[:2]
            properties.append(int(property))
            objects.append(int(object))
    if save:
        dump([properties, objects], f'../data/{filename}.joblib')
    return [properties, objects]


def process_csv(dataset_path: Path,
                filename: str,
                save: bool = True,
                size: int | None = None) -> list[list]:
    """

    :param dataset_path: the path of the dataset
    :param filename: the name of the output file that is
    generated if the save parameter is set to True
    :param save: a boolean defining whether the result of
    the function has to be solved or not
    :param size: the size of the generated file expressed
    in lines, if the save parameter is set to True
    :return: a list of list containing all the properties and
    all the objects contained in the dataset, respectively
    """
    with open(dataset_path, 'r') as data:
        csv_data = csv.reader(data)
        for row in csv_data:
            print(row)


if __name__ == '__main__':
    clean_dataset(DATASET, CSV_DATASET)
    # process_dataset(CLEAN_DATASET, 'toy_properties_object', size=1000)
