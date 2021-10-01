import graphene
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


class Mutation(graphene.ObjectType):
    delete_avatar = DeleteAvatar.Field()

