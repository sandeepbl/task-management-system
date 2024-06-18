from flask import request, jsonify
from flask_jwt_extended import jwt_required

from app import app, db
from app.models import Task


@app.route("/tasks/create/", methods=["POST"])  # Add a task to a project
@jwt_required()
def create_tasks():
    task_data = request.get_json()
    new_task = Task(title=task_data.get("title"),
                    description=task_data.get("description"),
                    assigned_user_id=task_data.get("assigned_user_id"),
                    project_id=task_data.get("project_id")
                    )
    if new_task.get_task_by_title_part(task_data.get('title')):
        return jsonify({"message": "Task already exists with the same Title",
                        "Title": task_data.get('title')}), 403

    db.session.add(new_task)
    db.session.commit()
    return jsonify({"message": "New Task added Successfully",
                    "task": {"title": new_task.title,
                             "description": new_task.description}}), 201


@app.route("/tasks/", methods=["GET"])  # Retrieve a list of all tasks
@jwt_required()
def get_tasks():
    task_list = list()
    for task in db.session.query(Task):
        if task.assigned_user_id:
            assigned_user = " ".join([task.assignee.first_name, task.assignee.last_name])
            assigned_user_id = task.assignee.id
        else:
            assigned_user = ""  # Allow unassigned tasks
            assigned_user_id = ""
        if task.project_id:
            project_title = task.project.title
        else:
            project_title = ""  # Allow tasks not related to projects
        task_list.append({"id": task.id,
                          "title": task.title,
                          "description": task.description,
                          "assigned_user": assigned_user,
                          "project_title": project_title,
                          "project_id": task.project_id,
                          "assigned_user_id": assigned_user_id})
    if task_list:
        return jsonify({"task_list": task_list}), 200
    else:
        return jsonify({"message": f"Tasks not found!"}), 200


@app.route("/tasks/project/<project_id>/", methods=["GET"])  # Retrieve a list of tasks for a project
@jwt_required()
def get_project_tasks(project_id):
    tasks = db.session.query(Task).filter_by(project_id=project_id)
    project_task_list = list()
    for task in tasks:
        if task.assigned_user_id:
            assigned_user = " ".join([task.assignee.first_name, task.assignee.last_name])
            assigned_user_id = task.assignee.id
        else:
            assigned_user = ""  # Allow unassigned tasks
            assigned_user_id = ""
        if task.project_id:
            project_title = task.project.title
        else:
            project_title = ""  # Allow tasks not related to projects
        project_task_list.append({"id": task.id,
                                  "title": task.title,
                                  "description": task.description,
                                  "assigned_user": assigned_user,
                                  "assigned_user_id": assigned_user_id,
                                  "project_title": project_title,
                                  "project_id": task.project_id})
    if project_task_list:
        return jsonify({"project_tasks": project_task_list}), 200
    else:
        return jsonify({"message": f"Project Tasks with Project id: {id} not found!"}), 409


@app.route("/tasks/<task_id>/", methods=["PUT"])  # Update task details
@jwt_required()
def update_task(task_id):
    data = request.get_json()
    db.session.query(Task).filter_by(id=task_id).update({"title": data.get("title"),
                                                         "description": data.get("description"),
                                                         "assigned_user_id": data.get("assigned_user_id"),
                                                         "project_id": data.get("project_id")})
    try:
        db.session.commit()
        return jsonify({"message": f'Task: {data.get("title")} was modified'}), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "Task modify failed", "error": e}), 409


@app.route("/tasks/<id>/", methods=["DELETE"])  # Delete task
@jwt_required()
def delete_task(id):
    task_to_delete = db.session.query(Task).filter_by(id=id).first()
    print(f"task to delete: {task_to_delete}")
    if not task_to_delete:
        return jsonify({"message": "Task not found. Can not be deleted"}), 409

    db.session.delete(task_to_delete)
    db.session.commit()
    return {"deleted-tasks": [id]}, 200
