"""

"""


def parallel_load_map(i, row, __df, subjects_mapping, objects_mapping,
                      properties_mapping):
    """

    :return:
    """
    i += 1
    if i % 1000000 == 0:
        print(i, "mapping rows processed...")
    identifier = int(row[0])
    if identifier in __df['s'].values:
        subjects_mapping[identifier] = row[1]
        print('found in subjects: ', identifier, ":", row[1])
    if identifier in __df['o'].values:
        objects_mapping[identifier] = row[1]
        print('found in objects: ', identifier, ":", row[1])
    if identifier in __df['p'].values:
        properties_mapping[identifier] = row[1]
        print('found in properties: ', identifier, ":", row[1])
