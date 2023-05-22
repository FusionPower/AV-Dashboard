from graphene import ObjectType, Field, String, Schema, Mutation
from graphene_sqlalchemy import SQLAlchemyObjectType
from extensions import db
from user_models import User

# pylint: disable=no-member,unused-argument,no-self-argument,


class UserType(SQLAlchemyObjectType):
    class Meta:
        model = User


class Query(ObjectType):
    user = Field(UserType, id=String(), username=String())

    def resolve_user(parent, info, **args):
        username = args.get("username")
        user_id = args.get("id")

        if username is not None:
            return db.session.query(User).filter_by(username=username).first()

        if user_id is not None:
            return db.session.query(User).filter_by(id=user_id).first()

        return None


class CreateUser(Mutation):
    class Arguments:
        username = String(required=True)
        email = String(required=True)
        password = String(required=True)

    ok = Field(String)
    user = Field(lambda: UserType)

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


class AppMutation(ObjectType):
    create_user = CreateUser.Field()
    delete_user = DeleteUser.Field()


schema = Schema(query=Query, mutation=AppMutation)
