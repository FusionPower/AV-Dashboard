from graphene.test import Client
from user_models import User
from schema import schema
from extensions import db
from app import app
import tempfile
import os
from simulation_models import SimulationType, Vehicle, SimulationConfig, SimulationResult
import json

# pylint: disable=fixme,no-member


def add_test_user():
    new_user = User(username="testuser", email="testuser@email.com")
    new_user.set_password("testpassword")
    db.session.add(new_user)
    db.session.commit()

def add_test_simulation_type():
    new_simulation_type = SimulationType(name="Test Simulation", description="testdescription")
    db.session.add(new_simulation_type)
    db.session.commit()

def add_test_vehicle():
    sensor_info = json.dumps({"test": "test"})
    physical_properties = json.dumps({"test": "test"})
    new_vehicle = Vehicle(name="Test Vehicle", description="testdescription", sensor_information=sensor_info, physical_properties=physical_properties)
    db.session.add(new_vehicle)
    db.session.commit()
    return new_vehicle    

def add_test_simulation_config():
    environmental_conditions = json.dumps({"test": "test"})
    initial_conditions = json.dumps({"test": "test"})
    physical_constraints = json.dumps({"test": "test"})
    time_settings = json.dumps({"test": "test"})
    traffic_rules = json.dumps({"test": "test"})
    success_definition = json.dumps({"test": "test"})

    vehicle = add_test_vehicle()

    new_simulation_config = SimulationConfig(
        user_id=1,
        simulation_type_id=1,
        vehicles = [vehicle],
        environmental_conditions=environmental_conditions,
        initial_conditions=initial_conditions,
        physical_constants=physical_constraints,
        time_settings=time_settings,
        traffic_rules=traffic_rules,
        success_definition=success_definition
    )
    db.session.add(new_simulation_config)
    db.session.commit()

def add_test_simulation_result():
    add_test_simulation_config()
    success = json.dumps({"test": "test"})
    navigation_data = json.dumps({"test": "test"})
    safety_metrics = json.dumps({"test": "test"})
    vehicle_system_performance = json.dumps({"test": "test"})

    new_simulation_result = SimulationResult(
        simulation_config_id=1,
        success=success,
        navigation_data=navigation_data,
        safety_metrics=safety_metrics,
        vehicle_system_performance=vehicle_system_performance
    )
    db.session.add(new_simulation_result)
    db.session.commit()

def config_test():
    db_fd, app.config["DATABASE"] = tempfile.mkstemp()
    app.config["TESTING"] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + app.config["DATABASE"]
    db.create_all()
    return db_fd

def end_test(db_fd):
    db.drop_all()
    os.close(db_fd)
    os.unlink(app.config["DATABASE"])

def test_create_user():
    # Set up Flask testing environment
    app.config["TESTING"] = True
    with app.app_context():
        db_fd = config_test()
        client = Client(schema)
        executed = client.execute(
            """
        mutation {
            createUser(username: "testuser", email: "testuser@email.com", password: "testpassword") {
                ok
                user {
                    id
                    username
                    email
                }
            }
        }
        """
        )

        assert executed == {
            "data": {
                "createUser": {
                    "ok": "User Created",
                    "user": {
                        "id": "1",
                        "username": "testuser",
                        "email": "testuser@email.com",
                    },
                }
            }
        }
        end_test(db_fd)


def test_query_user():
    app.config["TESTING"] = True

    with app.app_context():
        db_fd = config_test()
        add_test_user()
        client = Client(schema)

        executed = client.execute(
            """
            query {
                user(id: "1") {
                    id
                    username
                    email
                }
            }
        """
        )
        assert executed == {
            "data": {
                "user": {
                    "id": "1",
                    "username": "testuser",
                    "email": "testuser@email.com",
                }
            }
        }
        end_test(db_fd)


def test_delete_user():
    app.config["TESTING"] = True
    with app.app_context():
        db_fd = config_test()
        client = Client(schema)

        # Test delete by username
        add_test_user()
        executed = client.execute(
            """
            mutation {
                deleteUser(username: "testuser") {
                    ok
                }
            }
            """
        )
        assert executed == {"data": {"deleteUser": {"ok": "User Deleted"}}}

        # Test delete by email
        add_test_user()
        executed = client.execute(
            """
            mutation {
                deleteUser(email: "testuser@email.com") {
                    ok
                }
            }
            """
        )
        assert executed == {"data": {"deleteUser": {"ok": "User Deleted"}}}

        # Test delete by username and email
        add_test_user()
        executed = client.execute(
            """
            mutation {
                deleteUser(username: "testuser", email: "testuser@email.com") {
                    ok
                }
            }
            """
        )
        assert executed == {"data": {"deleteUser": {"ok": "User Deleted"}}}
        end_test(db_fd)



