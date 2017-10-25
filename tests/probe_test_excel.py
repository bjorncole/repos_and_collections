from repos_and_collections.excel_objects import ExcelCollectionSet
from pprint import PrettyPrinter
from deep_metamodeling.metamodels.m2_uml import Class, Property, Association, AssociationClass
from repos_and_collections.collections import Collection

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

    prop1.name = 'front right'
    prop2.name = 'front left'
    prop3.name = 'rear right'
    prop4.name = 'rear left'
    prop5.name = 'diameter'

    class1.owned_attribute.append(prop1)
    class1.owned_attribute.append(prop2)
    class1.owned_attribute.append(prop3)
    class2.owned_attribute.append(prop4)

    class1.owned_attribute.append(prop5)

    for collection in xmi_collect.collection_list:
        pp.pprint(collection.id_to_object_map)

    for package in xmi_collect.collection_list:
        print('Object in ' + package.name)
        for collected in package.id_to_object_map:
            pp.pprint(package.dump_obj_as_dict(collected))

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