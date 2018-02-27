import logging

from repos_and_collections.collections import Collection
from .fixture_data_generator1 import create_some_objects, create_some_objects_with_properties, \
    create_some_objects_with_properties_id, create_some_objects_with_intersting_properties
import sys

def dumb_function(x):
	return 1

def test_dumb():
    '''
    Basic test of test functionality
    '''

    logging.basicConfig(filename="test.log", filemode='w', level=logging.DEBUG)

    assert dumb_function(1) == 0

def test_add_to_collection():

    '''
    Adding a new item should expand the dictionary with a key that is a new unique
    identifier and a value that is the new object, add object to internal list
    :return: None
    '''

    logging.debug('Running test test_add_to_collection')

    module = sys.modules[__name__]

    working_dict = create_some_objects()

    for name, value in working_dict.items():
        setattr(module, name, value)

    tested_collection = Collection()

    tested_collection.add_object_to_collection(dummy_car)

    tested_collection.add_object_to_collection(dummy_LR_wheel)
    tested_collection.add_object_to_collection(dummy_LF_wheel)
    tested_collection.add_object_to_collection(dummy_RR_wheel)
    tested_collection.add_object_to_collection(dummy_RF_wheel)

    # use trick for loading up the objects

    assert len(tested_collection) == 5
    assert len(tested_collection.collected_objects) == 5

    assert dummy_car in tested_collection.collected_objects
    assert dummy_car in tested_collection.id_to_object_map.values()
    assert hex(id(dummy_car)) in tested_collection.object_to_id_map.keys()

def test_del_from_collection():
    '''
    Removing an item from the dictionary should drop the key that is
    identifier and a value that is the new object, also remove object from internal list
    :return: None
    '''

    logging.debug('Running test test_del_from_collection')

    module = sys.modules[__name__]

    working_dict = create_some_objects()

    for name, value in working_dict.items():
        setattr(module, name, value)

    tested_collection = Collection()

    tested_collection.add_object_to_collection(dummy_car)

    tested_collection.add_object_to_collection(dummy_LR_wheel)
    tested_collection.add_object_to_collection(dummy_LF_wheel)
    tested_collection.add_object_to_collection(dummy_RR_wheel)
    tested_collection.add_object_to_collection(dummy_RF_wheel)

    id_to_pull = tested_collection.object_to_id_map[hex(id(dummy_LR_wheel))]

    assert len(tested_collection) == 5
    assert len(tested_collection.collected_objects) == 5

    tested_collection.remove_object_from_collection(id_to_pull)

    assert len(tested_collection) == 4
    assert len(tested_collection.collected_objects) == 4

    assert dummy_car in tested_collection.collected_objects
    assert dummy_LR_wheel not in tested_collection.collected_objects

def test_del_from_collection_via_constraint():

    logging.debug('Running test test_del_from_collection_via_constraint')

    module = sys.modules[__name__]

    working_dict = create_some_objects()

    for name, value in working_dict.items():
        setattr(module, name, value)

    tested_collection = Collection()

    tested_collection.add_object_to_collection(dummy_car)

    tested_collection.add_object_to_collection(dummy_LR_wheel)
    tested_collection.add_object_to_collection(dummy_LF_wheel)
    tested_collection.add_object_to_collection(dummy_RR_wheel)
    tested_collection.add_object_to_collection(dummy_RF_wheel)

    id_to_pull = tested_collection.object_to_id_map[hex(id(dummy_LR_wheel))]

    assert len(tested_collection) == 5
    assert len(tested_collection.collected_objects) == 5

    tested_collection.remove_object_from_collection(id_to_pull)

    assert tested_collection.check_internal_constraints()

