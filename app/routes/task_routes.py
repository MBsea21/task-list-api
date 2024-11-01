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
##completed_at not an attribute
    try: 
        completed_at = request_body["completed_at"]
    except: 
        completed_at = None
    new_task = Task(title=title, description= description,completed_at= completed_at) 



    db.session.add(new_task)
    db.session.commit()
    

    is_complete = check_for_completion(new_task)
    response = {
        "id": new_task.id,
        "title": new_task.title,
        "description": new_task.description,
        "is_complete": is_complete
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

    return tasks_response,200
    


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
        response = ({"message" : f"task {task_id} not a valid id"},400)
        abort(make_response(response))
    
    query = db.select(Task).where(Task.id == task_id)
    task = db.session.scalar(query)

    if not task:
        response = ({"message": f"task {task_id} not found"},404)
        abort(make_response(response))
    
    return task
    



