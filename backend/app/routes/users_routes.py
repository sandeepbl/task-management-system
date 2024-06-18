import flask
from flask import request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import IntegrityError
from app.auth_middleware import admin_access_required
from app import app, db
from app.models import User
from flask_sqlalchemy import pagination


@app.route("/users/register/", methods=["POST"])  # Register a new user
@jwt_required()
def register_user():
    username = request.json['username']
    new_user = User(username=request.json['username'],
                    first_name=request.json['first_name'],
                    last_name=request.json['last_name'],
                    role=request.json['role'])
    new_user.set_hashed_password(request.json['password'])
    db.session.add(new_user)
    try:
        db.session.commit()
    except IntegrityError:
        return jsonify({'message': 'Error: Duplicate key value violates unique constraint',
                        'username': username}), 409
    return jsonify({'message': 'User added', 'username': username}), 201


@app.route("/users/login/", methods=["POST"])  # Login and obtain a JWT token
def login_user():
    data = request.get_json()
    user = User.get_by_username(data.get("username"))

    if user and user.check_password(password=data.get("password")):
        access_token = create_access_token(identity=user.username)
        refresh_token = create_refresh_token(identity=user.username)
        return jsonify(
            {
                "message": "Login Successful",
                "tokens": {
                    "access_token": access_token,
                    "refresh_token": refresh_token
                },
                "user": {
                    "username": user.username,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "role": user.role
                }
            }
        ), 200
    return jsonify({"error": "Invalid username or password"}), 400


@app.route("/healthcheck/", methods=["GET"])  # Check if the API server is reachable
def healthcheck():
    return jsonify({"message": "I am alive"}), 200


@app.route("/access/", methods=["GET"])  # Check is JWT token gives User access
@jwt_required()
def check_access():
    return jsonify({"message": "User is Logged-In"}), 200


@app.route("/admin/", methods=["GET"])  # Check is JWT token gives Admin access
@jwt_required()
@admin_access_required
def admin_test():
    return jsonify({"message": "Admin is Logged-in"}), 200


@app.route("/refresh/", methods=["GET"])  # Refresh token when the access token has expired
@jwt_required(refresh=True)
def refresh_access():
    identity = get_jwt_identity()
    new_access_token = create_access_token(identity=identity)
    return jsonify({"access_token": new_access_token})


@app.route("/users/", methods=["GET"])  # Retrieve List of Users
@jwt_required()
def get_users():
    user_list = list()
    for user in db.session.query(User):
        user_list.append({"id": user.id,
                          "username": user.username,
                          "first_name": user.first_name,
                          "last_name": user.last_name,
                          "role": user.role})
    if user_list:
        return jsonify({"users": user_list}), 200
    else:
        return jsonify({"message": "Error: Users not found!"}), 409


@app.route("/users/<id>/", methods=["GET"])  # View User Profile
@jwt_required()
def get_user(id):
    user = User.get_by_id(id)
    if user:
        return jsonify({"id": user.id,
                        "username": user.username,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "role": user.role}), 200
    else:
        return jsonify({"message": f"User with id: {id} not found!"}), 409


@app.route("/users/<id>/", methods=["DELETE"])  # Delete User
@jwt_required()
@admin_access_required
def delete_user(id):
    user = User.get_by_id(id)
    if not user:
        return jsonify({"message": "User not found", "error": "user not in the database"}), 409

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": f"Deleted user: {user.username}"}), 200


@app.route("/users/<id>/", methods=["PUT"])  # Modify User. Admin access decorator applied
@jwt_required()
@admin_access_required
def update_user(id):
    data = request.get_json()
    db.session.query(User).filter(User.id == id).update({"username": data.get("username"),
                                                         "first_name": data.get("first_name"),
                                                         "last_name": data.get("last_name"),
                                                         "role": data.get("role")})
    try:
        db.session.commit()
        return jsonify({"message": f"User: {id} was modified"}), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "User modify failed", "error": e}), 409


@app.route("/whoami/", methods=["GET"])  # A quick way to find whoiam
@jwt_required()
def whoami():
    user_cls = User.get_by_username(get_jwt_identity())
    user = {"username": user_cls.username,
            "first_name": user_cls.first_name,
            "last_name": user_cls.last_name,
            "role": user_cls.role}
    return jsonify({"user": user}), 200