def test_create_simulation_type():
    app.config["TESTING"] = True
    with app.app_context():
        db_fd = config_test()
        client = Client(schema)

        executed = client.execute(
            """
            mutation {
                createSimulationType(name: "Test Simulation", description: "testdescription") {
                    ok
                    simulationType {
                        id
                        name
                        description
                    }
                }
            }
            """
        )

        assert executed == {
            "data": {
                "createSimulationType": {
                "ok": "Simulation Type Created",
                "simulationType": {
                    "id": "1",
                    "name": "Test Simulation",
                    "description": "testdescription"
                }
                }
            }
        }
        end_test(db_fd)

def test_query_simulation_type():
    app.config["TESTING"] = True
    with app.app_context():
        db_fd = config_test()
        client = Client(schema)

        add_test_simulation_type()
        executed = client.execute(
            """
            query {
                simulationType(id: "1") {
                    id
                    name
                    description
                }
            }
            """
        )

        assert executed == {
            "data": {
                "simulationType": {
                    "id": "1",
                    "name": "Test Simulation",
                    "description": "testdescription"
                }
            }
        }
        end_test(db_fd)

def test_update_simulation_type():
    app.config["TESTING"] = True
    with app.app_context():
        db_fd = config_test()
        client = Client(schema)

        add_test_simulation_type()
        executed = client.execute(
            """
            mutation {
                updateSimulationType(id: "1", name: "Updated Simulation", description: "updateddescription") {
                    ok
                    simulationType {
                        id
                        name
                        description
                    }
                }
            }
            """
        )

        assert executed == {
            "data": {
                "updateSimulationType": {
                    "ok": "Simulation Type Updated",
                    "simulationType": {
                        "id": "1",
                        "name": "Updated Simulation",
                        "description": "updateddescription"
                    }
                }
            }
        }
        # Update only name
        executed = client.execute(

            """
            mutation {
                updateSimulationType(id: "1", name: "Updated Simulation2") {
                    ok
                    simulationType {
                        id
                        name
                        description
                    }
                }
            }
            """
        )

        assert executed == {
            "data": {
                "updateSimulationType": {
                    "ok": "Simulation Type Updated",
                    "simulationType": {
                        "id": "1",
                        "name": "Updated Simulation2",
                        "description": "updateddescription"
                    }
                }
            }
        }
        # Update only description
        executed = client.execute(
            """
            mutation {
                updateSimulationType(id: "1", description: "updateddescription2") {
                    ok
                    simulationType {
                        id
                        name
                        description
                    }
                }
            }
            """
        )

        assert executed == {
            "data": {
                "updateSimulationType": {
                    "ok": "Simulation Type Updated",
                    "simulationType": {
                        "id": "1",
                        "name": "Updated Simulation2",
                        "description": "updateddescription2"
                    }
                }
            }
        }
        end_test(db_fd)

def test_delete_simulation_type():
    app.config["TESTING"] = True
    with app.app_context():
        db_fd = config_test()
        client = Client(schema)

        add_test_simulation_type()
        executed = client.execute(
            """
            mutation {
                deleteSimulationType(id: "1") {
                    ok
                }
            }
            """
        )

        assert executed == {
            "data": {
                "deleteSimulationType": {
                    "ok": "Simulation Type Deleted"
                }
            }
        }
        end_test(db_fd)


def test_create_vehicle():
    app.config["TESTING"] = True
    with app.app_context():
        db_fd = config_test()
        client = Client(schema)

        sensor_info = json.dumps({"test": "test"})
        physical_properties = json.dumps({"test": "test"})

        executed = client.execute(
            """
            mutation {
                createVehicle(
                    name: "Test Vehicle",
                    description: "testdescription",
                    sensorInformation: \" """ + sensor_info.replace("\"", "\\\"") + """\",
                    physicalProperties: \" """ + physical_properties.replace("\"", "\\\"") + """\"
                ) {
                    ok
                    vehicle {
                        id
                        name
                        description
                        sensorInformation
                        physicalProperties
                    }
                }
            }
            """
        )
        assert executed == {
            "data": {
                "createVehicle": {
                    "ok": "Vehicle Created",
                    "vehicle": {
                        "id": "1",
                        "name": "Test Vehicle",
                        "description": "testdescription",
                        "sensorInformation": '\" ' + sensor_info.replace("\"", "\\\"") + '\"',
                        "physicalProperties": '\" ' + physical_properties.replace("\"", "\\\"") + '\"',
                    }
                }
            }
        }
    
        end_test(db_fd)


