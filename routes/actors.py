from flask import Blueprint, request, jsonify
from marshmallow import ValidationError


from api.models import db
from api.models.actor import Actor
from api.schemas.actor import actor_schema, actors_schema


actors_router = Blueprint('actors', __name__, url_prefix='/actors')

@actors_router.get('/')
def read_all_actors():
    actors = Actor.query.all()
    return actors_schema.dump(actors)


@actors_router.get('/<actor_id>')
def read_actor(actor_id):
    actor = Actor.query.get(actor_id)
    return actor_schema.dump(actor)


@actors_router.post('/')
def create_actor():
    actor_data = request.json

    try:
        actor_schema.load(actor_data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    actor = Actor(**actor_data)
    db.session.add(actor)
    db.session.commit()

    return actor_schema.dump(actor)

@actors_router.put('/<actor_id>')
def update_actor(actor_id):
    actor_data = request.json
    actor = Actor.query.get_or_404(actor_id)

    try:
        actor_schema.load(actor_data, partial=True)
    except ValidationError as err:
        return jsonify(err.messages), 400

    for key, value in actor_data.items():
        setattr(actor, key, value)

    db.session.commit()
    return actor_schema.dump(actor), 200

@actors_router.delete('/<actor_id>')
def delete_actor(actor_id):
    actor = Actor.query.get_or_404(actor_id)

    db.session.delete(actor)
    db.session.commit()
    return jsonify({"message": "Actor successfully deleted"}), 200
