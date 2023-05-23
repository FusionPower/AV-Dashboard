from graphene import ObjectType, Field, String, Schema, Mutation
from graphene_sqlalchemy import SQLAlchemyObjectType
import json
from extensions import db
from user_models import User
from simulation_models import (
    SimulationType,
    SimulationConfig,
    SimulationResult,
    Vehicle,
)
import user_utils

# pylint: disable=no-member,unused-argument,no-self-argument,redefined-builtin


class GQLUser(SQLAlchemyObjectType):
    class Meta:
        model = User


class GQLSimulationType(SQLAlchemyObjectType):
    class Meta:
        model = SimulationType


class GQLSimulationConfig(SQLAlchemyObjectType):
    class Meta:
        model = SimulationConfig


class GQLSimulationResult(SQLAlchemyObjectType):
    class Meta:
        model = SimulationResult


class GQLVehicle(SQLAlchemyObjectType):
    class Meta:
        model = Vehicle


class Query(ObjectType):
    user = Field(GQLUser, email=String(), username=String())
    simulation_type = Field(GQLSimulationType, id=String(), name=String())
    vehicle = Field(GQLVehicle, id=String(), name=String())
    simulation_config = Field(GQLSimulationConfig, id=String())
    simulation_result = Field(GQLSimulationResult, id=String())

    def resolve_user(parent, info, **args):
        username = args.get("username")
        email = args.get("email")
        username = user_utils.find_user(username=username, email=email)
        return username

    def resolve_simulation_type(parent, info, **args):
        name = args.get("name")
        simulation_type_id = args.get("id")

        if name is not None:
            return db.session.query(SimulationType).filter_by(name=name).first()

        if simulation_type_id is not None:
            return (
                db.session.query(SimulationType)
                .filter_by(id=simulation_type_id)
                .first()
            )

        return None

    def resolve_vehicle(parent, info, **args):
        name = args.get("name")
        vehicle_id = args.get("id")

        if name is not None:
            return db.session.query(Vehicle).filter_by(name=name).first()
        if vehicle_id is not None:
            return db.session.query(Vehicle).filter_by(id=vehicle_id).first()
        return None

    def resolve_simulation_config(parent, info, **args):
        simulation_config_id = args.get("id")
        if simulation_config_id is not None:
            return (
                db.session.query(SimulationConfig)
                .filter_by(id=simulation_config_id)
                .first()
            )
        return None

    def resolve_simulation_result(parent, info, **args):
        simulation_result_id = args.get("id")
        if simulation_result_id is not None:
            return (
                db.session.query(SimulationResult)
                .filter_by(id=simulation_result_id)
                .first()
            )
        return None


# User Mutations
class CreateUser(Mutation):
    class Arguments:
        username = String(required=True)
        email = String(required=True)
        password = String(required=True)

    ok = Field(String)
    user = Field(lambda: GQLUser)

    def mutate(root, info, username, email, password):
        new_user, ok = user_utils.create_user(username, email, password)
        return CreateUser(user=new_user, ok=ok)


class DeleteUser(Mutation):
    class Arguments:
        username = String()
        email = String()

    ok = Field(String)

    def mutate(root, info, username=None, email=None):
        ok = user_utils.delete_user(username=username, email=email)
        return DeleteUser(ok=ok)


class Login(Mutation):
    class Arguments:
        username = String(required=True)
        password = String(required=True)

    ok = Field(String)
    user = Field(lambda: GQLUser)

    def mutate(root, info, username, password):
        user = user_utils.login(username, password)
        if user:
            ok = "Login Successful"
        else:
            ok = "Login Failed"
        return Login(user=user, ok=ok)


# Simulation Type Mutations
class CreateSimulationType(Mutation):
    class Arguments:
        name = String(required=True)
        description = String(required=True)

    ok = Field(String)
    simulation_type = Field(lambda: GQLSimulationType)

    def mutate(root, info, name, description):
        new_simulation_type = SimulationType(name=name, description=description)

        db.session.add(new_simulation_type)
        db.session.commit()

        ok = "Simulation Type Created"
        return CreateSimulationType(simulation_type=new_simulation_type, ok=ok)


class UpdateSimulationType(Mutation):
    class Arguments:
        id = String(required=True)
        name = String()
        description = String()

    ok = Field(String)
    simulation_type = Field(lambda: GQLSimulationType)

    def mutate(root, info, id, name=None, description=None):
        simulation_type = db.session.query(SimulationType).filter_by(id=id).first()
        if simulation_type:
            simulation_type.name = name if name else simulation_type.name
            simulation_type.description = (
                description if description else simulation_type.description
            )
            db.session.commit()
            ok = "Simulation Type Updated"
        else:
            ok = "Simulation Type Not Found"
        return UpdateSimulationType(simulation_type=simulation_type, ok=ok)


