from api.schemas import ma
from api.models.film import Film

class FilmSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Film

film_schema = FilmSchema()
films_schema = FilmSchema(many=True)
