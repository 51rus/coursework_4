from flask import request
from flask_restx import abort, Namespace, Resource

from implemented import user_service, auth_service

auth_ns = Namespace('auth')


@auth_ns.route('/register')
class AuthRegisterView(Resource):

    def post(self):
        data = request.json
        return user_service.create(data)


@auth_ns.route('/login')
class AuthLoginView(Resource):

    def post(self):
        data = request.json
        email = data.get('email')
        password = data.get('password')

        try:
            tokens = auth_service.generate_token(email, password)
            return tokens, 201

        except Exception as e:
            abort(401)
