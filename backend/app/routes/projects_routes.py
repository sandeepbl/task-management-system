from flask import request, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import IntegrityError
from app.auth_middleware import manager_access_required
from app import app, db
from app.models import Project, User


@app.route("/projects/create/", methods=["POST"])  # Create a new project
@jwt_required()
def create_project():
    data = request.get_json()
    new_project = Project(title=data.get("title"),
                          description=data.get("description"),
                          manager_user_id=data.get("manager_user_id"))
    print(data)
    user = db.session.query(User).filter_by(id=new_project.manager_user_id).first()
    if user:

        if user.role == "Manager":
            db.session.add(new_project)
            try:
                db.session.commit()
            except IntegrityError:
                return jsonify({'message': 'Error:  duplicate key value violates unique constraint',
                                'title': data.get("title")}), 409
            return jsonify({'message': 'Project added', 'title': data.get("title")}), 201
        else:
            return jsonify({'message': 'User is not a Manager',
                            'error': "not_manager"}), 409
    else:
        return jsonify({'message': 'User Not Found',
                        'error': "not_registered_user"}), 409


@app.route("/projects/", methods=["GET"])  # Retrieve a list of projects.
@jwt_required()
def get_projects():
    project_list = list()
    for project in db.session.query(Project):
        manager_cls = User.get_by_id(project.manager_user_id)
        manager = {"username": manager_cls.username,
                   "first_name": manager_cls.first_name,
                   "last_name": manager_cls.last_name,
                   "role": manager_cls.role}
        project_list.append({"id": project.id,
                             "title": project.title,
                             "description": project.description,
                             "manager_user_id": project.manager_user_id,
                             "manager": " ".join([manager["first_name"], manager["last_name"]])})
    if project_list:
        return jsonify({"projects": project_list}), 200
    else:
        return jsonify({"message": "Error: Projects not found"}), 409


@app.route("/projects/<id>/", methods=["GET"])  # GET project details by ID
@jwt_required()
@manager_access_required
def get_project(id):
    project = db.session.query(Project).filter(Project.id == id).first()
    if project:
        return jsonify({"project": {
            "project_id": project.id,
            "project_title": project.title,
            "project_description": project.description,
            "project_manager_user_id": project.manager_user_id
        }}), 200
    else:
        return jsonify({"message": f"No project found for Project ID: {id}", "error": "no_project_found"}), 409


@app.route("/projects/<id>/", methods=["PUT"])  # Update project details
@jwt_required()
@manager_access_required
def update_project(id):
    data = request.get_json()
    db.session.query(Project).filter(Project.id == id).update({"title": data.get("title"),
                                                               "description": data.get("description"),
                                                               "manager_user_id": data.get("manager_user_id")})
    try:
        db.session.commit()
        return jsonify({"message": f"Project: {id} was modified"}), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "Project modify failed", "error": e}), 409


@app.route("/projects/<id>/", methods=["DELETE"])  # Delete a project
@jwt_required()
@manager_access_required
def delete_project(id):
    project = Project.get_project_by_id(project_id=id)
    if not project:
        return jsonify({"message": "Project not found", "error": "Project not in the database"}), 409

    db.session.delete(project)
    db.session.commit()
    return jsonify({"message": f"Deleted Project: {project.title}"}), 200
