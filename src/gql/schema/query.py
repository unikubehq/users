import graphene
from commons.keycloak.users import UserHandler
from graphene_federation import key

from users.models import UnikubeUser


@key(fields="id")
class UserNode(graphene.ObjectType):
    id = graphene.UUID(required=True)
    email = graphene.String()
    name = graphene.String()
    family_name = graphene.String()
    given_name = graphene.String()
    avatar_image = graphene.String()

    def __resolve_reference(self, info, **kwargs):
        uh = UserHandler()
        kc_user = uh.get(self.id)
        user, _ = UnikubeUser.objects.get_or_create(id=self.id)
        return UserNode(
            id=self.id,
            email=kc_user["email"],
            name=kc_user["username"],
            family_name=kc_user["lastName"],
            given_name=kc_user["firstName"],
            avatar_image=user.avatar_image.url if user.avatar_image else None,
        )


class Query(graphene.ObjectType):
    user = graphene.Field(UserNode, id=graphene.UUID(required=False))

    def resolve_user(self, info, id=None):
        if id is None or info.context.kcuser["uuid"] == str(id):
            # this might be the first request and the user may be unknown to the db
            # we accept the token (which comes from the keycloak) as a valid source of truth and create the user
            # in the db
            user, _ = UnikubeUser.objects.get_or_create(id=info.context.kcuser["uuid"])
            # the requesting user fetches itself
            return UserNode(
                id=info.context.kcuser["uuid"],
                email=info.context.kcuser["email"],
                name=info.context.kcuser["name"],
                family_name=info.context.kcuser["family_name"],
                given_name=info.context.kcuser["given_name"],
                avatar_image=user.avatar_image.url if user.avatar_image else None,
            )
        # first, check if this user exists in keycloak
        uh = UserHandler()
        # this should raise a 404 is user does not exist
        kc_user = uh.get(id)
        # second, resolve user from this service
        user, _ = UnikubeUser.objects.get_or_create(id=id)
        return UserNode(
            id=id,
            email=kc_user["email"],
            name=kc_user["username"],
            family_name=kc_user["lastName"],
            given_name=kc_user["firstName"],
            avatar_image=user.avatar_image.url if user.avatar_image else None,
        )
