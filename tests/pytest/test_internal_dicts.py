from multi_repo.collections import Collection


def dumb_function(x):
	return 1

def test_dumb():
    '''
    Basic test of test functionality
    '''

    assert dumb_function(1) == 0

def test_add_to_collection():
    '''
    Adding a new item should expand the dictionary with a key that is a new unique
    identifier and a value that is the new object, add object to internal list
    :return: None
    '''

    assert dumb_function(1) == 0

def test_del_from_collection():
    '''
    Removing an item from the dictionary should drop the key that is
    identifier and a value that is the new object, also remove object from internal list
    :return: None
    '''

    assert dumb_function(1) == 0