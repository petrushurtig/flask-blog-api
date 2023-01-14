from dependency_injector.wiring import inject, Provide
from dotenv import load_dotenv
from functools import wraps
from flask import json, Response, request, g, jsonify

from app_source import app
from src.interfaces.repositories.user_repository import IUserRepository
from src.dependency.containers import Container
from src.db.services.auth_service import AuthService

def auth_required():
    def inner_decorator(func, ):
        @wraps(func)
        @inject
        def decorated_auth(
            *args,
            auth_service: AuthService = Provide[Container.auth_service], 
            **kwargs):

            auth_header = "Authorization"

            if auth_header not in request.headers:
                return jsonify({"message": "Token missing"}), 401

            token = request.headers[auth_header]

            try:
                user = auth_service.get_user_by_token(token)

                if not user:
                    return jsonify("Token invalid")

                return func(user, *args, **kwargs)
            except Exception as e:
                app.logger.info(e)
                return jsonify({"message": "Unauthorized"}), 401
        return decorated_auth
    return inner_decorator