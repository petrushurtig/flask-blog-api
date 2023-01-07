import os
import jwt
import datetime
from dotenv import load_dotenv
from functools import wraps
from flask import json, Response, request, g, jsonify
from src.db.dbmodels.user import User
from app_source import app

class Auth():

    load_dotenv()

    def encode_token(payload, exp, iat):
        try:
            if exp is not None:
                payload["exp"] = exp
            if iat is not None:
                payload["iat"] = iat
            
            jwt_secret = os.environ['JWT_SECRET_KEY']

            return jwt.encode(payload, jwt_secret, algorithm="HS256")
        except Exception as e:
            error_msg = "Exception when calling Auth.encode_token: %s\n" % e
            raise Exception(error_msg)

        
    @staticmethod
    def decode_token(token):
        re = {'data': {}, 'error': {}}
        try:
            payload = jwt.decode(token, os.environ('JWT_SECRET_KEY'))
            re['data'] = {'user_id', payload['sub']}
            return re
        except jwt.ExpiredSignatureError as e1:
            re['error'] = {'message': 'Token expired'}
            return re
        except jwt.InvalidTokenError:
            re['error'] = {'message': 'Invalid token'}
            return re

    @staticmethod
    def auth_required(func):
        @wraps(func)
        def decorated_auth(*args, **kwargs):

            if 'api-token' not in request.headers:
                msg = {"message": "Token missing"}
                return jsonify(msg), 400
            
            token = request.headers.get('api-token')
            data = Auth.decode_token(token)
            if data['error']:
                msg = {"message": "error"}
                return jsonify(msg), 400
            
            user_id = data['data']['user_id']
            check_user = User.get_user_by_id(user_id)
            if not check_user:
                msg = {"message": "user does not exist, invalid token"}
                return jsonify(msg), 400

            g.user = {'id': user_id}
            return func(*args, **kwargs)
        return decorated_auth

    @staticmethod
    def login(email, password):
        try:
            user = User.find_by_credentials(email, password)
            
            if not user:
                msg = {"message": "Wrong creds"}
                raise Exception(msg)
            
            issued_at = datetime.datetime.now(tz=datetime.timezone.utc)
            access_token_expries = issued_at + datetime.timedelta(hours=2)
            payload: dict = {
                "user_id": user.id,
                "grant_type": "ACCESS_TOKEN"
            }

            access_token = Auth.encode_token(payload=payload, exp=access_token_expries, iat=issued_at)
            refresh_token_expires = issued_at + datetime.timedelta(days=14)
            refresh_token = Auth.encode_token(payload=payload, exp=refresh_token_expires, iat=issued_at)

            return {
                "access_token": f"token|{access_token}",
                "refresh_token": f"token|{refresh_token}"
            }
        except Exception as e:
            error_msg = "Exception when calling AuthService.login: %s\n" % e
            raise Exception(error_msg)
