from flask import Blueprint, jsonify, request
import simulation_utils

simulation_routes = Blueprint("simulation_routes", __name__)


# Simulation type routes
@simulation_routes.route("/simulation_types", methods=["POST"])
def create_simulation_type():
    data = request.get_json()
    name = data.get("name")
    description = data.get("description")

    if not name or not description:
        return jsonify({"error": "Invalid data"}), 400
    simulation_type = simulation_utils.create_simulation_type(name, description)
    if not simulation_type:
        return jsonify({"error": "Simulation type could not be created"}), 400

    return jsonify(simulation_type.to_dict()), 200


@simulation_routes.route("/simulation_types", methods=["GET"])
def get_simulation_type():
    simulation_type_id = request.args.get("simulation_type_id")
    simulation_type_name = request.args.get("simulation_type_name")

    simulation_type = simulation_utils.get_simulation_type(
        simulation_type_id, simulation_type_name
    )
    if not simulation_type:
        return jsonify({"error": "Simulation type could not be found"}), 404

    return jsonify(simulation_type.to_dict()), 200


@simulation_routes.route("/simulation_types/<int:simulation_type_id>", methods=["PUT"])
def update_simulation_type(simulation_type_id):
    data = request.get_json()
    name = data.get("name")
    description = data.get("description")
    simulation_utils.update_simulation_type(
        simulation_type_id, name=name, description=description
    )

    return jsonify({"success": "Simulation type updated successfully"}), 200


@simulation_routes.route(
    "/simulation_types/<int:simulation_type_id>", methods=["DELETE"]
)
def delete_simulation_type(simulation_type_id):
    if not simulation_type_id:
        return jsonify({"error": "Invalid data"}), 400

    simulation_utils.delete_simulation_type(simulation_type_id)
    if not simulation_utils.get_simulation_type(simulation_type_id):
        return jsonify({"success": "Simulation type deleted successfully"}), 200
    else:
        return jsonify({"error": "Simulation type could not be deleted"}), 500


# Vehicle routes
@simulation_routes.route("/vehicles", methods=["POST"])
def create_vehicle():
    data = request.get_json()
    name = data.get("name")
    description = data.get("description")
    sensor_information = data.get("sensor_information")
    physical_properties = data.get("physical_properties")

    if not name or not description or not sensor_information or not physical_properties:
        return jsonify({"error": "Invalid data"}), 400

    vehicle = simulation_utils.create_vehicle(
        name, description, sensor_information, physical_properties
    )
    if not vehicle:
        return jsonify({"error": "Vehicle could not be created"}), 500
    return jsonify({"success": "Vehicle created successfully"}), 200


@simulation_routes.route("/vehicles", methods=["GET"])
def get_vehicle():
    vehicle_id = request.args.get("vehicle_id")
    vehicle_name = request.args.get("vehicle_name")

    if not vehicle_id and not vehicle_name:
        return jsonify({"error": "Invalid data"}), 400

    vehicle = simulation_utils.get_vehicle(vehicle_id, vehicle_name)
    if not vehicle:
        return jsonify({"error": "Vehicle could not be found"}), 404
    return (
        jsonify(
            {"success": "Vehicle retrieved successfully", "vehicle": vehicle.to_dict()}
        ),
        200,
    )


@simulation_routes.route("/vehicles/<int:vehicle_id>", methods=["DELETE"])
def delete_vehicle(vehicle_id):
    if not vehicle_id:
        return jsonify({"error": "Invalid data"}), 400

    simulation_utils.delete_vehicle(vehicle_id)
    if not simulation_utils.get_vehicle(vehicle_id):
        return jsonify({"success": "Vehicle deleted successfully"}), 200
    else:
        return jsonify({"error": "Vehicle could not be deleted"}), 500


# Simulation config routes
@simulation_routes.route("/simulation_configs", methods=["POST"])
def create_simulation_config():
    data = request.get_json()
    user_id = data.get("user_id")
    simulation_type_id = data.get("simulation_type_id")
    vehicles = data.get("vehicles")
    environmental_conditions = data.get("environmental_conditions")
    initial_conditions = data.get("initial_conditions")
    physical_constants = data.get("physical_constants")
    time_settings = data.get("time_settings")
    traffic_rules = data.get("traffic_rules")
    success_definition = data.get("success_definition")

    if (
        not user_id
        or not simulation_type_id
        or not vehicles
        or not environmental_conditions
        or not initial_conditions
        or not physical_constants
        or not time_settings
        or not traffic_rules
        or not success_definition
    ):
        return jsonify({"error": "Invalid data"}), 400

    simulation_config = simulation_utils.create_simulation_config(
        user_id,
        simulation_type_id,
        vehicles,
        environmental_conditions,
        initial_conditions,
        physical_constants,
        time_settings,
        traffic_rules,
        success_definition,
    )
    if not simulation_config:
        return jsonify({"error": "Simulation config could not be created"}), 500
    return jsonify({"success": "Simulation config created successfully"}), 200


