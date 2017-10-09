from repos_and_collections.xmi_objects import XMICollectionSet
from pprint import PrettyPrinter

def main():

    '''
    Paths, etc. expect this to be run from tests directory on CLI
    :return:
    '''

    xmi_collect = XMICollectionSet()
    xmi_tree = xmi_collect.load_from_file('../test_data/Transfer Tests Round 3.xml')

    pp = PrettyPrinter(indent=2)

    #root = xmi_tree.getroot()

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