from .test_types import TrialNamespace

def create_some_objects():
    '''
    Generate some Python objects to test collection functionality
    :return: a dictionary of new test objects
    '''

    dummy_car = TrialNamespace()
    dummy_car.object_name = 'Dummy Car'
    dummy_LR_wheel = TrialNamespace()
    dummy_LR_wheel.object_name = 'Dummy LR Wheel'
    dummy_LF_wheel = TrialNamespace()
    dummy_LF_wheel.object_name = 'Dummy LF Wheel'
    dummy_RR_wheel = TrialNamespace()
    dummy_RR_wheel.object_name = 'Dummy RR Wheel'
    dummy_RF_wheel = TrialNamespace()
    dummy_RF_wheel.object_name = 'Dummy RF Wheel'

    object_dict = {}

    object_dict.update({'dummy_car': dummy_car})
    object_dict.update({'dummy_LR_wheel': dummy_LR_wheel})
    object_dict.update({'dummy_LF_wheel': dummy_LF_wheel})
    object_dict.update({'dummy_RR_wheel': dummy_RR_wheel})
    object_dict.update({'dummy_RF_wheel': dummy_RF_wheel})

    return object_dict

def create_some_objects_with_properties():
    '''
    Generate some Python objects to test collection functionality
    :return: a dictionary of new test objects with properties
    '''

    dummy_car = TrialNamespace()
    dummy_car.object_name = 'Dummy Car'
    dummy_LR_wheel = TrialNamespace()
    dummy_LR_wheel.object_name = 'Dummy LR Wheel'
    dummy_LF_wheel = TrialNamespace()
    dummy_LF_wheel.object_name = 'Dummy LF Wheel'
    dummy_RR_wheel = TrialNamespace()
    dummy_RR_wheel.object_name = 'Dummy RR Wheel'
    dummy_RF_wheel = TrialNamespace()
    dummy_RF_wheel.object_name = 'Dummy RF Wheel'

    dummy_car.left_rear = dummy_LR_wheel
    dummy_car.left_front = dummy_LF_wheel
    dummy_car.right_rear = dummy_RR_wheel
    dummy_car.right_front = dummy_RF_wheel

    object_dict = {}

    object_dict.update({'dummy_car': dummy_car})
    object_dict.update({'dummy_LR_wheel': dummy_LR_wheel})
    object_dict.update({'dummy_LF_wheel': dummy_LF_wheel})
    object_dict.update({'dummy_RR_wheel': dummy_RR_wheel})
    object_dict.update({'dummy_RF_wheel': dummy_RF_wheel})

    return object_dict