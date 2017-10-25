# A way of putting classes into Excel and vice versa

import xlwings as xl
import inspect
import networkx as nw
from collections import Collection

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