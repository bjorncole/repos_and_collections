from repos_and_collections.excel_objects import ExcelCollectionSet
from pprint import PrettyPrinter
from deep_metamodeling.metamodels.m2_uml import Class, Property, Association, AssociationClass, CompositionGraph
from repos_and_collections.collections import Collection
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

    new_sheet = Collection()
    new_sheet.name = 'Car Data'

    # Make up some fake UML data

    class1 = Class()
    class2 = Class()

    class1.name = 'Car'
    class2.name = 'Wheel'

    prop1 = Property()
    prop2 = Property()
    prop3 = Property()
    prop4 = Property()
    prop5 = Property()
    prop6 = Property()

    prop1.name = 'front right'
    prop2.name = 'front left'
    prop3.name = 'rear right'
    prop4.name = 'rear left'
    prop5.name = 'diameter'
    prop6.name = 'radius'

    class1.owned_attribute.append(prop1)
    class1.owned_attribute.append(prop2)
    class1.owned_attribute.append(prop3)
    class1.owned_attribute.append(prop4)

    class2.owned_attribute.append(prop5)

    prop1.type_.append(class2)
    prop2.type_.append(class2)
    prop3.type_.append(class2)
    prop4.type_.append(class2)

    test_graph = CompositionGraph(class1)

    pp.pprint(list(test_graph.comp_graph.edges()))

    pp.pprint(list(nx.topological_sort(test_graph.comp_graph)))

    pp.pprint(nx.out_degree_centrality(test_graph.comp_graph))

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