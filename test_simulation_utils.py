import simulation_utils
from app import app
import json


# pylint: disable=fixme
# fmt:off
# TODO use dummy database


def does_simulation_type_exist(simulation_type_name):
    # Check if the simulation type is in the database
    assert (simulation_utils.get_simulation_type(simulation_type_name=simulation_type_name)) is not None, (
        "get_simulation_type() by simulation_type_name should return the test simulation type"
    )
    simulation_type_id = simulation_utils.get_simulation_type(simulation_type_name=simulation_type_name).id
    assert(simulation_utils.get_simulation_type(simulation_type_id=simulation_type_id)) is not None, "get_simulation_type() by id should return the test simulation type"
    assert(simulation_utils.get_simulation_type(simulation_type_name=simulation_type_name, simulation_type_id=simulation_type_id)) is not None, (
        "get_simulation_type() by simulation_type_name and id should return the test simulation type"
    )

    # Check if the simulation type is not in the database
    assert (simulation_utils.get_simulation_type(simulation_type_name="not_test_simulation_type_name")) is None,(
        "get_simulation_type() by simulation_type_name should not return the test simulation type"
    )
    assert (simulation_utils.get_simulation_type(simulation_type_id=-1)) is None, ( 
        "get_simulation_type() by wrong id should not return the test simulation type"
    )
    assert (simulation_utils.get_simulation_type(simulation_type_name="not_test_simulation_type_name", simulation_type_id=simulation_type_id)) is None, (
        "get_simulation_type() by wrong simulation_type_name and id should not return the test simulation type"
    )
    assert (simulation_utils.get_simulation_type(simulation_type_name=simulation_type_name, simulation_type_id=-1)) is None, (
        "get_simulation_type() by simulation_type_name and wrong id should not return the test simulation type"
    )


    # Check null inputs
    assert (simulation_utils.get_simulation_type()) is None, "get_simulation_type() with no arguments should return None"
    assert (simulation_utils.delete_simulation_type()) is None, "delete_simulation_type() with no arguments should return None"



def test_simulation_type_utils():
    
    simulation_type_name = "test_simulation_type_name"
    description = "test_description"
    with app.app_context():
        simulation_utils.create_simulation_type(simulation_type_name, description)
        
        # Check if the simulation type is in the database
        # does_simulation_type_exist(simulation_type_name)

        #update simulation type
        new_simulation_type_name = "new_test_simulation_type_name"
        new_description = "new_test_description"
        simulation_utils.update_simulation_type(
            simulation_type_name=simulation_type_name, name=new_simulation_type_name, description=new_description)
        does_simulation_type_exist(new_simulation_type_name)
        new_description = simulation_utils.get_simulation_type(simulation_type_name=new_simulation_type_name).description
        assert(new_description == "new_test_description"), "update_simulation_type() should update the description of the simulation type"

        simulation_type_id = simulation_utils.get_simulation_type(simulation_type_name=new_simulation_type_name).id
        # Delete the simulation type
        simulation_utils.delete_simulation_type(simulation_type_name=new_simulation_type_name)
        assert (simulation_utils.get_simulation_type(simulation_type_name=new_simulation_type_name)) is None, (
            "get_simulation_type() by simulation_type_name should not return the test simulation type after deletion"
        )
        assert(simulation_utils.get_simulation_type(simulation_type_id=simulation_type_id)) is None, (
            "get_simulation_type() by id should not return the test simulation type after deletion"
        )

def test_vehicle_utils():
    with app.app_context():
        name = "test_vehicle_name"
        description = "test_vehicle_description"
        # the next data goes in a json file
        sensor_information = {"sensor1": "sensor1_description", "sensor2": "sensor2_description"}
        physical_properties = {"property1": "property1_description", "property2": "property2_description"}
        # transform dictionaries to json
        sensor_information = json.dumps(sensor_information)
        physical_properties = json.dumps(physical_properties)

        # create vehicle
        simulation_utils.create_vehicle(name, description, sensor_information, physical_properties)

        # Check if the vehicle is in the database
        vehicle_id = simulation_utils.get_vehicle(vehicle_name=name).id
        assert(simulation_utils.get_vehicle(vehicle_id=vehicle_id)) is not None, "get_vehicle() by id should return the test vehicle"
        assert(simulation_utils.get_vehicle(vehicle_name=name)) is not None, "get_vehicle() by name should return the test vehicle"
        assert(simulation_utils.get_vehicle(vehicle_name=name, vehicle_id=vehicle_id)) is not None, (
            "get_vehicle() by name and id should return the test vehicle"
        )

        # Check if data checks out
        assert(simulation_utils.get_vehicle(vehicle_id=vehicle_id).name == name), "get_vehicle() should return the test vehicle"
        assert(simulation_utils.get_vehicle(vehicle_id=vehicle_id).description == description), "get_vehicle() should return the test vehicle"
        assert(simulation_utils.get_vehicle(vehicle_id=vehicle_id).sensor_information == sensor_information), "get_vehicle() should return the test vehicle"
        assert(simulation_utils.get_vehicle(vehicle_id=vehicle_id).physical_properties == physical_properties), "get_vehicle() should return the test vehicle"

        # Check null input
        assert(simulation_utils.get_vehicle()) is None, "get_vehicle() with no arguments should return None"
        
        # Delete vehicle
        simulation_utils.delete_vehicle(vehicle_id=vehicle_id)

        # Check if the vehicle is not in the database
        assert(simulation_utils.get_vehicle(vehicle_id=vehicle_id)) is None, "get_vehicle() by id should not return the test vehicle after deletion"
