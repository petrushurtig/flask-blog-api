import datetime
from flask import request, json, Response, Blueprint, jsonify
from dependency_injector.wiring import inject, Provide

from app_source import app
from src.interfaces.models.user import IUser
from src.dependency.containers import Container
from src.db.services.user_service import UserService
from src.web.middleware.auth_middleware import auth_required

blueprint = Blueprint("admin_user_api", __name__)

@blueprint.route("/", methods=["GET"])
@inject
@auth_required()
def get_all_users(
    user: IUser,
    user_service: UserService = Provide[Container.user_service]
):
    try:
        users = user_service.get_all_users()

        return jsonify(users), 200
    except Exception as e:
        app.logger.info(e)
        return jsonify({"message": "Server error"}), 500