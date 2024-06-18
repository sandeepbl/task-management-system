from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from flask_swagger_ui import get_swaggerui_blueprint

import os


def create_app(config_name=None):
    app = Flask(__name__, instance_relative_config=True)
    if not config_name:
        config_name = os.getenv('FLASK_CONFIG', 'default')
    app.config.from_object('config.DefaultConfig')
    return app


app = create_app()
CORS(app)
db = SQLAlchemy(app)
migrate = Migrate()
migrate.init_app(app, db)
jwt = JWTManager(app)

### Swagger UI configuration ###
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Flask App API"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


from app.routes import users_routes, tasks_routes, projects_routes, error_handler


@app.route("/")  # Test if the server is up and responding
def home():
    return "Hello World"
