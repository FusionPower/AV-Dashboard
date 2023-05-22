import os
import tempfile
import pytest

from flask import json
from app import app
from extensions import db

# pylint: disable=redefined-outer-name

@pytest.fixture
def test_client():
    db_file_descriptor, app.config["DATABASE"] = tempfile.mkstemp()
    app.config["TESTING"] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + app.config["DATABASE"]

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

    os.close(db_file_descriptor)
    os.unlink(app.config["DATABASE"])


def test_simulation_type_routes(test_client):
    # Create simulation type
    response = test_client.post(
        "/simulation_types",
        data=json.dumps(
            {
                "name": "Test Simulation",
                "description": "This is a test",
            }
        ),
        content_type="application/json",
    )
    assert response.status_code == 200

    # Get simulation type
    # Assuming a simulation type with id 1 exists
    response = test_client.get("/simulation_types?simulation_type_id=1")
    assert response.status_code == 200
    response = test_client.get("/simulation_types?simulation_type_name=Test Simulation")
    assert response.status_code == 200
    response = test_client.get(
        "/simulation_types?simulation_type_id=1&simulation_type_name=Test Simulation"
    )
    assert response.status_code == 200

    # Update simulation type
    # Assuming a simulation type with id 1 exists
    response = test_client.put(
        "/simulation_types/1",
        data=json.dumps(
            {
                "name": "Updated Simulation",
                "description": "This is an updated test",
            }
        ),
        content_type="application/json",
    )

    assert response.status_code == 200

    # Delete simulation type
    # Assuming a simulation type with id 1 exists and can be deleted
    response = test_client.delete(
        "/simulation_types/1", content_type="application/json"
    )

    assert response.status_code == 200


# Vehicle routes testing
def test_vehicle_routes(test_client):
    # Create vehicle
    response = test_client.post(
        "/vehicles",
        data=json.dumps(
            {
                "name": "Test Vehicle",
                "description": "This is a test",
                "sensor_information": {"test": "test"},
                "physical_properties": {"test": "test"},
            }
        ),
        content_type="application/json",
    )
    assert response.status_code == 200

    # Get vehicle
    response = test_client.get("/vehicles?vehicle_id=1&vehicle_name=Test Vehicle")
    assert response.status_code == 200

    response = test_client.get("/vehicles?vehicle_name=Test Vehicle")
    assert response.status_code == 200

    response = test_client.get("/vehicles?vehicle_id=1")
    assert response.status_code == 200

    # Delete vehicles
    # Assuming a vehicle type with id 1 exists and can be deleted
    response = test_client.delete("/vehicles/1", content_type="application/json")

    assert response.status_code == 200


def test_simulation_configs(test_client):
    # Create simulation config

    # Create vehicle first
    test_client.post(
        "/vehicles",
        data=json.dumps(
            {
                "name": "Test Vehicle",
                "description": "This is a test",
                "sensor_information": {"test": "test"},
                "physical_properties": {"test": "test"},
            }
        ),
        content_type="application/json",
    )
    vehicle_response = test_client.get(
        "/vehicles?vehicle_id=1&vehicle_name=Test Vehicle"
    )
    vehicle_id = vehicle_response.json.get("vehicle").get("id")

    # Now create simulation config
    response = test_client.post(
        "/simulation_configs",
        data=json.dumps(
            {
                "user_id": "1",
                "simulation_type_id": "1",
                "vehicles": [vehicle_id],
                "environmental_conditions": {"test": "test"},
                "initial_conditions": {"test": "test"},
                "physical_constants": {"test": "test"},
                "time_settings": {"test": "test"},
                "traffic_rules": {"test": "test"},
                "success_definition": {"test": "test"},
            }
        ),
        content_type="application/json",
    )
    assert response.status_code == 200

    # Get simulation config
    # Assuming a simulation type with id 1 exists
    response = test_client.get("/simulation_configs?simulation_config_id=1")
    assert response.status_code == 200

    # Update simulation config
    # Assuming a simulation type with id 1 exists
    response = test_client.put(
        "/simulation_configs/1",
        data=json.dumps(
            {
                "user_id": "1",
                "simulation_type_id": "1",
                "vehicles": [vehicle_id],
                "environmental_conditions": {"new_test": "new_test"},
                "initial_conditions": {"new_test": "new_test"},
                "physical_constants": {"new_test": "new_test"},
                "time_settings": {"new_test": "new_test"},
                "traffic_rules": {"new_test": "new_test"},
                "success_definition": {"new_test": "new_test"},
            }
        ),
        content_type="application/json",
    )
    assert response.status_code == 200

    # Delete simulation config
    # Assuming a simulation type with id 1 exists and can be deleted
    response = test_client.delete(
        "/simulation_configs/1", content_type="application/json"
    )

    assert response.status_code == 200


def test_simulation_result(test_client):
    # Create simulation result
    response = test_client.post(
        "/simulation_results",
        data=json.dumps(
            {
                "simulation_config_id": "1",
                "success": {"test": "test"},
                "navigation_data": {"test": "test"},
                "safety_metrics": {"test": "test"},
                "vehicle_system_performance": {"test": "test"},
            }
        ),
        content_type="application/json",
    )
    assert response.status_code == 200

    # Get a simulation result
    response = test_client.get("/simulation_results?simulation_result_id=1")
    assert response.status_code == 200

    # Update simulation result
    response = test_client.put(
        "/simulation_results/1",
        data=json.dumps(
            {
                "simulation_config_id": "1",
                "success": {"new_test": "new_test"},
                "navigation_data": {"new_test": "new_test"},
                "safety_metrics": {"new_test": "new_test"},
                "vehicle_system_performance": {"new_test": "new_test"},
            }
        ),
        content_type="application/json",
    )
    assert response.status_code == 200

    # Delete simulation result
    # Assuming a simulation type with id 1 exists and can be deleted
    response = test_client.delete(
        "/simulation_results/1", content_type="application/json"
    )
