from functools import wraps
from flask_jwt_extended import get_jwt_identity
from flask import jsonify
from app.models import User


def admin_access_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        identity = get_jwt_identity()
        user = User.get_by_username(identity)
        if user.role != "Admin":
            return jsonify({"message": "Admin login required!", "error": "not_admin_user"}), 401
        return f(*args, **kwargs)

    return wrap


def manager_access_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        identity = get_jwt_identity()
        user = User.get_by_username(identity)
        if user.role != "Manager":
            return jsonify({"message": "Manager access required!", "error": "not_manager_user"}), 401
        return f(*args, **kwargs)

    return wrap
