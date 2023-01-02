from flask import jsonify, request
from flask.views import MethodView
from sqlalchemy.exc import IntegrityError
from models import UserModel, AdvertModel, Session
from errors import ApiError
from validation import register_schema, advert_schema, validate_data


def register():
    user = validate_data(request.json, register_schema)
    with Session() as session:
        new_user = UserModel(**user)
        session.add(new_user)
        try:
            session.commit()
        except IntegrityError:
            raise ApiError(400, "Email уже существует")
        return jsonify({
            "user_id": new_user.user_id,
            "email": new_user.email,
            "password": new_user.password
        })


class AdvertView(MethodView):

    def get(self, id: int):
        with Session() as session:
            advert = session.query(AdvertModel).get(id)
            if advert is None:
                raise ApiError(404, "Пользователь не найден")
            return jsonify({
                "id": advert.advert_id,
                "title": advert.title,
                "description": advert.description,
                "created_time": advert.created_time,
                "author": advert.author
            })

    def post(self):
        advert_data = validate_data(request.json, advert_schema)
        with Session() as session:
            advert = AdvertModel(**advert_data)
            session.add(advert)
            session.commit()
            return jsonify({
                "id": advert.advert_id,
                "title": advert.title,
                "description": advert.description,
                "created_time": advert.created_time,
                "author": advert.author
            })

    def delete(self, id: int):
        with Session() as session:
            advert = session.query(AdvertModel).get(id)
            if advert is None:
                raise ApiError(404, "Пользователь не найден")
            else:
                session.delete(advert)
                session.commit()
                return jsonify({"Статус": "Удален"})

    def patch(self, id: int):
        advert_data = validate_data(request.json, advert_schema)
        with Session() as session:
            advert = session.query(AdvertModel).get(id)
            for field, val in advert_data.items():
                setattr(advert, field, val)
            session.add(advert)
            session.commit()
            return jsonify({
                "id": advert.advert_id,
                "title": advert.title,
                "description": advert.description,
                "created_time": advert.created_time,
                "author": advert.author
                })


