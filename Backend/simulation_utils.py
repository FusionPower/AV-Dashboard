from simulation_models import (
    SimulationConfig,
    SimulationResult,
    SimulationType,
    Vehicle,
)
from extensions import db

# pylint: disable=fixme,unused-argument,no-member
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


def get_all_simulation_types():
    # Query all users
    return SimulationType.query.all()


# Simulation type utils
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
    return new_type

def get_simulation_type(simulation_type_id=None, simulation_type_name=None):
    if not simulation_type_id and not simulation_type_name:
        print("You need to provide either a simulation type id or a simulation type name.")
        return
    if simulation_type_id and simulation_type_name:
        simulation_type = SimulationType.query.filter_by(id=simulation_type_id).first()
        if simulation_type != SimulationType.query.filter_by(name=simulation_type_name).first():
            print(f"simulation type {simulation_type_id} with name {simulation_type_name} does not exist.")
            return
        return simulation_type
    if simulation_type_id:
        return SimulationType.query.filter_by(id=simulation_type_id).first()
    elif simulation_type_name:
        return SimulationType.query.filter_by(name=simulation_type_name).first()

def update_simulation_type(simulation_type_id=None, simulation_type_name=None, **kwargs):
    if not simulation_type_id and not simulation_type_name:
        print("You need to provide either a simulation type id or a simulation type name.")
        return
    
    simulation_type = get_simulation_type(simulation_type_id, simulation_type_name)

    if not simulation_type:
        print(f"simulation type {simulation_type_id} does not exist.")
        return
    
    for key, value in kwargs.items():
        setattr(simulation_type, key, value)
    db.session.commit()

    print(f"simulation type {simulation_type.name} updated successfully")
    

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


# Vehicle utils

def get_all_vehicles():
    return Vehicle.query.all()

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
    return new_vehicle

def get_vehicle(vehicle_id=None, vehicle_name=None):
    if not vehicle_id and not vehicle_name:
        print("You need to provide either a vehicle id or a vehicle name.")
        return
    if vehicle_id and vehicle_name:
        vehicle = Vehicle.query.filter_by(id=vehicle_id).first()
        if vehicle == Vehicle.query.filter_by(name=vehicle_name).first():
            return vehicle
        print(f"vehicle {vehicle_id} with name {vehicle_name} does not exist.")
        return
    if vehicle_id:
        return Vehicle.query.filter_by(id=vehicle_id).first()
    elif vehicle_name:
        return Vehicle.query.filter_by(name=vehicle_name).first()

def delete_vehicle(vehicle_id):
    vehicle = get_vehicle(vehicle_id)
    db.session.delete(vehicle)
    db.session.commit()


# Simulation config utils

def get_vehicles_from_ids(vehicle_ids):
    vehicles = []
    for vehicle_id in vehicle_ids:
        vehicle = get_vehicle(vehicle_id)
        if not vehicle:
            print(f"vehicle {vehicle_id} does not exist.")
            return
        vehicles.append(vehicle)
    return vehicles

def create_simulation_config(
        user_id,
        simulation_type_id,
        vehicle_ids,
        environmental_conditions,
        initial_conditions,
        physical_constants,
        time_settings,
        traffic_rules,
        success_definition
        ):

    # Get vehicles
    vehicles = get_vehicles_from_ids(vehicle_ids)
    
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
    return new_config


def get_all_simulation_configs():
    return SimulationConfig.query.all()

def get_simulation_config(simulation_config_id=None):
    return SimulationConfig.query.filter_by(id=simulation_config_id).first()

def update_simulation_config(simulation_config_id, **kwargs):
    # Check if simulation config exists
    if get_simulation_config(simulation_config_id) is None:
        print(f"simulation config {simulation_config_id} does not exist.")
        return
    # TODO Check if data is valid

    # Update simulation config
    config = get_simulation_config(simulation_config_id)
    for key, value in kwargs.items():
        if key=="vehicles":
            value = get_vehicles_from_ids(value)
        setattr(config, key, value)
    db.session.commit()
    print(f"simulation config {simulation_config_id} updated successfully.")


def delete_simulation_config(simulation_config_id):
    config = get_simulation_config(simulation_config_id)
    db.session.delete(config)
    db.session.commit()


# Simulation result utils

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
    return new_result

def get_simulation_result(simulation_result_id=None):
    return SimulationResult.query.filter_by(id=simulation_result_id).first()

def get_all_simulation_results():
    return SimulationResult.query.all()

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
