# A way of putting classes into Excel and vice versa

import xlwings as xl
import inspect
import networkx as nx
from repos_and_collections.collections import Collection

class ExcelCollectionSet(object):
    '''
    Represents Excel workbooks as a set of collections, one per sheet
    '''

    def __init__(self):
        self.collection_list = []

    def write_to_excel(self):
        '''
        Writes to Excel as a graph, noting the path should ultimately terminate in individual values or a list
        (For example, tree of merged cells on the left via rows and lists expanding column-wise or the transpose)
        :return: None (side effect is a modified Excel sheet)
        '''

        max_graph_depth = 0

class ExcelCollection(Collection):

    '''
    Represents a collection of Excel objects (serializes as a single sheet)
    '''

    def __init__(self):
        super().__init__()
        # if true, put graph on first columns of sheet, if false put graph
        # on first rows of sheet
        self.row_headers = False
        self.graphs = []
        self.roots = []

    def add_graph(self, incoming_graph, incoming_root):
        new_graph = ExcelCellPath()
        new_graph.path_graph = incoming_graph
        self.graphs.append(new_graph)
        self.roots.append(incoming_root)

    def set_cells(self):
        total_max_depth = 0
        total_width = 0
        for indx, grph in enumerate(self.graphs):
            # get max depth and width for a given graph

            leaf_list = []

            for key, val in nx.out_degree_centrality(grph.path_graph).items():
                if val == 0.0:
                    leaf_list.append(key)

            # assume row-wise to start; can work transpose later

            cell_dict = {}

            path_dict = {}

            for leaf in leaf_list:
                for tree_path in list(nx.all_shortest_paths(grph.path_graph, self.roots[0], leaf)):
                    path_builder = ''
                    for indx, step in enumerate(tree_path):
                        if indx == 0:
                            path_builder = step
                        else:
                            path_builder = path_builder + '.' + step

                    path_dict.update({path_builder: tree_path})

            col_counter = 1

            for path in sorted(path_dict):
                print(path)
                if total_max_depth < len(path_dict[path]):
                    total_max_depth = len(path_dict[path])
                row_counter = len(path_dict[path])
                for indx2, step in enumerate(reversed(path_dict[path])):

                    if step in cell_dict:
                        current_list = cell_dict[step]
                        current_list.append([row_counter, col_counter])
                    else:
                        cell_dict.update({step: [[row_counter, col_counter]]})

                    row_counter = row_counter - 1

                col_counter = col_counter + 1

            total_width = col_counter - 1

            print('Max depth on cells = ' + repr(total_max_depth))
            print('Width of cells = ' + repr(total_width))

            print(repr(cell_dict))

class ExcelCellPath(object):
    '''
    A convenience class for calculating and holding the paths for value locations
    '''

    def __init__(self):
        self.path_graph = None

    def inspect_class(self, obj):
        '''

        :param obj: Python object to analyze
        :return: None (modifies internal state to have all paths accounted for)
        '''

    def add_attributes_to_graph(self, obj):
        '''
        Helper method to recurse a class
        :param obj:
        :return:
        '''