class DeleteSimulationType(Mutation):
    class Arguments:
        id = String()
        name = String()

    ok = Field(String)

    def mutate(root, info, name=None, id=None):
        if not name and not id:
            raise ValueError("Must provide name")
        if id:
            simulation_type = db.session.query(SimulationType).filter_by(id=id).first()
        elif name:
            simulation_type = (
                db.session.query(SimulationType).filter_by(name=name).first()
            )

        if simulation_type:
            db.session.delete(simulation_type)
            db.session.commit()
            ok = "Simulation Type Deleted"
        else:
            ok = "Simulation Type Not Found"
        return DeleteSimulationType(ok=ok)


# Vehicle Mutations
class CreateVehicle(Mutation):
    class Arguments:
        name = String(required=True)
        description = String(required=True)
        sensorInformation = String(required=True)
        physicalProperties = String(required=True)

    ok = Field(String)
    vehicle = Field(lambda: GQLVehicle)

    def mutate(root, info, name, description, sensorInformation, physicalProperties):
        new_vehicle = Vehicle(
            name=name,
            description=description,
            sensor_information=sensorInformation,
            physical_properties=physicalProperties,
        )

        db.session.add(new_vehicle)
        db.session.commit()

        ok = "Vehicle Created"
        return CreateVehicle(vehicle=new_vehicle, ok=ok)


class DeleteVehicle(Mutation):
    class Arguments:
        id = String()
        name = String()

    ok = Field(String)

    def mutate(root, info, name=None, id=None):
        if not name and not id:
            raise ValueError("Must provide name")
        if id:
            vehicle = db.session.query(Vehicle).filter_by(id=id).first()
        elif name:
            vehicle = db.session.query(Vehicle).filter_by(name=name).first()
        if vehicle:
            db.session.delete(vehicle)
            db.session.commit()
            ok = "Vehicle Deleted"
        else:
            ok = "Vehicle Not Found"
        return DeleteVehicle(ok=ok)


# Simulation Config Mutations
class CreateSimulationConfig(Mutation):
    class Arguments:
        userId = String(required=True)
        simulationTypeId = String(required=True)
        vehicleIds = String(required=True)
        environmentalConditions = String(required=True)
        initialConditions = String(required=True)
        physicalConstants = String(required=True)
        timeSettings = String(required=True)
        trafficRules = String(required=True)
        successDefinition = String(required=True)

    ok = Field(String)
    simulation_config = Field(lambda: GQLSimulationConfig)

    def mutate(
        root,
        info,
        userId,
        simulationTypeId,
        vehicleIds,
        environmentalConditions,
        initialConditions,
        physicalConstants,
        timeSettings,
        trafficRules,
        successDefinition,
    ):
        vehicles = []
        for vehicleId in json.loads(vehicleIds):
            print(type(vehicleId))
            vehicle = db.session.query(Vehicle).filter_by(id=vehicleId).first()
            if vehicle:
                vehicles.append(vehicle)
            else:
                raise ValueError("Vehicle not found")

        new_simulation_config = SimulationConfig(
            user_id=userId,
            simulation_type_id=simulationTypeId,
            vehicles=vehicles,
            environmental_conditions=environmentalConditions,
            initial_conditions=initialConditions,
            physical_constants=physicalConstants,
            time_settings=timeSettings,
            traffic_rules=trafficRules,
            success_definition=successDefinition,
        )

        db.session.add(new_simulation_config)
        db.session.commit()

        ok = "Simulation Config Created"
        return CreateSimulationConfig(simulation_config=new_simulation_config, ok=ok)


class UpdateSimulationConfig(Mutation):
    class Arguments:
        id = String(required=True)
        userId = String()
        simulationTypeId = String()
        vehicleIds = String()
        environmentalConditions = String()
        initialConditions = String()
        physicalConstants = String()
        timeSettings = String()
        trafficRules = String()
        successDefinition = String()

    ok = Field(String)
    simulation_config = Field(lambda: GQLSimulationConfig)

    def mutate(
        root,
        info,
        id,
        userId=None,
        simulationTypeId=None,
        vehicleIds=None,
        environmentalConditions=None,
        initialConditions=None,
        physicalConstants=None,
        timeSettings=None,
        trafficRules=None,
        successDefinition=None,
    ):
        vehicles = []
        if vehicleIds:
            for vehicleId in json.loads(vehicleIds):
                vehicle = db.session.query(Vehicle).filter_by(id=vehicleId).first()
                if vehicle:
                    vehicles.append(vehicle)
                else:
                    raise ValueError("Vehicle not found")
        simulation_config = db.session.query(SimulationConfig).filter_by(id=id).first()
        if simulation_config:
            simulation_config.user_id = userId if userId else simulation_config.user_id
            simulation_config.simulation_type_id = (
                simulationTypeId
                if simulationTypeId
                else simulation_config.simulation_type_id
            )
            simulation_config.vehicles = (
                vehicles if vehicles else simulation_config.vehicles
            )
            simulation_config.environmental_conditions = (
                environmentalConditions
                if environmentalConditions
                else simulation_config.environmental_conditions
            )
            simulation_config.initial_conditions = (
                initialConditions
                if initialConditions
                else simulation_config.initial_conditions
            )
            simulation_config.physical_constants = (
                physicalConstants
                if physicalConstants
                else simulation_config.physical_constants
            )
            simulation_config.time_settings = (
                timeSettings if timeSettings else simulation_config.time_settings
            )
            simulation_config.traffic_rules = (
                trafficRules if trafficRules else simulation_config.traffic_rules
            )
            simulation_config.success_definition = (
                successDefinition
                if successDefinition
                else simulation_config.success_definition
            )
            db.session.commit()
            ok = "Simulation Config Updated"
        else:
            ok = "Simulation Config Not Found"
        return UpdateSimulationConfig(simulation_config=simulation_config, ok=ok)


