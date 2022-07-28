"""

"""
from pathlib import Path
import pandas as pd

import argparse


def resize_dataset(dataset_path: Path, output_path: str, num: int) -> None:
    """

    :param dataset_path:
    :param output_path:
    :param n:
    :return:
    """
    df = pd.read_csv(dataset_path, header=0, index_col=False)
    sample = df.sample(n=int(num), replace=True, ignore_index=True)
    # replacement = True
    sample.to_csv(output_path, encoding='utf-8', index=False)


if __name__ == '__main__':
    my_parser = argparse.ArgumentParser(prog='resize_dataset',
                                        description='List the content of a folder')

    my_parser.add_argument('--dataset_path', help='a first argument')
    my_parser.add_argument('--output_path', help='a second argument')
    my_parser.add_argument('--n', help='a first argument')

    args = my_parser.parse_args()

    resize_dataset(dataset_path=args.dataset_path, output_path=args.output_path, num=args.n)
