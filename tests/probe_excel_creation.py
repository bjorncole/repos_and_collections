from repos_and_collections.excel_objects import ExcelCollectionSet
from pprint import PrettyPrinter
from deep_metamodeling.metamodels.m2_uml import Class, Property, ValueType, CompositionGraph
from repos_and_collections.collections import Collection
from repos_and_collections.excel_objects import ExcelCollection
import networkx as nx
import openpyxl as xl
from openpyxl.utils import get_column_letter
from openpyxl.styles import Alignment, Border, Font, Side
from openpyxl.comments import Comment

def main():

    '''
    A test of the facilities to project a UML model into Excel as a tree of nested cells with names
    :return:
    '''

    # So - how to do this? Should each class get its own section? How to know when to nest and when
    # to do more of a cross-reference? Also need to be careful to avoid recursion since UML graphs
    # often have many paths to get to a given attribute

    xl_collect = ExcelCollectionSet()

    pp = PrettyPrinter(indent=2)

    xl_collection = ExcelCollection()
    xl_collection.row_headers = False
    xl_collection.name = 'Car Data'

    # Make up some fake UML data

    class1 = Class()
    class2 = Class()
    class3 = Class()
    class4 = Class()
    class5 = Class()

    class1.name = 'Car'
    class2.name = 'Wheel'
    class3.name = 'Hub'
    class4.name = 'Tire'
    class5.name = 'Belt'

    vt1 = ValueType()
    vt2 = ValueType()

    vt1.name = "inches"
    vt1.unit = 'in'
    vt1.quantity_kind = 'length'

    vt2.name = "PSI"
    vt2.unit = 'psi'
    vt2.quantity_kind = 'pressure'

    prop1 = Property()
    prop2 = Property()
    prop3 = Property()
    prop4 = Property()
    prop5 = Property()
    prop6 = Property()
    prop7 = Property()
    prop8 = Property()
    prop9 = Property()
    prop10 = Property()

    prop1.name = 'front right'
    prop2.name = 'front left'
    prop3.name = 'rear right'
    prop4.name = 'rear left'
    prop5.name = 'diameter'
    prop6.name = 'thickness'
    prop7.name = 'hub'
    prop8.name = 'tire'
    prop9.name = 'belt'
    prop10.name = 'pressure'

    class1.owned_attribute.append(prop1)
    class1.owned_attribute.append(prop2)
    class1.owned_attribute.append(prop3)
    class1.owned_attribute.append(prop4)

    class2.owned_attribute.append(prop5)
    class2.owned_attribute.append(prop6)
    class2.owned_attribute.append(prop7)
    class2.owned_attribute.append(prop8)

    class4.owned_attribute.append(prop9)
    class4.owned_attribute.append(prop10)

    prop1.type_.append(class2)
    prop2.type_.append(class2)
    prop3.type_.append(class2)
    prop4.type_.append(class2)

    prop5.type_.append(vt1)
    prop6.type_.append(vt1)

    prop7.type_.append(class3)
    prop8.type_.append(class4)
    prop9.type_.append(class5)

    prop10.type_.append(vt2)

    starting_class = class1

    test_graph = CompositionGraph(starting_class)

    pp.pprint(nx.out_degree_centrality(test_graph.comp_graph))

    leaf_list = []

    for key, val in nx.out_degree_centrality(test_graph.comp_graph).items():
        if val == 0.0:
            leaf_list.append(key)

    xl_collection.add_graph(test_graph.comp_graph,
                            starting_class.name,
                            {starting_class.name : {'type_': starting_class.name}})

    xl_collection.build_cell_dict()

    for grph in xl_collection.graphs:
        pp.pprint(grph.path_dict)

    wb = xl.Workbook()
    sht = wb.active
    sht.title = xl_collection.name

    xl_collection.build_sheet(sht, test_graph)

    wb.save('TestWorkbook.xlsx')

if __name__ == "__main__":
    # run test from command line

    main()

