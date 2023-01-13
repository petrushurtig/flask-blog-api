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
