import simulation_utils
from app import app
from extensions import db
import json
import user_utils

# pylint: disable=fixme
# fmt:off
# TODO use dummy database


def create_simulation_type():
    simulation_type_name = "test_simulation_type_name"
    description = "test_description"
    return simulation_utils.create_simulation_type(simulation_type_name, description)

def create_new_vehicle():
    name = "test_vehicle_name"
    description = "test_vehicle_description"
    # the next data goes in a json file
    sensor_information = {"sensor1": "sensor1_description", "sensor2": "sensor2_description"}
    physical_properties = {"property1": "property1_description", "property2": "property2_description"}
    # transform dictionaries to json
    sensor_information = json.dumps(sensor_information)
    physical_properties = json.dumps(physical_properties)

    # create vehicle
    return simulation_utils.create_vehicle(name, description, sensor_information, physical_properties)


def create_simulation_config():
    # create simulation type
    simulation_type = create_simulation_type()
    simulation_type_id = simulation_type.id

    # create vehicle
    vehicle = create_new_vehicle()

    # create user
    username = "test_user_2"
    email = "test2@test.com"
    password = "password"
    user_utils.create_user(username, email, password)
    user_id = user_utils.find_user(username=username).id


    # create simulation config
    # the next data goes in a json file
    environmental_conditions = {"environmental1": "environmental1_description", "environmental2": "environmental2_description"}
    initial_conditions = {"initial1": "initial1_description", "initial2": "initial2_description"}
    physical_constants = {"constant1": "constant1_description", "constant2": "constant2_description"}
    time_settings = {"time1": "time1_description", "time2": "time2_description"}
    traffic_rules = {"rule1": "rule1_description", "rule2": "rule2_description"}
    success_definition = {"success1": "success1_description", "success2": "success2_description"}
    # transform dictionaries to json
    environmental_conditions = json.dumps(environmental_conditions)
    initial_conditions = json.dumps(initial_conditions)
    physical_constants = json.dumps(physical_constants)
    time_settings = json.dumps(time_settings)
    traffic_rules = json.dumps(traffic_rules)
    success_definition = json.dumps(success_definition)

    return simulation_utils.create_simulation_config(
        user_id,
        simulation_type_id,
        [vehicle.id],
        environmental_conditions,
        initial_conditions,
        physical_constants,
        time_settings,
        traffic_rules,
        success_definition
    )

def create_simulation_result():
    simulation_config = create_simulation_config()
    simulation_config_id = simulation_config.id
    success = {"Allowed_collisions": 0, "Allowed_near_misses": 0, "Reaction_time_needed_to_avoid_collision": 100}
    navigation_data = {"navigation1": "navigation1_description", "navigation2": "navigation2_description"}
    safety_metrics = {"safety1": "safety1_description", "safety2": "safety2_description"}
    vehicle_system_performance = {"performance1": "performance1_description", "performance2": "performance2_description"}
    # transform dictionaries to json
    success = json.dumps(success)
    navigation_data = json.dumps(navigation_data)
    safety_metrics = json.dumps(safety_metrics)
    vehicle_system_performance = json.dumps(vehicle_system_performance)

    return simulation_utils.create_simulation_result(
        simulation_config_id,
        success,
        navigation_data,
        safety_metrics,
        vehicle_system_performance
    )



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
    
    with app.app_context():
        db.drop_all()
        db.create_all()

        simulation_type = create_simulation_type()
        simulation_type_name = simulation_type.name
        # Check if the simulation type is in the database
        does_simulation_type_exist(simulation_type_name)

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
        db.drop_all()
        db.create_all()
        vehicle = create_new_vehicle()
        name = vehicle.name
        description = vehicle.description
        sensor_information = vehicle.sensor_information
        physical_properties = vehicle.physical_properties

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


