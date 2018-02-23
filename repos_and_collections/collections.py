import uuid
from uuid import UUID
import inspect
from lxml import etree
import copy

class Collection(object):
    '''
    A collection object serves as a container of convenience for multiple Python objects.
    It also provides a map from object to unique ID, and from unique ID to objects
    '''

    def __init__(self):
        self.id_to_object_map = {}
        self.object_to_id_map = {}
        self.collected_objects = []
        self.live_link_reverse_lookup = {}
        self.name = ''

    def __len__(self):
        return len(self.collected_objects)

    def __str__(self):
        return 'Collection with {0} members'.format(len(self))

    def add_object_to_collection(self, added_object):
        '''
        Add an object to the collection and assign it a unique id
        :param added_object: object to add to the collection
        :return: None
        '''

        new_id = uuid.uuid4()

        self.id_to_object_map.update({new_id: added_object})

        self.object_to_id_map.update({hex(id(added_object)): new_id})

        self.collected_objects.append(added_object)

    def add_object_to_collection_with_id(self, added_object, id_to_use):
        '''
        Add an object to the collection and assign it a unique id
        :param added_object: object to add to the collection
        :param id_to_use: id to apply to the addition
        :return: None
        '''

        self.id_to_object_map.update({id_to_use: added_object})

        self.object_to_id_map.update({hex(id(added_object)): id_to_use})

        self.collected_objects.append(added_object)

    def add_set_to_collection(self, added_objects):

        '''
        Add many objects to the collection and assign unique ids
        :param added_objects: objects to add to the collection
        :return: None
        '''

        for added_object in added_objects:
            new_id = uuid.uuid4()

            self.id_to_object_map.update({new_id: added_object})
            self.object_to_id_map.update({hex(id(added_object)): new_id})

            self.collected_objects.append(added_object)

    def remove_object_from_collection(self, id_to_remove):
        '''
        Remove an object from the collection
        :param id_to_remove: id from collection for object to remove
        :return: None
        '''
        # test if the removal is requested by object or by id

        object_to_pull = self.id_to_object_map[id_to_remove]

        # need to use the reverse directory to return live references to UUID's

        if (id_to_remove in self.live_link_reverse_lookup):
            for live_ref in self.live_link_reverse_lookup[id_to_remove]:

                obj = self.id_to_object_map[live_ref]

                for attr in inspect.getmembers(obj):
                    if attr[0][0] != '_' and not isinstance(attr[1], UUID) and not isinstance(attr[1], str):
                        if not isinstance(attr[1], list):
                            try:
                                id_to_deref_to = self.object_to_id_map[hex(id(attr[1]))]
                                if (id_to_remove == id_to_deref_to):
                                    obj.__setattr__(attr[0], id_to_deref_to)

                            except KeyError:
                                pass
                        else:
                            new_list = copy.copy(attr[1])
                            touched = False
                            for item in attr[1]:
                                if not (isinstance(item, UUID) or isinstance(item, str)):
                                    try:
                                        id_to_deref_to = self.object_to_id_map[hex(id(item))]
                                        if (id_to_remove == id_to_deref_to):
                                            new_list.append(id_to_deref_to)
                                            new_list.remove(item)
                                            touched = True
                                    # if general strings are accepted, they may not be in the map
                                    except KeyError:
                                        pass
                            if touched:
                                obj.__setattr__(attr[0], new_list)

        del self.id_to_object_map[id_to_remove]
        del self.object_to_id_map[hex(id(object_to_pull))]

        self.collected_objects.remove(object_to_pull)


    def check_internal_constraints(self):
        '''
        Check that the constraints of this construct are still satisfied:
        - same object appears in id to object map, object to id map, and collected objects
        - all objects are unique

        :return: True for constraints satisfied, False otherwise
        '''

        # Check that each entry in the id to object map appears in other two collections

        all_found = True

        for id_found in self.id_to_object_map:
            obj_found = self.id_to_object_map[id_found]
            obj_hex = hex(id(obj_found))
            if not(obj_hex in self.object_to_id_map and obj_found in self.collected_objects):
                all_found = False

        # Check that each entry in the hex map has a live object related to it

        hex_all_found = True

        for hex_found in self.object_to_id_map:
            id_found = self.object_to_id_map[hex_found]
            obj_found = self.id_to_object_map[id_found]

            if not(obj_found in self.collected_objects):
                hex_all_found = False

        return all_found and hex_all_found


    def resolve_references(self, id_of_obj_to_resolve):
        '''
        Look at all properties in an object and resolve them to in-memory links via the
        collection's internal id table
        :param id_of_obj_to_resolve: ID of object to have any UUID transformed into an in-memory link
        :return: None [state change in collection will be in given object]
        '''

        obj = self.id_to_object_map[id_of_obj_to_resolve]

        for attr in inspect.getmembers(obj):
            if attr[0][0] != '_' and attr[0] != 'name' and attr[0] != 'literals_cache' \
                    and attr[0] != 'references_cache' and (isinstance(attr[1], UUID) \
                                                                   or isinstance(attr[1], str) or isinstance(
                attr[1], list)):
                if not isinstance(attr[1], list):
                    try:
                        print('Looking to resolve id ' + str(attr[1]) + ' for property ' + attr[0])
                        obj_to_resolve = self.id_to_object_map[attr[1]]
                        obj.__setattr__(attr[0], obj_to_resolve)
                        if (attr[1] in self.live_link_reverse_lookup):
                            self.live_link_reverse_lookup[attr[1]].append(id_of_obj_to_resolve)
                        else:
                            self.live_link_reverse_lookup.update({attr[1]: [id_of_obj_to_resolve]})
                    # if general strings are accepted, they may not be in the map
                    except KeyError:
                        print('Failed')
                        pass

                else:
                    new_list = copy.copy(attr[1])
                    touched = False
                    for item in attr[1]:
                        if (isinstance(item, UUID) or isinstance(item, str)):
                            try:
                                obj_to_resolve = self.id_to_object_map[item]
                                new_list.append(obj_to_resolve)
                                new_list.remove(item)
                                touched = True
                                if (item in self.live_link_reverse_lookup):
                                    self.live_link_reverse_lookup[item].append(id_of_obj_to_resolve)
                                else:
                                    self.live_link_reverse_lookup.update({item: [id_of_obj_to_resolve]})
                            # if general strings are accepted, they may not be in the map
                            except KeyError:
                                pass
                    if touched:
                        obj.__setattr__(attr[0], new_list)

    def dereference_links(self, id_of_obj_to_deref):
        '''
        Look at all properties in an object and set property references to UUID's rather than
        the in-memory versions
        :param id_of_obj_to_deref: ID of object to have in-memory links rendered as UUID references
        :return: None [state change in collection will be in given object]
        '''

        obj = self.id_to_object_map[id_of_obj_to_deref]

        for attr in inspect.getmembers(obj):
            if attr[0][0] != '_' and not isinstance(attr[1], UUID) and not isinstance(attr[1], str):
                if not isinstance(attr[1], list):
                    try:
                        id_to_deref_to = self.object_to_id_map[hex(id(attr[1]))]
                        obj.__setattr__(attr[0], id_to_deref_to)
                    except KeyError:
                        print('Failed to match key hex ' + hex(id(attr[1])) + ' on property ' + attr[0])
                        raise KeyError
                else:
                    new_list = copy.copy(attr[1])
                    touched = False
                    for item in attr[1]:
                        if not (isinstance(item, UUID) or isinstance(item, str)):
                            try:
                                id_to_deref_to = self.object_to_id_map[hex(id(item))]
                                new_list.append(id_to_deref_to)
                                new_list.remove(item)
                                touched = True
                            # if general strings are accepted, they may not be in the map
                            except KeyError:
                                pass
                    if touched:
                        obj.__setattr__(attr[0], new_list)

    def dump_obj_as_dict(self, id_of_obj_to_dump):
        '''
        Render object to a dictionary of fields
        :param id_of_obj_to_dump: ID of object to be returned as a dictionary
        :return: dict describing object
        '''

        obj = self.id_to_object_map[id_of_obj_to_dump]

        obj_dict = {}

        for prop in inspect.getmembers(obj):
            if prop[0][0] != '_' and not callable(prop[1]) and \
                prop[0] != 'literals_cache' and prop[0] != 'references_cache' and \
                    prop[0].find('__meta') == -1:
                obj_dict.update({prop[0]: repr(prop[1])})

        return obj_dict

class CollectionMap():
    '''
    A map between collections to support comparison and transformation
    '''

    def __init__(self):
        self.collection_A_to_collection_B_map = {}
        self.collection_B_to_collection_A_map = {}