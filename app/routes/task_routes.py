from flask import Blueprint, abort, make_response, request, Response
from app.models.task import Task
from ..db import db


tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

@tasks_bp.post("")
def create_task(): 
    request_body = request.get_json()
    title = request_body["title"]
    description = request_body["description"]

    # is_complete = check_for_completion(request_body)
    is_complete = False

    try: 
        completed_at = request_body["completed_at"]
        new_task = Task(title=title, description= description,completed_at= completed_at, is_complete=True) 

    except: 
        new_task = Task(title=title, description= description, is_complete=False)

    db.session.add(new_task)
    db.session.commit()

    response = {
        "id": new_task.id,
        "title": new_task.title,
        "description": new_task.description,
        "is_complete": new_task.is_complete
    }

    return response, 201

@tasks_bp.get("")
def get_tasks():
    query = db.select(Task)
    title_param = request.args.get("title")
    if title_param: 
        query = query.where(Task.title.ilike(f"%{title_param}%"))
        title_param = request.args.get("title")
    
    description_param = request.args.get("description")
    if description_param: 
        query = query.where(Task.description.ilike(f"%{description_param}%"))


    is_complete_param = request.args.get("is_complete")
    if is_complete_param: 
        query = query.where(Task.is_complete.ilike(f"%{is_complete_param}%"))
    

    query = query.order_by(Task.id)
    tasks = db.session.scalars(query)

    tasks_response = []

    for task in tasks: 
        tasks_response.append(get_dict(task))

    return tasks_response
    

def check_for_completion(request_body):
    try :
        request_body["completed_at"]
        return True

    except: 
        return False    

def get_dict(task):
    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "is_complete": task.is_complete
    }