def test_simulation_config():
    with app.app_context():
        db.drop_all()
        db.create_all()

        # create simulation config
        simulation_config = create_simulation_config()
        simulation_config_id = simulation_config.id
        user_id = simulation_config.user_id
        simulation_type_id = simulation_config.simulation_type_id
        vehicle = simulation_config.vehicles[0]
        environmental_conditions = simulation_config.environmental_conditions
        initial_conditions = simulation_config.initial_conditions
        physical_constants = simulation_config.physical_constants
        time_settings = simulation_config.time_settings
        traffic_rules = simulation_config.traffic_rules
        success_definition = simulation_config.success_definition


        # Check if the simulation config is in the database
        assert(simulation_utils.get_simulation_config(simulation_config_id=simulation_config_id)) is not None, (
            "get_simulation_config() by id should return the test simulation config"
        )
        # Check if data checks out
        assert(simulation_utils.get_simulation_config(simulation_config_id=simulation_config_id).user_id == user_id), (
            "get_simulation_config() should return the test simulation config"
        )
        assert(simulation_utils.get_simulation_config(simulation_config_id=simulation_config_id).simulation_type_id == simulation_type_id), (
            "get_simulation_config() should return the test simulation config"
        )
        assert(simulation_utils.get_simulation_config(simulation_config_id=simulation_config_id).vehicles[0].id == vehicle.id), (
            "get_simulation_config() should return the test simulation config"
        )
        assert(simulation_utils.get_simulation_config(simulation_config_id=simulation_config_id).environmental_conditions == environmental_conditions), (
            "get_simulation_config() should return the test simulation config"
        )
        assert(simulation_utils.get_simulation_config(simulation_config_id=simulation_config_id).initial_conditions == initial_conditions), (
            "get_simulation_config() should return the test simulation config"
        )
        assert(simulation_utils.get_simulation_config(simulation_config_id=simulation_config_id).physical_constants == physical_constants), (
            "get_simulation_config() should return the test simulation config"
        )
        assert(simulation_utils.get_simulation_config(simulation_config_id=simulation_config_id).time_settings == time_settings), (
            "get_simulation_config() should return the test simulation config"
        )
        assert(simulation_utils.get_simulation_config(simulation_config_id=simulation_config_id).traffic_rules == traffic_rules), (
            "get_simulation_config() should return the test simulation config"
        )
        assert(simulation_utils.get_simulation_config(simulation_config_id=simulation_config_id).success_definition == success_definition), (
            "get_simulation_config() should return the test simulation config"
        )

        # Check null input
        assert(simulation_utils.get_simulation_config()) is None, "get_simulation_config() with no arguments should return None"

        # Update simulation config
        new_environmental_conditions = {"new_environmental1": "new_environmental1_description", "new_environmental2": "new_environmental2_description"}
        new_initial_conditions = {"new_initial1": "new_initial1_description", "new_initial2": "new_initial2_description"}
        new_physical_constants = {"new_constant1": "new_constant1_description", "new_constant2": "new_constant2_description"}
        new_time_settings = {"new_time1": "new_time1_description", "new_time2": "new_time2_description"}
        new_traffic_rules = {"new_rule1": "new_rule1_description", "new_rule2": "new_rule2_description"}
        new_success_definition = {"new_success1": "new_success1_description", "new_success2": "new_success2_description"}
        # transform dictionaries to json
        new_environmental_conditions = json.dumps(new_environmental_conditions)
        new_initial_conditions = json.dumps(new_initial_conditions)
        new_physical_constants = json.dumps(new_physical_constants)
        new_time_settings = json.dumps(new_time_settings)
        new_traffic_rules = json.dumps(new_traffic_rules)
        new_success_definition = json.dumps(new_success_definition)

        simulation_utils.update_simulation_config(
            simulation_config_id=simulation_config_id,
            environmental_conditions=new_environmental_conditions,
            initial_conditions=new_initial_conditions,
            physical_constants=new_physical_constants,
            time_settings=new_time_settings,
            traffic_rules=new_traffic_rules,
            success_definition=new_success_definition
        )

        # Check if data checks out
        assert(simulation_utils.get_simulation_config(simulation_config_id=simulation_config_id).environmental_conditions == new_environmental_conditions), (
            "update_simulation_config() should update the environmental conditions of the simulation config"
        )
        assert(simulation_utils.get_simulation_config(simulation_config_id=simulation_config_id).initial_conditions == new_initial_conditions), (
            "update_simulation_config() should update the initial conditions of the simulation config"
        )
        assert(simulation_utils.get_simulation_config(simulation_config_id=simulation_config_id).physical_constants == new_physical_constants), (
            "update_simulation_config() should update the physical constants of the simulation config"
        )
        assert(simulation_utils.get_simulation_config(simulation_config_id=simulation_config_id).time_settings == new_time_settings), (
            "update_simulation_config() should update the time settings of the simulation config"
        )
        assert(simulation_utils.get_simulation_config(simulation_config_id=simulation_config_id).traffic_rules == new_traffic_rules), (
            "update_simulation_config() should update the traffic rules of the simulation config"
        )
        assert(simulation_utils.get_simulation_config(simulation_config_id=simulation_config_id).success_definition == new_success_definition), (
            "update_simulation_config() should update the success definition of the simulation config"
        )
        
        # Delete simulation config
        simulation_utils.delete_simulation_config(simulation_config_id=simulation_config_id)

        # Check if the simulation config is not in the database
        assert(simulation_utils.get_simulation_config(simulation_config_id=simulation_config_id)) is None, (
            "get_simulation_config() by id should not return the test simulation config after deletion"
        )

