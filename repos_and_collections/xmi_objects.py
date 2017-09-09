from lxml import etree

class XMICollectionSet():
    '''
    A collection with tailored methods for loading, saving, and handling XMI
    '''

    def load_from_file(self, file_path):
        loaded_xmi = open(file_path, 'r')

        load_up = etree.parse(loaded_xmi)

        self.initial_parse(load_up)

        return load_up

    def initial_parse(self, loaded_up):
        '''
        Method to take raw XMI input and turn it into collection of usable objects
        :param loaded_up: XMI after parsing by LXML
        :return: None [will have objects loaded into internal collection]
        '''

        # start by finding the base model

        root = loaded_up.getroot()

        # recursively get all packages and create separate collections
        # (there is a chance to recombine them later and look to support resolving
        # references at that point)

        for child in root:
            split_tag = etree.QName(child.tag)
            if split_tag.localname == 'Model':
                all_packages = self.collect_subpackages(child)

        for package in all_packages:
            for attribute in package.attrib.keys():
                split_key = etree.QName(attribute)
                # cycle through the keys (can get more efficient once we learn how
                # to compose keys with namespaces
                if split_key.localname == 'name':
                    print(package.attrib[attribute])

        for package in all_packages:
            for packedElement in package:
                split_tag = etree.QName(packedElement.tag)
                if split_tag.localname == 'packagedElement':
                    thing_name = ''
                    thing_type = ''
                    for attribute in packedElement.attrib.keys():
                        split_key = etree.QName(attribute)
                        # cycle through the keys (can get more efficient once we learn how
                        # to compose keys with namespaces
                        if split_key.localname == 'name':
                            thing_name = packedElement.attrib[attribute]
                        if split_key.localname == 'type':
                            thing_type = packedElement.attrib[attribute]
                    print(thing_type + ' ' + thing_name)

    def collect_subpackages(self, current_package):
        gathered_packages = []
        # need something recursive here
        for next_child in current_package:
            split_tag = etree.QName(next_child.tag)
            # subpackage will always be a packaged element
            if split_tag.localname == 'packagedElement':
                for attribute in next_child.attrib.keys():
                    split_key = etree.QName(attribute)
                    # cycle through the keys (can get more efficient once we learn how
                    # to compose keys with namespaces
                    if split_key.localname == 'type':
                        print(split_tag.localname)
                        print(next_child.attrib[attribute])
                        # check for package type
                        if next_child.attrib[attribute] == 'uml:Package':
                            # add to current list and then recurse
                            gathered_packages.append(next_child)
                            new_packages = self.collect_subpackages(next_child)

                            gathered_packages.extend(new_packages)

        return gathered_packages