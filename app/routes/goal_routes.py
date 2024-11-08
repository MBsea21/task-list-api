from flask import Blueprint, abort, make_response, request, Response
from app.models.task import Task
from ..db import db
from datetime import datetime
from app.routes.utilities_routes import create_model, validate_model, get_models_with_filters, check_for_completion, delete_model
from app.models.goal import Goal
import requests

goals_bp = Blueprint("goals_bp",__name__, url_prefix= "/goals")


@goals_bp.post("")
def create_goal():
    request_body = request.get_json()
    return create_model(Goal,request_body)

@goals_bp.get("")
def get_goals():
    request_arguements = request.args
    return get_models_with_filters(Goal, request_arguements)

@goals_bp.get("/<goal_id>")
def get_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    response = {"goal": goal.to_dict()}
    return make_response(response, 200)

@goals_bp.put("/<goal_id>")
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    goal_title = request_body["title"]
    db.session.commit()

    response_body = {"message": f"Goal #{goal_id} succesfully updated"}
    return make_response(response_body, 200)

@goals_bp.delete("/<goal_id>")
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    return delete_model(Goal, goal)