def test_simulation_result():
    with app.app_context():
        db.drop_all()
        db.create_all()
        # create simulation type
        simulation_result = create_simulation_result()
        simulation_result_id = simulation_result.id

        assert (simulation_utils.get_simulation_result(simulation_result_id=simulation_result_id)) is not None, (
            "get_simulation_result() by id should return the test simulation result"
        )
        # Check if data checks out
        assert (simulation_utils.get_simulation_result(simulation_result_id=simulation_result_id).simulation_config_id == simulation_result.simulation_config_id), (
            "get_simulation_result() should return the test simulation result"
        )
        assert (simulation_utils.get_simulation_result(simulation_result_id=simulation_result_id).success == simulation_result.success), (
            "get_simulation_result() should return the test simulation result"
        )
        assert (simulation_utils.get_simulation_result(simulation_result_id=simulation_result_id).navigation_data == simulation_result.navigation_data), (
            "get_simulation_result() should return the test simulation result"
        )
        assert (simulation_utils.get_simulation_result(simulation_result_id=simulation_result_id).safety_metrics == simulation_result.safety_metrics), (
            "get_simulation_result() should return the test simulation result"
        )
        assert (simulation_utils.get_simulation_result(simulation_result_id=simulation_result_id).vehicle_system_performance == simulation_result.vehicle_system_performance), (
            "get_simulation_result() should return the test simulation result"
        )

        # Check null input
        assert (simulation_utils.get_simulation_result()) is None, "get_simulation_result() with no arguments should return None"

        # Update simulation result
        new_navigation_data = {"new_navigation1": "new_navigation1_description", "new_navigation2": "new_navigation2_description"}
        new_safety_metrics = {"new_safety1": "new_safety1_description", "new_safety2": "new_safety2_description"}
        new_vehicle_system_performance = {"new_performance1": "new_performance1_description", "new_performance2": "new_performance2_description"}
        # transform dictionaries to json
        new_navigation_data = json.dumps(new_navigation_data)
        new_safety_metrics = json.dumps(new_safety_metrics)
        new_vehicle_system_performance = json.dumps(new_vehicle_system_performance)
        
        simulation_utils.update_simulation_result(
            simulation_result_id=simulation_result_id,
            navigation_data=new_navigation_data,
            safety_metrics=new_safety_metrics,
            vehicle_system_performance=new_vehicle_system_performance
        )

        # Check if data checks out
        assert (simulation_utils.get_simulation_result(simulation_result_id=simulation_result_id).navigation_data == new_navigation_data), (
            "update_simulation_result() should update the navigation data of the simulation result"
        )
        assert (simulation_utils.get_simulation_result(simulation_result_id=simulation_result_id).safety_metrics == new_safety_metrics), (
            "update_simulation_result() should update the safety metrics of the simulation result"
        )
        assert (simulation_utils.get_simulation_result(simulation_result_id=simulation_result_id).vehicle_system_performance == new_vehicle_system_performance), (
            "update_simulation_result() should update the vehicle system performance of the simulation result"
        )

        # Delete simulation result
        simulation_utils.delete_simulation_result(simulation_result_id=simulation_result_id)

        # Check if the simulation result is not in the database
        assert (simulation_utils.get_simulation_result(simulation_result_id=simulation_result_id)) is None, (
            "get_simulation_result() by id should not return the test simulation result after deletion"
        )
