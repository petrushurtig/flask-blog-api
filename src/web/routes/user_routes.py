import datetime
from flask import request, json, Response, Blueprint, jsonify
from flask_bcrypt import generate_password_hash


from app_source import app
from src.db.dbmodels.user import User
from src.shared.auth import Auth, auth_required


user_api = Blueprint('users', __name__)

#Register user

@user_api.route('/', methods=['POST'])
def create():

    try:
        user_data = request.get_json()
        
        user_exist = User.get_user_by_email(user_data["email"])

        if user_exist:
            message = {'error': 'User already exist, please give another email address'}
            return jsonify(message),400
        
        password_hash = generate_password_hash(user_data["password"]).decode("utf-8")
    
        user = User(None, user_data["name"], user_data["email"], password_hash, datetime.datetime.now(), datetime.datetime.now())
        user.save()
        
        msg = {"message": "Created user: " + str(user.password)}
        return jsonify(msg), 201
    
    except Exception as e:
        app.logger.info(e)
        app.logger.info(user_data)

        return jsonify({"message": "Server error"}), 500   

    #token = Auth.generate_token(ser_data.get('id'))

    #return custom_response({'jwt_token': token}, 201)

#Login   

@user_api.route('/login', methods=['POST'])
def login():

    try:
        data = request.get_json()

        if "password" not in data:
            msg = {"message": "Password missing"}
            return jsonify(msg, data), 400

        if "email" not in data:
            msg = {"message": "Username missing"}
            return jsonify(msg, data), 400

        email = data["email"]
        password = data["password"]

        try:
            user_tokens = Auth.login(email, password)
        except Exception as e:
            app.logger.info(e)
            msg = {"message": "Invalid credentials"}
            return jsonify(msg), 401
  
        return jsonify(user_tokens), 200
    except Exception as e:
        app.logger.info(e)

        return jsonify({"message": "Server error"}), 500

#Get users

@user_api.route('/', methods=['GET'])
@auth_required()
def get_all_users(user: User):
    
    try:
        users = User.get_all_users()
        users_list = []

        for user in users:
            users_list.append(user)
        
        return jsonify(users), 200
    except Exception as e:
        app.logger.info(e)

        return jsonify({"message": "Server error"}), 500

@user_api.route('/<user_id>', methods=['GET'])
@auth_required()
def get_user_by_id(user: User, user_id: str):
    
    try:
        user = User.get_user_by_id(user_id)
        
        if not user:
            return jsonify({"message": "user not found"})
        
        return jsonify(user.json()), 200
    except Exception as e:
        app.logger.info(e)

        return jsonify({"message": "Server error"}), 500

@user_api.route('/me', methods=['GET'])
@auth_required()
def get_user_details(user: User):

    auth_header = "Authorization"

    if auth_header not in request.headers:
        return jsonify({"message": "Token missing"}), 401

    token = request.headers[auth_header]

    try:
        user = Auth.get_user_by_token(token)

        if not user:
            return jsonify("Token invalid")

        return jsonify(user.json())
    except Exception as e:
        app.logger.info(e)
        return jsonify({"message": "Unauthorized"}), 401


