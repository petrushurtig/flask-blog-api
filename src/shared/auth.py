import os
import jwt
import datetime
from dotenv import load_dotenv
from functools import wraps
from flask import json, Response, request, g, jsonify
from src.db.dbmodels.user import User
from app_source import app


def auth_required():
        def inner_decorator(func, ):
            @wraps(func)
            def decorated_auth(*args, **kwargs):

                auth_header = "Authorization"

                if auth_header not in request.headers:
                    return jsonify({"message": "Token missing"}), 401

                token = request.headers[auth_header]

                try:
                    user = Auth.get_user_by_token(token)

                    if not user:
                        return jsonify("Token invalid")

                    return func(user, *args, **kwargs)
                except Exception as e:
                    app.logger.info(e)
                    return jsonify({"message": "Unauthorized"}), 401
            return decorated_auth
        return inner_decorator
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

    def decode_token(token):
        try:
            payload = jwt.decode(token, os.environ['JWT_SECRET_KEY'], algorithms=["HS256"])
            return payload['user_id']
        except jwt.ExpiredSignatureError as e:
            error_msg = "TokenExpiredException when calling Auth.decode_token: %s\n" % e
            raise Exception(error_msg)
        except Exception as e:
            error_msg = "Exception when calling Auth.decode_token: %s\n" % e
            raise Exception(error_msg)

    def get_user_by_token(bearer_access_token):
        try:
            bearer_access_token_prefix = "Bearer token|"
            if not str(bearer_access_token).startswith(bearer_access_token_prefix):
                raise Exception(f"bearer_access_token does not start with "
                                    f"{bearer_access_token_prefix}")
            
            access_token = str(bearer_access_token).split(bearer_access_token_prefix)[1]
            payload = Auth.decode_token(access_token)
            user = User.get_user_by_id(payload)
            
            return user
        except Exception as e:
            error_msg = "TokenException when calling AuthService.get_user_by_token: %s\n"\
                % e
            raise Exception(error_msg)


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