class DeleteSimulationConfig(Mutation):
    class Arguments:
        id = String()

    ok = Field(String)

    def mutate(root, info, id):
        simulation_config = db.session.query(SimulationConfig).filter_by(id=id).first()
        if simulation_config:
            db.session.delete(simulation_config)
            db.session.commit()
            ok = "Simulation Config Deleted"
        else:
            ok = "Simulation Config Not Found"
        return DeleteSimulationConfig(ok=ok)


# Simulation Result Mutations
class CreateSimulationResult(Mutation):
    class Arguments:
        simulationConfigId = String(required=True)
        success = String(required=True)
        navigationData = String(required=True)
        safetyMetrics = String(required=True)
        vehicleSystemPerformance = String(required=True)

    ok = Field(String)
    simulation_result = Field(lambda: GQLSimulationResult)

    def mutate(
        root,
        info,
        simulationConfigId,
        success,
        navigationData,
        safetyMetrics,
        vehicleSystemPerformance,
    ):
        new_simulation_result = SimulationResult(
            simulation_config_id=simulationConfigId,
            success=success,
            navigation_data=navigationData,
            safety_metrics=safetyMetrics,
            vehicle_system_performance=vehicleSystemPerformance,
        )

        db.session.add(new_simulation_result)
        db.session.commit()

        ok = "Simulation Result Created"
        return CreateSimulationResult(simulation_result=new_simulation_result, ok=ok)


class UpdateSimulationResult(Mutation):
    class Arguments:
        id = String(required=True)
        simulationConfigId = String()
        success = String()
        navigationData = String()
        safetyMetrics = String()
        vehicleSystemPerformance = String()

    ok = Field(String)
    simulation_result = Field(lambda: GQLSimulationResult)

    def mutate(
        root,
        info,
        id,
        simulationConfigId=None,
        success=None,
        navigationData=None,
        safetyMetrics=None,
        vehicleSystemPerformance=None,
    ):
        simulation_result = db.session.query(SimulationResult).filter_by(id=id).first()
        if simulation_result:
            simulation_result.simulation_config_id = (
                simulationConfigId
                if simulationConfigId
                else simulation_result.simulation_config_id
            )
            simulation_result.success = (
                success if success else simulation_result.success
            )
            simulation_result.navigation_data = (
                navigationData if navigationData else simulation_result.navigation_data
            )
            simulation_result.safety_metrics = (
                safetyMetrics if safetyMetrics else simulation_result.safety_metrics
            )
            simulation_result.vehicle_system_performance = (
                vehicleSystemPerformance
                if vehicleSystemPerformance
                else simulation_result.vehicle_system_performance
            )
            db.session.commit()
            ok = "Simulation Result Updated"
        else:
            ok = "Simulation Result Not Found"
        return UpdateSimulationResult(simulation_result=simulation_result, ok=ok)


class DeleteSimulationResult(Mutation):
    class Arguments:
        id = String()

    ok = Field(String)

    def mutate(root, info, id):
        simulation_result = db.session.query(SimulationResult).filter_by(id=id).first()
        if simulation_result:
            db.session.delete(simulation_result)
            db.session.commit()
            ok = "Simulation Result Deleted"
        else:
            ok = "Simulation Result Not Found"
        return DeleteSimulationResult(ok=ok)


# App Mutations
class AppMutation(ObjectType):
    create_user = CreateUser.Field()
    delete_user = DeleteUser.Field()
    login = Login.Field()
    create_simulation_type = CreateSimulationType.Field()
    update_simulation_type = UpdateSimulationType.Field()
    delete_simulation_type = DeleteSimulationType.Field()
    create_vehicle = CreateVehicle.Field()
    delete_vehicle = DeleteVehicle.Field()
    create_simulation_config = CreateSimulationConfig.Field()
    delete_simulation_config = DeleteSimulationConfig.Field()
    update_simulation_config = UpdateSimulationConfig.Field()
    create_simulation_result = CreateSimulationResult.Field()
    update_simulation_result = UpdateSimulationResult.Field()
    delete_simulation_result = DeleteSimulationResult.Field()


schema = Schema(query=Query, mutation=AppMutation)
