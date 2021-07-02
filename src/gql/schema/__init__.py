from graphene_federation import build_schema

from .mutation import Mutation
from .query import Query

schema = build_schema(query=Query)
# TODO: add Mutation once implemented!