def test_del_from_collection_fixed_id():
    '''
    Removing an item from the dictionary should drop the key that is
    identifier and a value that is the new object, also remove object from internal list
    :return: None
    '''

    logging.debug('Running test test_del_from_collection_fixed_id')

    module = sys.modules[__name__]

    working_dict = create_some_objects()

    for name, value in working_dict.items():
        setattr(module, name, value)

    tested_collection = Collection()

    tested_collection.add_object_to_collection_with_id(dummy_car, 'xyz_car')

    tested_collection.add_object_to_collection_with_id(dummy_LR_wheel, 'xyz_LR')
    tested_collection.add_object_to_collection_with_id(dummy_LF_wheel, 'xyz_LF')
    tested_collection.add_object_to_collection_with_id(dummy_RR_wheel, 'xyz_RR')
    tested_collection.add_object_to_collection_with_id(dummy_RF_wheel, 'xyz_RF')

    assert len(tested_collection) == 5
    assert len(tested_collection.collected_objects) == 5

    tested_collection.remove_object_from_collection('xyz_LF')
    tested_collection.remove_object_from_collection('xyz_RF')
    tested_collection.remove_object_from_collection('xyz_car')

    assert len(tested_collection) == 2
    assert len(tested_collection.collected_objects) == 2

    assert dummy_LR_wheel in tested_collection.collected_objects
    assert dummy_car not in tested_collection.collected_objects
    assert dummy_RF_wheel not in tested_collection.collected_objects

def test_del_from_collection_fixed_id():
    '''
    Removing an item from the dictionary should drop the key that is
    identifier and a value that is the new object, also remove object from internal list
    :return: None
    '''

    logging.debug('Running test test_del_from_collection_fixed_id')

    module = sys.modules[__name__]

    working_dict = create_some_objects_with_properties_id()

    for name, value in working_dict.items():
        setattr(module, name, value)

    tested_collection = Collection()

    tested_collection.add_object_to_collection_with_id(dummy_car, 'xyz_car')

    tested_collection.add_object_to_collection_with_id(dummy_LR_wheel, 'xyz_LR')
    tested_collection.add_object_to_collection_with_id(dummy_LF_wheel, 'xyz_LF')
    tested_collection.add_object_to_collection_with_id(dummy_RR_wheel, 'xyz_RR')
    tested_collection.add_object_to_collection_with_id(dummy_RF_wheel, 'xyz_RF')

    tested_collection.add_object_to_collection_with_id(dummy_grocery1, 'DG1')
    tested_collection.add_object_to_collection_with_id(dummy_grocery2, 'DG2')

    print(tested_collection.dump_obj_as_dict('xyz_car'))

    tested_collection.resolve_references('xyz_car')

    print(tested_collection.dump_obj_as_dict('xyz_car'))

    print(tested_collection.live_link_reverse_lookup)

    assert len(tested_collection) == 7
    assert len(tested_collection.collected_objects) == 7

    tested_collection.remove_object_from_collection('xyz_LF')
    tested_collection.remove_object_from_collection('xyz_RF')

    print(tested_collection.dump_obj_as_dict('xyz_car'))

    tested_collection.dereference_links('xyz_car')

    assert len(tested_collection) == 5
    assert len(tested_collection.collected_objects) == 5

def test_del_from_collection_post_deref():
    '''
    Removing an item from the dictionary should drop the key that is
    identifier and a value that is the new object, also remove object from internal list
    :return: None
    '''

    logging.debug('Running test test_del_from_collection_post_deref')

    module = sys.modules[__name__]

    working_dict = create_some_objects_with_properties_id()

    for name, value in working_dict.items():
        setattr(module, name, value)

    tested_collection = Collection()

    tested_collection.add_object_to_collection_with_id(dummy_car, 'xyz_car')

    tested_collection.add_object_to_collection_with_id(dummy_LR_wheel, 'xyz_LR')
    tested_collection.add_object_to_collection_with_id(dummy_LF_wheel, 'xyz_LF')
    tested_collection.add_object_to_collection_with_id(dummy_RR_wheel, 'xyz_RR')
    tested_collection.add_object_to_collection_with_id(dummy_RF_wheel, 'xyz_RF')

    tested_collection.add_object_to_collection_with_id(dummy_grocery1, 'DG1')
    tested_collection.add_object_to_collection_with_id(dummy_grocery2, 'DG2')

    print(tested_collection.dump_obj_as_dict('xyz_car'))

    tested_collection.resolve_references('xyz_car')

    print(tested_collection.dump_obj_as_dict('xyz_car'))

    print(tested_collection.live_link_reverse_lookup)

    assert len(tested_collection) == 7
    assert len(tested_collection.collected_objects) == 7

    tested_collection.remove_object_from_collection('xyz_LF')
    tested_collection.remove_object_from_collection('xyz_RF')

    tested_collection.remove_object_from_collection('DG1')

    print(tested_collection.dump_obj_as_dict('xyz_car'))

    tested_collection.dereference_links('xyz_car')

    assert len(tested_collection) == 4
    assert len(tested_collection.collected_objects) == 4

