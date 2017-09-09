from repos_and_collections.xmi_objects import XMICollectionSet

def main():

    '''
    Paths, etc. expect this to be run from tests directory on CLI
    :return:
    '''

    xmi_collect = XMICollectionSet()
    xmi_tree = xmi_collect.load_from_file('../test_data/Transfer Tests Round 3.xml')

    #pp = pprint.PrettyPrinter(indent=2)

    #root = xmi_tree.getroot()

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