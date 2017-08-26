import uuid

class Collection(object):
    '''
    A collection object serves as a container of convenience for multiple Python objects.
    It also provides a map from object to unique ID, and from unique ID to objects
    '''

    def __init__(self):
        self.id_to_object_map = {}
        self.object_to_id_map = {}
        self.collected_objects = []

    def __sizeof__(self):
        return len(self.collected_objects)

    def __str__(self):
        return 'Collection with {0} members'.format(len(self))

    def add_object_to_collection(self, added_object):
        pass

    def add_set_to_collection(self, added_objects):
        pass

    def remove_object_from_collection(self, removed_object_or_id):
        # test if the removal is requested by object or by id
        if isinstance(removed_object_or_id, str):
            pass
        else:
            pass
        pass

    def check_internal_constraints(self):
        '''
        Check that the constraints of this construct are still satisfied:
        - same object appears in id to object map, object to id map, and collected objects
        - all objects are unique

        :return: True for constraints satisfied, False otherwise
        '''