@simulation_routes.route("/simulation_configs", methods=["GET"])
def get_simulation_config():
    simulation_config_id = request.args.get("simulation_config_id")
    if not simulation_config_id:
        return jsonify({"error": "Invalid data"}), 400

    simulation_config = simulation_utils.get_simulation_config(simulation_config_id)
    if not simulation_config:
        return jsonify({"error": "Simulation config could not be found"}), 404
    return (
        jsonify(
            {
                "success": "Simulation config retrieved successfully",
                "simulation_config": simulation_config.to_dict(),
            }
        ),
        200,
    )


@simulation_routes.route(
    "/simulation_configs/<int:simulation_config_id>", methods=["PUT"]
)
def update_simulation_config(simulation_config_id):
    data = request.get_json()
    user_id = data.get("user_id")
    simulation_type_id = data.get("simulation_type_id")
    vehicles = data.get("vehicles")
    environmental_conditions = data.get("environmental_conditions")
    initial_conditions = data.get("initial_conditions")
    physical_constants = data.get("physical_constants")
    time_settings = data.get("time_settings")
    traffic_rules = data.get("traffic_rules")
    success_definition = data.get("success_definition")

    if not simulation_config_id:
        return jsonify({"error": "Invalid data"}), 400

    simulation_utils.update_simulation_config(
        simulation_config_id,
        user_id=user_id,
        simulation_type_id=simulation_type_id,
        vehicles=vehicles,
        environmental_conditions=environmental_conditions,
        initial_conditions=initial_conditions,
        physical_constants=physical_constants,
        time_settings=time_settings,
        traffic_rules=traffic_rules,
        succes_definition=success_definition,
    )

    return jsonify({"success": "Simulation config updated successfully"}), 200


@simulation_routes.route(
    "/simulation_configs/<int:simulation_config_id>", methods=["DELETE"]
)
def delete_simulation_config(simulation_config_id):
    if not simulation_config_id:
        return jsonify({"error": "Invalid data"}), 400

    simulation_utils.delete_simulation_config(simulation_config_id)

    return jsonify({"success": "Simulation config deleted successfully"}), 200


# Simulation result routes
@simulation_routes.route("/simulation_results", methods=["POST"])
def create_simulation_result():
    data = request.get_json()
    simulation_config_id = data.get("simulation_config_id")
    success = data.get("success")
    navigation_data = data.get("navigation_data")
    safety_metrics = data.get("safety_metrics")
    vehicle_system_performance = data.get("vehicle_system_performance")

    if not simulation_config_id:
        return jsonify({"error": "Invalid data"}), 400

    simulation_utils.create_simulation_result(
        simulation_config_id,
        success,
        navigation_data,
        safety_metrics,
        vehicle_system_performance,
    )

    return jsonify({"success": "Simulation result created successfully"}), 200


@simulation_routes.route("/simulation_results", methods=["GET"])
def get_simulation_result():
    simulation_result_id = request.args.get("simulation_result_id")

    if not simulation_result_id:
        return jsonify({"error": "Invalid data"}), 400

    simulation_result = simulation_utils.get_simulation_result(simulation_result_id)
    if not simulation_result:
        return jsonify({"error": "Simulation result could not be found"}), 404
    return (
        jsonify(
            {
                "success": "Simulation result retrieved successfully",
                "simulation_result": simulation_result.to_dict(),
            }
        ),
        200,
    )


@simulation_routes.route(
    "/simulation_results/<int:simulation_result_id>", methods=["PUT"]
)
def update_simulation_result(simulation_result_id):
    data = request.get_json()
    simulation_config_id = data.get("simulation_config_id")
    success = data.get("success")
    navigation_data = data.get("navigation_data")
    safety_metrics = data.get("safety_metrics")
    vehicle_system_performance = data.get("vehicle_system_performance")

    if not simulation_result_id:
        return jsonify({"error": "Invalid data"}), 400

    simulation_utils.update_simulation_result(
        simulation_result_id,
        simulation_config_id=simulation_config_id,
        success=success,
        navigation_data=navigation_data,
        safety_metrics=safety_metrics,
        vehicle_system_performance=vehicle_system_performance,
    )
    return jsonify({"success": "Simulation result updated successfully"}), 200


@simulation_routes.route(
    "/simulation_results/<int:simulation_result_id>", methods=["DELETE"]
)
def delete_simulation_result(simulation_result_id):
    if not simulation_result_id:
        return jsonify({"error": "Invalid data"}), 400

    simulation_utils.delete_simulation_result(simulation_result_id)

    return jsonify({"success": "Simulation result deleted successfully"}), 200
