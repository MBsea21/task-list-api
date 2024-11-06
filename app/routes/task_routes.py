from flask import Blueprint, abort, make_response, request, Response
from app.models.task import Task
from ..db import db
from datetime import datetime


tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")
invalid_data_response = ({"details" : "Invalid data"}, 400)

#create a new task in database
@tasks_bp.post("")
def create_task(): 
    request_body = request.get_json()
    try: 
        title = request_body["title"]
    except: 
        abort(make_response(invalid_data_response))

    try:
        description = request_body["description"]
    except: 
        abort(make_response(invalid_data_response))

    # is_complete = check_for_completion(request_body)
    is_complete = False
##completed_at not an attribute
    try: 
        completed_at = request_body["completed_at"]
    except: 
        completed_at = None
    new_task = Task(title=title, description= description,completed_at= completed_at) 


    db.session.add(new_task)
    db.session.commit()
    

    is_complete = check_for_completion(new_task)
    response = {"task":{
        "id": new_task.id,
        "title": new_task.title,
        "description": new_task.description,
        "is_complete": is_complete
    }}

    return response, 201

#get all tasks with query paramaters added in 
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
    

    sort_param = request.args.get("sort")
    if sort_param == "asc": 
        query = query.order_by(Task.title.asc())

    elif sort_param == "desc":
        query = query.order_by(Task.title.desc())
    
    tasks = db.session.scalars(query)

    tasks_response = []

    for task in tasks:  
        tasks_response.append(get_dict(task))

    return tasks_response,200
    

#get task by task id: 
@tasks_bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_task(task_id)
    task_dict = get_dict(task)
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
    task = validate_task(task_id)
    
    request_body = request.get_json()
    task.title = request_body["title"]
    task.description = request_body["description"]
    try:
        completed_at = request_body["completed_at"]
    except:
        completed_at=task.completed_at
    
    task.completed_at = completed_at
    db.session.commit()
    
    response = {"task":get_dict(task)}
    return response, 200


#Delete task
@tasks_bp.delete("/<task_id>")
def delete_task(task_id):
    task = validate_task(task_id)
    task_title = task.title

    db.session.delete(task)
    db.session.commit()
    details = f"Task {task_id} \"{task_title}\" successfully deleted"
    response_body = {"details" : details}

    return response_body

@tasks_bp.patch("/<task_id>/mark_complete")
def mark_complete(task_id):
    task = validate_task(task_id)
    task.completed_at = datetime.now()
    db.session.commit()
    response = {"task": get_dict(task)}
    return make_response(response, 200)

@tasks_bp.patch("/<task_id>/mark_incomplete")
def mark_incomplete(task_id):
    task = validate_task(task_id)
    task.completed_at = None
    db.session.commit()
    response = {"task": get_dict(task)}
    return make_response(response,200)
#helperfunctions

def check_for_completion(task):
    completed_at = task.completed_at
    if completed_at is None: 
        return False
    else: 
        return True

def get_dict(task):
    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "is_complete": check_for_completion(task)
    }

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        response = ({"details" : "invalid data"},400)
        abort(make_response(response))
    
    query = db.select(Task).where(Task.id == task_id)
    task = db.session.scalar(query)

    if not task:
        response = ({"details": f"task {task_id} not found"},404)
        abort(make_response(response))
    
    return task
    



