import uuid
from uuid import UUID
import inspect
from lxml import etree

class Collection(object):
    '''
    A collection object serves as a container of convenience for multiple Python objects.
    It also provides a map from object to unique ID, and from unique ID to objects
    '''

    def __init__(self):
        self.id_to_object_map = {}
        self.object_to_id_map = {}
        self.collected_objects = []
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

    def resolve_references(self, id_of_obj_to_resolve):
        '''
        Look at all properties in an object and resolve them to in-memory links via the
        collection's internal id table
        :param id_of_obj_to_resolve: ID of object to have any UUID transformed into an in-memory link
        :return: None [state change in collection will be in given object]
        '''

        obj = self.id_to_object_map[id_of_obj_to_resolve]

        for attr in inspect.getmembers(obj):
            if attr[0][0] != '_' and isinstance(attr[1], UUID):
                obj_to_resolve = self.id_to_object_map[attr[1]]
                obj.__setattr__(attr[0], obj_to_resolve)

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
                id_to_deref_to = self.object_to_id_map[hex(id(attr[1]))]
                obj.__setattr__(attr[0], id_to_deref_to)

    def dump_obj_as_dict(self, id_of_obj_to_dump):
        '''
        Render object to a dictionary of fields
        :param id_of_obj_to_dump: ID of object to be returned as a dictionary
        :return: dict describing object
        '''

        obj = self.id_to_object_map[id_of_obj_to_dump]

        obj_dict = {}

        for prop in inspect.getmembers(obj):
            if prop[0][0] != '_':
                obj_dict.update({prop[0]: repr(prop[1])})

        return obj_dict

class CollectionMap():
    '''
    A map between collections to support comparison and transformation
    '''

    def __init__(self):
        self.collection_A_to_collection_B_map = {}
        self.collection_B_to_collection_A_map = {}