from flask import Blueprint, request, jsonify
from api.models import db
from api.models.film import Film
from api.schemas.film import film_schema, films_schema
from marshmallow import ValidationError

films_router = Blueprint('films', __name__, url_prefix='/films')

# GET all films
@films_router.get('/')
def get_all_films():
    films = Film.query.all()
    return films_schema.dump(films)

# GET a single film by ID
@films_router.get('/<int:film_id>')
def get_film(film_id):
    film = Film.query.get_or_404(film_id)
    return film_schema.dump(film)

# POST a new film
@films_router.post('/')
def create_film():
    film_data = request.json
    try:
        film_schema.load(film_data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    new_film = Film(**film_data)
    db.session.add(new_film)
    db.session.commit()
    return film_schema.dump(new_film), 201

# PUT (update) an existing film
@films_router.put('/<int:film_id>')
def update_film(film_id):
    film = Film.query.get_or_404(film_id)
    film_data = request.json
    try:
        film_schema.load(film_data, partial=True)
    except ValidationError as err:
        return jsonify(err.messages), 400

    for key, value in film_data.items():
        setattr(film, key, value)

    db.session.commit()
    return film_schema.dump(film)

# DELETE a film
@films_router.delete('/<int:film_id>')
def delete_film(film_id):
    film = Film.query.get_or_404(film_id)
    db.session.delete(film)
    db.session.commit()
    return jsonify({"message": "Film deleted successfully"}), 200
