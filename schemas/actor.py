from api.models.actor import Actor
from api.schemas import ma

class ActorSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = Actor


actor_schema = ActorSchema()
actors_schema = ActorSchema(many=True)

