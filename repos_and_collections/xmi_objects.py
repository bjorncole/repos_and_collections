from lxml import etree
from deep_metamodeling.metamodels.m2_uml import Class, Property, Association, AssociationClass
from repos_and_collections.collections import Collection

class XMICollectionSet(object):
    '''
    A collection with tailored methods for loading, saving, and handling XMI
    '''

    def __init__(self):
        self.collection_list = []

    def load_from_file(self, file_path):
        '''
        Process an XMI file into a set of collections (each Package becomes a collection)
        :param file_path: Location of XMI file
        :return: LXML parse root. Also alters internal state by populating self.collection_list with
        gathered UML Packages.
        '''
        loaded_xmi = open(file_path, 'r')

        load_up = etree.parse(loaded_xmi)

        package_list = self.initial_parse(load_up)

        # transform found packages into collections

        for package in package_list:
            model_collection = None
            for attribute in package.attrib.keys():
                split_key = etree.QName(attribute)
                # cycle through the keys (can get more efficient once we learn how
                # to compose keys with namespaces
                if split_key.localname == 'name':
                    model_collection = Collection()
                    model_collection.name = package.attrib[attribute]
                    self.collection_list.append(model_collection)
            for packedElement in package:
                split_tag = etree.QName(packedElement.tag)
                if split_tag.localname == 'packagedElement':
                    thing_name = ''
                    thing_type = ''
                    thing_id = ''
                    new_thing = None
                    added_properties = []
                    for attribute in packedElement.attrib.keys():
                        split_key = etree.QName(attribute)
                        # cycle through the keys (can get more efficient once we learn how
                        # to compose keys with namespaces
                        if split_key.localname == 'name':
                            thing_name = packedElement.attrib[attribute]
                        if split_key.localname == 'id':
                            thing_id = packedElement.attrib[attribute]
                        if split_key.localname == 'type':
                            thing_type = packedElement.attrib[attribute]
                            # add class to package to be part of collection

                            if packedElement.attrib[attribute] == 'uml:Class':
                                new_thing = Class()
                                added_properties = self.collect_attributes(packedElement)
                            elif packedElement.attrib[attribute] == 'uml:Association':
                                new_thing = Association()
                                added_properties = self.collect_attributes(packedElement)
                            elif packedElement.attrib[attribute] == 'uml:AssociationClass':
                                new_thing = AssociationClass()
                                added_properties = self.collect_attributes(packedElement)

                    # this logic needs to be recursive to handle owned elements and their specializations
                    if new_thing is not None and thing_name is not None:
                        new_thing.name = thing_name
                        print(thing_type + ' ' + thing_name + ' added to collection ' + model_collection.name)
                        model_collection.add_object_to_collection_with_id(new_thing, thing_id)
                        for new_prop in added_properties:
                            model_collection.add_object_to_collection_with_id(added_properties[new_prop], new_prop)

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

        #for package in all_packages:
        #    for attribute in package.attrib.keys():
        #        split_key = etree.QName(attribute)
        #        # cycle through the keys (can get more efficient once we learn how
        #        # to compose keys with namespaces
        #        if split_key.localname == 'name':
        #            print(package.attrib[attribute])

        return all_packages

    def collect_subpackages(self, current_package):
        '''
        Recursively gather packages from current point in XMI
        :param current_package: current package in navigation
        :return: all encountered packages so far
        '''
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

    def collect_attributes(self, current_class):
        '''
        Gather attributes of a class
        :param current_class:
        :return: all attributes parsed so far as Python Property objects
        '''

        sub_attributes = {}

        for next_att in current_class:
            split_tag = etree.QName(next_att.tag)
            # subpackage will always be a packaged element
            if split_tag.localname == 'ownedAttribute' or \
                split_tag.localname == 'ownedEnd' or \
                split_tag.localname == 'navigableOwnedEnd':
                thing_name = ''
                thing_type = ''
                thing_id = ''
                new_prop = None
                for attribute in next_att.attrib.keys():
                    split_key = etree.QName(attribute)
                    # cycle through the keys (can get more efficient once we learn how
                    # to compose keys with namespaces
                    if split_key.localname == 'name':
                        thing_name = next_att.attrib[attribute]
                    if split_key.localname == 'id':
                        thing_id = next_att.attrib[attribute]
                    if split_key.localname == 'type':
                        thing_type = next_att.attrib[attribute]
                        # add class to package to be part of collection

                        if next_att.attrib[attribute] == 'uml:Property':
                            new_prop = Property()

                # this logic needs to be recursive to handle owned elements and their specializations
                if new_prop is not None and thing_name is not None:
                    new_prop.name = thing_name
                    print('Property ' + thing_type + ' ' + thing_name + ' found')
                    sub_attributes.update({thing_id : new_prop})

        return sub_attributes