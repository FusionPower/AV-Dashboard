from graphene import ObjectType, Field, String, Schema, Mutation
from graphene_sqlalchemy import SQLAlchemyObjectType
from extensions import db
from user_models import User
from simulation_models import SimulationType, SimulationConfig, SimulationResult, Vehicle

# pylint: disable=no-member,unused-argument,no-self-argument,


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
    user = Field(GQLUser, id=String(), username=String())
    simulation_type = Field(GQLSimulationType, id=String(), name=String())

    def resolve_user(parent, info, **args):
        username = args.get("username")
        user_id = args.get("id")

        if username is not None:
            return db.session.query(User).filter_by(username=username).first()

        if user_id is not None:
            return db.session.query(User).filter_by(id=user_id).first()

        return None
    
    def resolve_simulation_type(parent, info, **args):
        name = args.get("name")
        simulation_type_id = args.get("id")

        if name is not None:
            return db.session.query(SimulationType).filter_by(name=name).first()

        if id is not None:
            return db.session.query(SimulationType).filter_by(id=simulation_type_id).first()

        return None


class CreateUser(Mutation):
    class Arguments:
        username = String(required=True)
        email = String(required=True)
        password = String(required=True)

    ok = Field(String)
    user = Field(lambda: GQLUser)

    def mutate(root, info, username, email, password):
        new_user = User(username=username, email=email)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        ok = "User Created"
        return CreateUser(user=new_user, ok=ok)


class DeleteUser(Mutation):
    class Arguments:
        username = String()
        email = String()

    ok = Field(String)

    def mutate(root, info, username=None, email=None):
        if not username and not email:
            raise ValueError("Must provide either username or id")

        user = None
        if username:
            user = db.session.query(User).filter_by(username=username).first()
        elif email:
            user = db.session.query(User).filter_by(email=email).first()

        if user:
            db.session.delete(user)
            db.session.commit()
            ok = "User Deleted"
        else:
            ok = "User Not Found"
        return DeleteUser(ok=ok)

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
        name = String(required=True)
        description = String(required=True)

    ok = Field(String)
    simulation_type = Field(lambda: GQLSimulationType)

    def mutate(root, info, name, description):
        simulation_type = db.session.query(SimulationType).filter_by(name=name).first()

        if simulation_type:
            simulation_type.description = description
            db.session.commit()
            ok = "Simulation Type Updated"
        else:
            ok = "Simulation Type Not Found"
        return UpdateSimulationType(simulation_type=simulation_type, ok=ok)
    

class DeleteSimulationType(Mutation):
    class Arguments:
        name = String()

    ok = Field(String)

    def mutate(root, info, name=None):
        if not name:
            raise ValueError("Must provide name")

        simulation_type = db.session.query(SimulationType).filter_by(name=name).first()

        if simulation_type:
            db.session.delete(simulation_type)
            db.session.commit()
            ok = "Simulation Type Deleted"
        else:
            ok = "Simulation Type Not Found"
        return DeleteSimulationType(ok=ok)





class AppMutation(ObjectType):
    create_user = CreateUser.Field()
    delete_user = DeleteUser.Field()
    create_simulation_type = CreateSimulationType.Field()


schema = Schema(query=Query, mutation=AppMutation)
