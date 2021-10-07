import graphene
from commons.keycloak.users import UserHandler
from graphql import ResolveInfo

from users.models.users import UnikubeUser


class DeleteAvatar(graphene.Mutation):
    class Arguments:
        id = graphene.UUID()

    ok = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info: ResolveInfo, **kwargs):
        pk = kwargs.get("id")
        if str(pk) == str(info.context.kcuser.get("uuid")):
            user = UnikubeUser.objects.get(id=pk)
            user.avatar_image.delete()
            return cls(ok=True)
        return cls(ok=False)


class UserInput(graphene.InputObjectType):
    id = graphene.UUID(required=True)
    email = graphene.String()
    name = graphene.String()
    family_name = graphene.String()
    given_name = graphene.String()


class UpdateUser(graphene.Mutation):
    class Arguments:
        user_data = UserInput(required=True)

    ok = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info: ResolveInfo, user_data=None):
        pk = user_data.id
        if str(pk) == str(info.context.kcuser.get("uuid")):
            try:
                # build update data ...
                data = {
                    "email": user_data.email,
                    "username": user_data.name,
                    "lastName": user_data.family_name,
                    "firstName": user_data.given_name,
                }
                # ... but only consider values that were actually provided
                data = {k: v for k, v in data.items() if v}

                uh = UserHandler()
                status = uh.update(pk, data)

                if status == 204:
                    return cls(ok=True)
                return cls(ok=False)
            except Exception:
                pass
        return cls(ok=False)


class Mutation(graphene.ObjectType):
    delete_avatar = DeleteAvatar.Field()
    update_user = UpdateUser.Field()
