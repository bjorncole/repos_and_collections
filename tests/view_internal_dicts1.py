from repos_and_collections.collections import Collection
from pytest.fixture_data_generator1 import create_some_objects
import pprint
import sys

def main():

    '''
    Adding a new item should expand the dictionary with a key that is a new unique
    identifier and a value that is the new object, add object to internal list
    :return: None
    '''

    module = sys.modules[__name__]

    pp = pprint.PrettyPrinter(indent=2)

    working_dict = create_some_objects()

    for name, value in working_dict.items():
        setattr(module, name, value)

    tested_collection = Collection()

    tested_collection.add_object_to_collection(dummy_car)

    tested_collection.add_object_to_collection(dummy_LR_wheel)
    tested_collection.add_object_to_collection(dummy_LF_wheel)
    tested_collection.add_object_to_collection(dummy_RR_wheel)
    tested_collection.add_object_to_collection(dummy_RF_wheel)

    print("\nAll objects in.\n")

    pp.pprint(repr(tested_collection.id_to_object_map))
    pp.pprint(repr(tested_collection.object_to_id_map))

    print("\nRemove Dummy LR Wheel\n")

    id_to_pull = tested_collection.object_to_id_map[hex(id(dummy_LR_wheel))]

    tested_collection.remove_object_from_collection(id_to_pull)

    pp.pprint(repr(tested_collection.id_to_object_map))
    pp.pprint(repr(tested_collection.object_to_id_map))


if __name__ == "__main__":
    # run test from command line

    main()