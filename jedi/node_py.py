"""

"""
import pickle
from csv import reader

from graphviz import Digraph
from joblib import delayed, Parallel

from parallel_utils import parallel_load_map
from label_map import get_label_from_id


class Node:
    __counter = 0

    # all properties of the loaded dataframe of a node
    def __properties(self):
        return self.__df['p']

    # all subjects of the loaded dataframe of a node
    def __subjects(self):
        return self.__df['s']

    # all subjects of the loaded dataframe of a node
    def __objects(self):
        return self.__df['o']

    # all distinct properties of the loaded dataframe of a node
    def __properties_unique(self):
        return self.__properties().unique()

    # all distinct subjects of the loaded dataframe of a node
    def __subjects_unique(self):
        return self.__subjects().unique()

    # all distinct subjects of the loaded dataframe of a node
    def __objects_unique(self):
        return self.__objects().unique()

    # the *n* most used properties of the loaded dataframe of a node
    def __most_used_properties(self, n=10):
        return self.__properties().value_counts()[0:n].index

    # the rows that use the most used property of the loaded dataframe of a node
    def __rows_for_most_used_property(self):
        return self.__df.loc[self.__df['p'] == self.__most_used_property]

    # the rows of subjects that use the most used property of
    # the loaded dataframe of a node
    def __rows_for_subjects_using_most_used_property(self):
        subjects = self.__rows_for_most_used_property()['s'].values
        rows = self.__df.loc[self.__df['s'].isin(subjects)]
        return rows.loc[rows['p'] != self.__most_used_property]

    # the complement of rows of subjects that use the most used property
    # of the loaded dataframe of a node
    def __complement_for_subjects_using_most_used_property(self):
        subjects = self.__rows_for_most_used_property()['s'].values
        rows = self.__df.loc[~self.__df['s'].isin(subjects)]
        return rows

    # constructor taking a KG in pandas dataframe format
    def __init__(self, dataframe):
        self.objects_mapping = None
        self.properties_mapping = None
        self.subjects_mapping = None
        Node.__counter += 1
        self.__identifier = Node.__counter
        self.__df = dataframe.copy()
        self.__most_used_property = self.__most_used_properties(1)[0]

        right_rows = self.__complement_for_subjects_using_most_used_property()
        if right_rows.empty:
            self.right = None
        else:
            self.right = Node(right_rows)

        left_rows = self.__rows_for_subjects_using_most_used_property()
        if left_rows.empty:
            self.left = None
        else:
            self.left = Node(left_rows)

    # print some interesting stats of the subgraph this node represents
    def print_stats(self):
        print("======================================================")
        print("node: ", self.__identifier)
        print("number of rows: ", len(self.__df))
        print("distinct property count: ", len(self.__properties_unique()))
        print("distinct subject count: ", len(self.__subjects_unique()))
        print("most used property:", self.__most_used_property)
        print("property label:", get_label_from_id(self.__most_used_property))
        print("======================================================")

    # print a graphviz representation of the constructed tree
    def print_graph(self, dot=Digraph()):
        args = (
            self.__most_used_property,
            len(self.__df),
            len(self.__subjects_unique()),
            len(self.__properties_unique()),
            len(self.__objects_unique()),
        )
        label = """
            most used property: {0}
            #distinct statements: {1}
            #distinct instances: {2}
            #distinct properties: {3}
            #distinct objects: {4}
        """.format(*args)
        dot.node(name=str(self.__identifier), label=label,
                 URL=str(self.__most_used_property))
        if self.left is not None:
            self.left.print_graph(dot)
            dot.edge(str(self.__identifier), str(self.left.__identifier),
                     label="next most used property")
        if self.right is not None:
            self.right.print_graph(dot)
            dot.edge(str(self.__identifier), str(self.right.__identifier),
                     label="complement")
        return dot

    # loads a mapping in form of csv for the identifiers of the KG
    # and stores them in internal dict mappings
    def load_map(self, mapping_file):
        self.subjects_mapping = {}
        self.properties_mapping = {}
        self.objects_mapping = {}
        with open(mapping_file) as f:
            with open(mapping_file, 'r') as read_obj:
                csv_reader = reader(read_obj, delimiter='\t')
                i = 0
                Parallel(n_jobs=-1)(
                    delayed(parallel_load_map)(i, row, self.__df,
                                               self.subjects_mapping,
                                               self.objects_mapping,
                                               self.properties_mapping) for row
                    in csv_reader)

    # applies internal mappings to the rows of the internal
    # dataframe - recursively
    def apply_map(self):
        if self.subjects_mapping and self.properties_mapping and self.objects_mapping:
            self.map_replace(self.subjects_mapping, self.objects_mapping,
                             self.properties_mapping)
        else:
            raise Exception(
                "Apply map require a loaded map! Use load_map() first!")

    def map_replace(self, subjects, objects, properties):
        self.__df.replace({"s": subjects}, inplace=True)
        self.__df.replace({"o": objects}, inplace=True)
        self.__df.replace({"p": properties}, inplace=True)
        self.__most_used_property = self.__most_used_properties(1)[0]
        if self.left:
            self.left.map_replace(subjects, objects, properties)
        if self.right:
            self.right.map_replace(subjects, objects, properties)

    # stores this object for later use as a binary representation
    def serialize(self, filename):
        with open(filename, "wb") as file:
            pickle.dump(self, file)

    # loads object for reuse from a binary representation -
    # returns a full object of type Node()
    @staticmethod
    def deserialize(filename):
        with open(filename, "rb") as file:
            return pickle.load(file)
