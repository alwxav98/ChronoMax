from flask_restful import Resource, reqparse
from werkzeug.security import generate_password_hash, check_password_hash
from models.user_model import UserModel
import jwt
import datetime
from flask import current_app

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str, required=True, help="Email is required.")
    parser.add_argument('password', type=str, required=True, help="Password is required.")

    def post(self):
        data = UserRegister.parser.parse_args()
        if UserModel.find_by_email(data['email']):
            return {"message": "User already exists."}, 400

        hashed_password = generate_password_hash(data['password'], method='sha256')
        new_user = UserModel(email=data['email'], password_hash=hashed_password)
        new_user.save_to_db()

        return {"message": "User created successfully."}, 201


class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str, required=True, help="Email is required.")
    parser.add_argument('password', type=str, required=True, help="Password is required.")

    def post(self):
        data = UserLogin.parser.parse_args()
        user = UserModel.find_by_email(data['email'])

        if user and check_password_hash(user.password_hash, data['password']):
            token = jwt.encode(
                {'id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)},
                current_app.config['SECRET_KEY'],
                algorithm='HS256'
            )
            return {'token': token}, 200

        return {"message": "Invalid credentials."}, 401