def test_query_vehicle():
    app.config["TESTING"] = True
    with app.app_context():
        db_fd = config_test()
        client = Client(schema)
        sensor_info = json.dumps({"test": "test"})
        physical_properties = json.dumps({"test": "test"})

        add_test_vehicle()
        executed = client.execute(
            """
            query{
                vehicle(id: "1") {
                    id
                    name
                    description
                    sensorInformation
                    physicalProperties
                }
            }
            """
        )        
        assert executed == {
            "data": {
                "vehicle": {
                    "id": "1",
                    "name": "Test Vehicle",
                    "description": "testdescription",
                    "sensorInformation": '\"' + sensor_info.replace("\"", "\\\"") + '\"',
                    "physicalProperties": '\"' + physical_properties.replace("\"", "\\\"") + '\"',
                }
            }
        }
        end_test(db_fd)

def test_delete_vehicle():
    app.config["TESTING"] = True
    with app.app_context():
        db_fd = config_test()
        client = Client(schema)
        add_test_vehicle()
        executed = client.execute(
            """
            mutation {
                deleteVehicle(id: "1") {
                    ok
                }
            }
            """
        )
        assert executed == {
            "data": {
                "deleteVehicle": {
                    "ok": "Vehicle Deleted"
                }
            }
        }
        add_test_vehicle()
        executed = client.execute(
            """
            mutation {
                deleteVehicle(name: "Test Vehicle") {
                    ok
                }
            }
            """
        )
        assert executed == {
            "data": {
                "deleteVehicle": {
                    "ok": "Vehicle Deleted"
                }
            }
        }
        end_test(db_fd)

def test_create_simulation_config():
    app.config["TESTING"] = True
    with app.app_context():
        db_fd = config_test()
        client = Client(schema)

        add_test_vehicle()
        environmental_conditions = json.dumps({"test": "test"})
        initial_conditions = json.dumps({"test": "test"})
        physical_constraints = json.dumps({"test": "test"})
        time_settings = json.dumps({"test": "test"})
        traffic_rules = json.dumps({"test": "test"})
        success_definition = json.dumps({"test": "test"})


        executed = client.execute(
            """
            mutation {
                createSimulationConfig(
                    userId: "1",
                    vehicleIds: "[1]",
                    simulationTypeId: "1",
                    environmentalConditions: \"""" + environmental_conditions.replace("\"", "\\\"") + """\",
                    initialConditions: \"""" + initial_conditions.replace("\"", "\\\"") + """\"
                    physicalConstants: \"""" + physical_constraints.replace("\"", "\\\"") + """\"
                    timeSettings: \"""" + time_settings.replace("\"", "\\\"") + """\"
                    trafficRules: \"""" + traffic_rules.replace("\"", "\\\"") + """\"
                    successDefinition: \"""" + success_definition.replace("\"", "\\\"") + """\"
                ) {
                    ok
                    simulationConfig {
                        id
                        userId
                        simulationTypeId
                        environmentalConditions
                        initialConditions
                        physicalConstants
                        timeSettings
                        trafficRules
                        successDefinition
                    }
                }
            }
            """
        )

        assert executed == {
            "data": {
                "createSimulationConfig": {
                    "ok": "Simulation Config Created",
                    "simulationConfig": {
                        "id": "1",
                        "userId": 1,
                        "simulationTypeId": 1,
                        "environmentalConditions": '\"' + environmental_conditions.replace("\"", "\\\"") + '\"',
                        "initialConditions": '\"' + initial_conditions.replace("\"", "\\\"") + '\"',
                        "physicalConstants": '\"' + physical_constraints.replace("\"", "\\\"") + '\"',
                        "timeSettings": '\"' + time_settings.replace("\"", "\\\"") + '\"',
                        "trafficRules": '\"' + traffic_rules.replace("\"", "\\\"") + '\"',
                        "successDefinition": '\"' + success_definition.replace("\"", "\\\"") + '\"',
                    }
                }
            }
        }
        end_test(db_fd)

