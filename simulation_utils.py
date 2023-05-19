from simulation_models import (
    SimulationConfig,
    SimulationResult,
    SimulationType,
    Vehicle,
)
from database import db

# pylint: disable=fixme
# pylint: disable=unused-argument
# fmt: off

def is_simulation_config_data_clean(
        user_id,
        simulation_type_id,
        vehicles,
        environmental_conditions,
        initial_conditions,
        physical_constants,
        time_settings,
        traffic_rules,
        success_definition
        ):
    # TODO - implement this function
    # Check if user exists
    # Check if simulation type exists
    # Check if vehicles exist
    # Check if environmental conditions are valid
    # Check if initial conditions are valid
    # Check if physical constants are valid
    # Check if time settings are valid
    # Check if traffic rules are valid
    # Check if success definition is valid
    # Check if all data is provided
    return True, None    

def is_simulation_result_data_clean(
        simulation_config_id,
        success,
        navigation_data,
        safety_metrics,
        vehicle_system_performance
        
):
    # TODO - implement this function
    # Check if simulation config exists
    # Check if success is valid
    # Check if navigation data is valid
    # Check if safety metrics are valid
    # Check if vehicle system performance is valid
    # Check if all data is provided
    return True, None

def is_vehicle_data_clean(
    name,
    description,
    sensor_information,
    physical_properties
):
    # TODO - implement this function
    # Check if name is valid
    # Check if description is valid
    # Check if sensor information is valid
    # Check if physical properties are valid
    # Check if all data is provided
    return True, None

def create_simulation_type(
    name,
    description
):
    if not name or not description:
        print("You need to provide a name and a description.")
        return
    new_type = SimulationType(name=name, description=description)
    db.session.add(new_type)
    db.session.commit()

    print(f"simulation type {new_type.name} created successfully.")


def delete_simulation_type(simulation_type_id=None, simulation_type_name=None):
    if not simulation_type_id and not simulation_type_name:
        print("You need to provide either a simulation type id or a simulation type name.")
        return
    if simulation_type_id:
        simulation_type = SimulationType.query.filter_by(id=simulation_type_id).first()
    elif simulation_type_name:
        simulation_type = SimulationType.query.filter_by(name=simulation_type_name).first()

    simulation_type_name = simulation_type.name # Save name for printing before deleting it
    db.session.delete(simulation_type)
    db.session.commit()

    print(f"simulation type {simulation_type_name} deleted successfully.")

def create_vehicle(
    name,
    description,
    sensor_information,
    physical_properties
):
    is_clean, errors = is_vehicle_data_clean(
        name,
        description,
        sensor_information,
        physical_properties
    )
    assert is_clean, f"found errors in vehicle data: {errors}"
    
    new_vehicle = Vehicle(
        name=name,
        description=description,
        sensor_information=sensor_information,
        physical_properties=physical_properties
    )
    db.session.add(new_vehicle)
    db.session.commit()

    print(f"vehicle {new_vehicle.name} created successfully.")

def create_simulation_config(
        user_id,
        simulation_type_id,
        vehicles,
        environmental_conditions,
        initial_conditions,
        physical_constants,
        time_settings,
        traffic_rules,
        success_definition
        ):

    is_clean, errors = is_simulation_config_data_clean(
        user_id,
        simulation_type_id,
        vehicles,
        environmental_conditions,
        initial_conditions,
        physical_constants,
        time_settings,
        traffic_rules,
        success_definition
        )
    assert is_clean, f"found errors in simulation config data: {errors}"

    new_config = SimulationConfig(
        user_id=user_id,
        simulation_type_id=simulation_type_id,
        vehicles=vehicles,
        environmental_conditions=environmental_conditions,
        initial_conditions=initial_conditions,
        physical_constants=physical_constants,
        time_settings=time_settings,
        traffic_rules=traffic_rules,
        success_definition=success_definition
    )
    db.session.add(new_config)
    db.session.commit()

    print(f"simulation config {new_config.id} created successfully.")

def get_simulation_config(simulation_config_id):
    return SimulationConfig.query.filter_by(id=simulation_config_id)

def update_simulation_config(simulation_config_id, **kwargs):
    # Check if simulation config exists
    if get_simulation_config(simulation_config_id) is None:
        print(f"simulation config {simulation_config_id} does not exist.")
        return
    # TODO Check if data is valid

    # Update simulation config
    config = get_simulation_config(simulation_config_id)
    for key, value in kwargs.items():
        setattr(config, key, value)
    db.session.commit()
    print(f"simulation config {simulation_config_id} updated successfully.")


def delete_simulation_config(simulation_config_id):
    config = get_simulation_config(simulation_config_id)
    db.session.delete(config)
    db.session.commit()

def create_simulation_result(
        simulation_config_id,
        success,
        navigation_data,
        safety_metrics,
        vehicle_system_performance
        ):
    
    is_clean, errors = is_simulation_result_data_clean(
        simulation_config_id,
        success,
        navigation_data,
        safety_metrics,
        vehicle_system_performance
        )
    assert is_clean, f"found errors in simulation result data: {errors}"

    new_result = SimulationResult(
        simulation_config_id=simulation_config_id,
        success=success,
        navigation_data=navigation_data,
        safety_metrics=safety_metrics,
        vehicle_system_performance=vehicle_system_performance
    )
    db.session.add(new_result)
    db.session.commit()

    print(f"simulation result {new_result.id} created successfully.")

def get_simulation_result(simulation_result_id):
    return SimulationResult.query.filter_by(id=simulation_result_id)


def update_simulation_result(simulation_result_id, **kwargs):
    # Check if simulation result exists
    if get_simulation_result(simulation_result_id) is None:
        print(f"simulation result {simulation_result_id} does not exist.")
        return
    
    # TODO Check if data is valid

    # Update simulation result
    result = get_simulation_result(simulation_result_id)
    for key, value in kwargs.items():
        setattr(result, key, value)
    db.session.commit()
    print(f"simulation result {simulation_result_id} updated successfully.")

def delete_simulation_result(simulation_result_id):
    result = get_simulation_result(simulation_result_id)
    db.session.delete(result)
    db.session.commit()
