from flask import jsonify
from app import app, jwt


@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_data):
    print(f"Expired Token, JWT Header: {jwt_header}, JWT Data: {jwt_data}")
    return jsonify({"message": "Token has expired!", "error": "token_expired"}), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    print(f"Invalid Token Error: {error}")
    return jsonify({"message": "Signature verification failed", "error": "invalid_token"}), 401


@jwt.unauthorized_loader
def missing_token_callback(error):
    print(f"Missing or Invalid Token: {error}")
    return jsonify({"message": "Request does not contain a valid token", "error": "authorization_missing"}), 401