def test_query_simulation_config():
    app.config["TESTING"] = True
    with app.app_context():
        db_db = config_test()
        client = Client(schema)

        add_test_simulation_config()

        executed = client.execute(
            """
            query {
                simulationConfig(id: "1") {
                    id
                    userId
                    simulationTypeId
                    environmentalConditions
                    initialConditions
                    physicalConstants
                    timeSettings
                    trafficRules
                    successDefinition
                }
            }
            """
        )
        assert executed == {
            "data": {
                "simulationConfig": {
                    "id": "1",
                    "userId": 1,
                    "simulationTypeId": 1,
                    "environmentalConditions": '\"' + json.dumps({"test": "test"}).replace("\"", "\\\"") + '\"',
                    "initialConditions": '\"' + json.dumps({"test": "test"}).replace("\"", "\\\"") + '\"',
                    "physicalConstants": '\"' + json.dumps({"test": "test"}).replace("\"", "\\\"") + '\"',
                    "timeSettings": '\"' + json.dumps({"test": "test"}).replace("\"", "\\\"") + '\"',
                    "trafficRules": '\"' + json.dumps({"test": "test"}).replace("\"", "\\\"") + '\"',
                    "successDefinition": '\"' + json.dumps({"test": "test"}).replace("\"", "\\\"") + '\"',
                }
            }
        }
        end_test(db_db)

def test_update_simulation_config():
    app.config["TESTING"] = True
    with app.app_context():
        db_fd = config_test()
        client = Client(schema)
        add_test_simulation_config()

        new_environmental_conditions = json.dumps({"new_test": "new_test"})
        new_initial_conditions = json.dumps({"new_test": "new_test"})
        new_physical_constraints = json.dumps({"new_test": "new_test"})
        new_time_settings = json.dumps({"new_test": "new_test"})
        new_traffic_rules = json.dumps({"new_test": "new_test"})
        new_success_definition = json.dumps({"new_test": "new_test"})

        executed = client.execute(
            """
            mutation {
                updateSimulationConfig(
                    id: "1",
                    userId: "2",
                    simulationTypeId: "2",
                    environmentalConditions: \"""" + new_environmental_conditions.replace("\"", "\\\"") + """\",
                    initialConditions: \"""" + new_initial_conditions.replace("\"", "\\\"") + """\",
                    physicalConstants: \"""" + new_physical_constraints.replace("\"", "\\\"") + """\",
                    timeSettings: \"""" + new_time_settings.replace("\"", "\\\"") + """\",
                    trafficRules: \"""" + new_traffic_rules.replace("\"", "\\\"") + """\",
                    successDefinition: \"""" + new_success_definition.replace("\"", "\\\"") + """\"
                ) {
                    ok
                    simulationConfig {
                        id
                        userId
                        simulationTypeId
                        environmentalConditions
                        initialConditions
                        physicalConstants
                        timeSettings
                        trafficRules
                        successDefinition
                    }
                }
            }
            """
        )
        assert executed == {
            "data": {
                "updateSimulationConfig": {
                    "ok": "Simulation Config Updated",
                    "simulationConfig": {
                        "id": "1",
                        "userId": 2,
                        "simulationTypeId": 2,
                        "environmentalConditions": '\"' + new_environmental_conditions.replace("\"", "\\\"") + '\"',
                        "initialConditions": '\"' + new_initial_conditions.replace("\"", "\\\"") + '\"',
                        "physicalConstants": '\"' + new_physical_constraints.replace("\"", "\\\"") + '\"',
                        "timeSettings": '\"' + new_time_settings.replace("\"", "\\\"") + '\"',
                        "trafficRules": '\"' + new_traffic_rules.replace("\"", "\\\"") + '\"',
                        "successDefinition": '\"' + new_success_definition.replace("\"", "\\\"") + '\"',
                    }
                }
            }
        }
        end_test(db_fd)
        


def test_delete_simulation_config():
    app.config["TESTING"] = True
    with app.app_context():
        db_fd = config_test()
        client = Client(schema)

        add_test_simulation_config()
        executed = client.execute(
            """
            mutation {
                deleteSimulationConfig(id: "1") {
                    ok
                }
            }
            """
        )
        assert executed == {
            "data": {
                "deleteSimulationConfig": {
                    "ok": "Simulation Config Deleted"
                }
            }
        }
        end_test(db_fd)


