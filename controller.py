from flask import jsonify, request, Blueprint
from flask_jwt_extended import create_access_token, jwt_required, set_access_cookies, unset_jwt_cookies, create_refresh_token, set_refresh_cookies
from datetime import datetime

class Controller():

    login_controller = Blueprint('login', __name__)

    @login_controller.route('/login', methods=['POST'])
    def login():
        login = request.json['login']
        password = request.json['password']

        if login == 'admin' and password == 'admin':
            token = create_access_token(identity=login)
            refresh_token = create_refresh_token(identity=login)
            response = jsonify({'message': token})
            set_access_cookies(response, token)
            set_refresh_cookies(response, token)
        else:
            response = jsonify({'message': 'Invalid username or password'})
            response.status_code = 401

        return response

    @login_controller.route('/logout', methods=['GET'])
    @jwt_required()
    def logout():
        response = jsonify({'message': 'Logged out'})
        unset_jwt_cookies(response)
        return response

    @login_controller.route('/protected', methods=['GET'])
    @jwt_required()
    def protected():
        return jsonify({'message': datetime.now()})