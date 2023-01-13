from dependency_injector.wiring import inject, Provide
from flask import Blueprint, jsonify, request

from app_source import app
from src.db.services.auth_service import AuthService
from src.dependency.containers import Container

blueprint = Blueprint("auth_api", __name__)

@blueprint.route("/login", methods=["POST"])
@inject
def login(
    auth_service: AuthService = Provide[Container.auth_service]
):
    try:
        data = request.get_json()

        if "password" not in data:
            msg = {"message": "Password missing"}
            return jsonify(msg, data), 400

        if "email" not in data:
            msg = {"message": "Email missing"}
            return jsonify(msg, data), 400

        password: str = str(data["password"])
        email: str = str(data["email"])

        try:
            user_tokens = auth_service.login(email, password)
        except Exception:
            msg = {"message": "Invalid credentials"}
            return jsonify(msg), 401

        return jsonify(user_tokens), 200

    except Exception as e:
        app.logger.info(e)
        return jsonify({"message": "Server error"}), 500

    #get new access_token