def test_deref_ints_bools_nulls():
    '''
        Removing an item from the dictionary should drop the key that is
        identifier and a value that is the new object, also remove object from internal list
        :return: None
        '''

    logging.debug('Running test test_deref_ints_bools_nulls')

    module = sys.modules[__name__]

    working_dict = create_some_objects_with_intersting_properties()

    for name, value in working_dict.items():
        setattr(module, name, value)

    tested_collection = Collection()

    tested_collection.add_object_to_collection_with_id(dummy_car, 'xyz_car')

    tested_collection.add_object_to_collection_with_id(dummy_LR_wheel, 'xyz_LR')
    tested_collection.add_object_to_collection_with_id(dummy_LF_wheel, 'xyz_LF')
    tested_collection.add_object_to_collection_with_id(dummy_RR_wheel, 'xyz_RR')
    tested_collection.add_object_to_collection_with_id(dummy_RF_wheel, 'xyz_RF')

    tested_collection.add_object_to_collection_with_id(dummy_grocery1, 'DG1')
    tested_collection.add_object_to_collection_with_id(dummy_grocery2, 'DG2')

    print(tested_collection.dump_obj_as_dict('xyz_car'))

    tested_collection.resolve_references('xyz_car')

    print(tested_collection.dump_obj_as_dict('xyz_car'))

    print(tested_collection.live_link_reverse_lookup)

    assert len(tested_collection) == 7
    assert len(tested_collection.collected_objects) == 7

    tested_collection.remove_object_from_collection('xyz_LF')
    tested_collection.remove_object_from_collection('xyz_RF')

    tested_collection.remove_object_from_collection('DG1')

    logging.debug('Post removal state: {0}'.format(tested_collection.dump_obj_as_dict('xyz_car')))

    tested_collection.dereference_links('xyz_car')

    assert len(tested_collection) == 4
    assert len(tested_collection.collected_objects) == 4

def test_no_resolve_against_self():
    logging.debug('Running test test_no_resolve_against_self')

    module = sys.modules[__name__]

    working_dict = create_some_objects_with_intersting_properties()

    for name, value in working_dict.items():
        setattr(module, name, value)

    tested_collection = Collection()

    tested_collection.add_object_to_collection_with_id(dummy_car, 'xyz_car')

    tested_collection.add_object_to_collection_with_id(dummy_LR_wheel, 'xyz_LR')
    tested_collection.add_object_to_collection_with_id(dummy_LF_wheel, 'xyz_LF')
    tested_collection.add_object_to_collection_with_id(dummy_RR_wheel, 'xyz_RR')
    tested_collection.add_object_to_collection_with_id(dummy_RF_wheel, 'xyz_RF')

    tested_collection.add_object_to_collection_with_id(dummy_grocery1, 'DG1')
    tested_collection.add_object_to_collection_with_id(dummy_grocery2, 'DG2')

    dummy_car.idiot_reference = 'xyz_car'

    tested_collection.resolve_references('xyz_car')

    assert dummy_car.idiot_reference == 'xyz_car'