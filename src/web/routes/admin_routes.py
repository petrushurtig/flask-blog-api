import datetime
from flask import request, json, Response, Blueprint, jsonify
from dependency_injector.wiring import inject, Provide

from app import app
from src.interfaces.models.user import IUser
from src.common.containers import Container
from src.services.user_service import UserService
from src.web.middleware.auth_middleware import auth_required_admin
from src.common.exceptions.request_data_exception import RequestDataException
from src.common.exceptions.user_not_found_exception import UserNotFoundException

blueprint = Blueprint("admin_user_api", __name__)

@blueprint.route("/", methods=["GET"])
@inject
@auth_required_admin()
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

@blueprint.route("/<user_id>", methods=["GET"])
@inject
@auth_required_admin()
def get_user(
    user: IUser,
    user_id: int,
    user_service: UserService = Provide[Container.user_service]
):
    try:

        user = user_service.find_by_id(user_id)
        if not user:
            return jsonify({"message": "user not found"}), 404
        
        return jsonify(user.json()), 200
    except Exception as e:
        app.logger.info(e)
        return jsonify({"message": "Server error"}), 500

@blueprint.route("/<user_id>", methods=["PUT"])
@inject
@auth_required_admin()
def update_user(
    user: IUser,
    user_id: int,
    user_service: UserService = Provide[Container.user_service]
):

    try:
        user_data = request.get_json()
        user: IUser = user_service.find_by_id(user_id)

        if not user:
            return jsonify({"message": "user not found"}), 404

        updated_user: IUser = user_service.update_user(user_id, user_data)

        return jsonify(updated_user.json()), 200
    except RequestDataException as e:
        app.logger.info(e)
        msg = {"message": str(e)}
        return jsonify(msg), 400
    except Exception as e:
        app.logger.info(e)
        return jsonify({"message": "Server error"})

@blueprint.route("/<user_id>", methods=["DELETE"])
@inject
@auth_required_admin()
def delete_user(
    user: IUser,
    user_id: int,
    user_service: UserService = Provide[Container.user_service]
):
    try:
        deleted: bool = user_service.delete_user(user=user, user_id=user_id)

        if not deleted:
            return jsonify({"message": "Server error"}), 500

        return jsonify({"deleted": True})
    except Exception as e:
        app.logger.info(e)

        return jsonify({"message": "Server error"}), 500