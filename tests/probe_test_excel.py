from repos_and_collections.excel_objects import ExcelCollectionSet
from pprint import PrettyPrinter
from deep_metamodeling.metamodels.m2_uml import Class, Property, Association, AssociationClass, CompositionGraph
from repos_and_collections.collections import Collection
from repos_and_collections.excel_objects import ExcelCollection
import networkx as nx

def main():

    '''
    Paths, etc. expect this to be run from tests directory on CLI
    :return:
    '''

    # So - how to do this? Should each class get its own section? How to know when to nest and when
    # to do more of a cross-reference? Also need to be careful to avoid recursion since UML graphs
    # often have many paths to get to a given attribute

    xl_collect = ExcelCollectionSet()

    pp = PrettyPrinter(indent=2)

    new_sheet = ExcelCollection()
    new_sheet.name = 'Car Data'

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

    prop1 = Property()
    prop2 = Property()
    prop3 = Property()
    prop4 = Property()
    prop5 = Property()
    prop6 = Property()
    prop7 = Property()
    prop8 = Property()
    prop9 = Property()

    prop1.name = 'front right'
    prop2.name = 'front left'
    prop3.name = 'rear right'
    prop4.name = 'rear left'
    prop5.name = 'diameter'
    prop6.name = 'radius'
    prop7.name = 'hub'
    prop8.name = 'tire'
    prop9.name = 'belt'

    class1.owned_attribute.append(prop1)
    class1.owned_attribute.append(prop2)
    class1.owned_attribute.append(prop3)
    class1.owned_attribute.append(prop4)

    class2.owned_attribute.append(prop5)
    class2.owned_attribute.append(prop6)
    class2.owned_attribute.append(prop7)
    class2.owned_attribute.append(prop8)

    class4.owned_attribute.append(prop9)

    prop1.type_.append(class2)
    prop2.type_.append(class2)
    prop3.type_.append(class2)
    prop4.type_.append(class2)

    prop7.type_.append(class3)
    prop8.type_.append(class4)
    prop4.type_.append(class5)

    test_graph = CompositionGraph(class1)

    pp.pprint(list(test_graph.comp_graph.edges()))

    pp.pprint(list(nx.topological_sort(test_graph.comp_graph)))

    pp.pprint(nx.out_degree_centrality(test_graph.comp_graph))

    leaf_list = []

    for key, val in nx.out_degree_centrality(test_graph.comp_graph).items():
        if val == 0.0:
            leaf_list.append(key)

    path_dict = {}

    for leaf in leaf_list:
        for tree_path in list(nx.all_shortest_paths(test_graph.comp_graph, class1.name, leaf)):
            path_builder = ''
            for indx, step in enumerate(tree_path):
                if indx == 0:
                    path_builder = step
                else:
                    path_builder = path_builder + '.' + step

            path_dict.update({path_builder: tree_path})

    pp.pprint(path_dict)

    new_sheet.add_graph(test_graph.comp_graph, class1.name)

    new_sheet.set_cells()

    #for child in root:
    #    split_tag = etree.QName(child.tag)
    #    if split_tag.localname == 'Model':
    #        # need something recursive here
    #        for next_child in child:
    #            split_tag = etree.QName(next_child.tag)
    #            print(split_tag.localname)
    #            pp.pprint(next_child.attrib)

if __name__ == "__main__":
    # run test from command line

    main()