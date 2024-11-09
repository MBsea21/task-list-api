from flask import Blueprint, abort, make_response, request, Response
from app.models.task import Task
from app.routes.utilities_routes import create_model, validate_model, get_models_with_filters, check_for_completion, delete_model
from app.routes.slack_functions import send_message
from datetime import datetime
from ..db import db
import requests
import os


tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")
invalid_data_response = ({"details" : "Invalid data"}, 400)

#create a new task in database
@tasks_bp.post("")
def create_task(): 
    request_body = request.get_json()
    return create_model(Task,request_body)

@tasks_bp.get("")
def get_tasks(): 
    request_arguements= request.args
    return get_models_with_filters(Task,request_arguements), 200


#get task by task id: 
@tasks_bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_model(Task,task_id)
    task_dict = task.to_dict()
    response = {"task":task_dict}
    expected = {
        "task": {
            "id": 1,
            "title": "A Brand New Task",
            "description": "Test Description",
            "is_complete": False
        }
    }
    print("the task dictionary is:\n", dict)
    print("the expected dictitonary was:\n",expected) 
    return response,200

#update task
@tasks_bp.put("/<task_id>")
def update_task(task_id):
    task = validate_model(Task,task_id)
    
    request_body = request.get_json()
    task.title = request_body["title"]
    task.description = request_body["description"]
    try:
        completed_at = request_body["completed_at"]
    except:
        completed_at=task.completed_at
    
    task.completed_at = completed_at
    db.session.commit()
    
    response = {"task":task.to_dict()}
    return response, 200


#Delete task
@tasks_bp.delete("/<task_id>")
def delete_task(task_id):
    task = validate_model(Task,task_id)
    return delete_model(Task, task)


#route 2
@tasks_bp.patch("/<task_id>/mark_complete")
def mark_complete(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = datetime.now()
    message = f"Task {task.title} has been marked as complete!"
    slack_response= send_message(message)

    if slack_response.status_code == 200: 
        response = {"task":task.to_dict()}
        db.session.commit()
        return (response,200)
    elif slack_response.status_code != 200: 
        return {"errror": "failed to send slack notification"}, 500




@tasks_bp.patch("/<task_id>/mark_incomplete")
def mark_incomplete(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = None
    db.session.commit()
    response = {"task": task.to_dict()}
    return make_response(response,200)