def test_create_simulation_result():
    app.config["TESTING"] = True
    with app.app_context():
        db_fd = config_test()
        client = Client(schema)

        add_test_simulation_config()
        success = json.dumps({"test": "test"})
        navigation_data = json.dumps({"test": "test"})
        safety_metrics = json.dumps({"test": "test"})
        vehicle_system_performance = json.dumps({"test": "test"})
        executed = client.execute(
            """
            mutation {
                createSimulationResult(
                    simulationConfigId: "1",
                    success: \"""" + success.replace("\"", "\\\"") + """\",
                    navigationData: \"""" + navigation_data.replace("\"", "\\\"") + """\",
                    safetyMetrics: \"""" + safety_metrics.replace("\"", "\\\"") + """\",
                    vehicleSystemPerformance: \"""" + vehicle_system_performance.replace("\"", "\\\"") + """\"
                ) {
                    ok
                    simulationResult {
                        id
                        simulationConfigId
                        success
                        navigationData
                        safetyMetrics
                        vehicleSystemPerformance
                    }
                }
            }
            """
        )
        assert executed == {
            "data": {
                "createSimulationResult": {
                    "ok": "Simulation Result Created",
                    "simulationResult": {
                        "id": "1",
                        "simulationConfigId": 1,
                        "success": '\"' + success.replace("\"", "\\\"") + '\"',
                        "navigationData": '\"' + navigation_data.replace("\"", "\\\"") + '\"',
                        "safetyMetrics": '\"' + safety_metrics.replace("\"", "\\\"") + '\"',
                        "vehicleSystemPerformance": '\"' + vehicle_system_performance.replace("\"", "\\\"") + '\"',
                    }
                }
            }
        }
        end_test(db_fd)

def test_query_simulation_result():
    app.config["TESTING"] = True
    with app.app_context():
        db_fd = config_test()
        client = Client(schema)

        add_test_simulation_result()
        executed = client.execute(
            """
            query {
                simulationResult(id: "1") {
                    id
                    simulationConfigId
                    success
                    navigationData
                    safetyMetrics
                    vehicleSystemPerformance
                }
            }
            """
        )

        assert executed == {
            "data": {
                "simulationResult": {
                    "id": "1",
                    "simulationConfigId": 1,
                    "success": '\"' + json.dumps({"test": "test"}).replace("\"", "\\\"") + '\"',
                    "navigationData": '\"' + json.dumps({"test": "test"}).replace("\"", "\\\"") + '\"',
                    "safetyMetrics": '\"' + json.dumps({"test": "test"}).replace("\"", "\\\"") + '\"',
                    "vehicleSystemPerformance": '\"' + json.dumps({"test": "test"}).replace("\"", "\\\"") + '\"',
                }
            }
        }

        end_test(db_fd)

def test_update_simulation_result():
    app.config["TESTING"] = True
    with app.app_context():
        db_fd = config_test()
        client = Client(schema)

        add_test_simulation_result()
        new_success = json.dumps({"new_test": "new_test"})
        new_navigation_data = json.dumps({"new_test": "new_test"})
        new_safety_metrics = json.dumps({"new_test": "new_test"})
        new_vehicle_system_performance = json.dumps({"new_test": "new_test"})
        executed = client.execute(
            """
            mutation {
                updateSimulationResult(
                    id: "1",
                    simulationConfigId: "2",
                    success: \"""" + new_success.replace("\"", "\\\"") + """\",
                    navigationData: \"""" + new_navigation_data.replace("\"", "\\\"") + """\",
                    safetyMetrics: \"""" + new_safety_metrics.replace("\"", "\\\"") + """\",
                    vehicleSystemPerformance: \"""" + new_vehicle_system_performance.replace("\"", "\\\"") + """\"
                ) {
                    ok
                    simulationResult {
                        id
                        simulationConfigId
                        success
                        navigationData
                        safetyMetrics
                        vehicleSystemPerformance
                    }
                }
            }
            """
        )
        assert executed == {
            "data": {
                "updateSimulationResult": {
                    "ok": "Simulation Result Updated",
                    "simulationResult": {
                        "id": "1",
                        "simulationConfigId": 2,
                        "success": '\"' + new_success.replace("\"", "\\\"") + '\"',
                        "navigationData": '\"' + new_navigation_data.replace("\"", "\\\"") + '\"',
                        "safetyMetrics": '\"' + new_safety_metrics.replace("\"", "\\\"") + '\"',
                        "vehicleSystemPerformance": '\"' + new_vehicle_system_performance.replace("\"", "\\\"") + '\"',
                    }
                }
            }
        }
        end_test(db_fd)

def test_delete_simulation_result():
    app.config["TESTING"] = True
    with app.app_context():
        db_fd = config_test()
        client = Client(schema)

        add_test_simulation_result()
        executed = client.execute(
            """
            mutation {
                deleteSimulationResult(id: "1") {
                    ok
                }
            }
            """
        )
        assert executed == {
            "data": {
                "deleteSimulationResult": {
                    "ok": "Simulation Result Deleted"
                }
            }
        }
        end_test(db_fd)