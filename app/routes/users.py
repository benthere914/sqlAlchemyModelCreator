from flask import Blueprint, request
from ..auth_token import auth_required
from ..models import User, db
user_routes = Blueprint('users', __name__)

@user_routes.route('/', methods=["POST"])
def add_one_user():
    req = request.get_json()
    username = req.get("username", None)
    email = req.get("email", None)
    hashed_password = req.get("hashed_password", None)
    new_user = User(username = username,email = email,hashed_password = hashed_password)
    db.session.add(new_user)
    db.session.commit()

@user_routes.route('/', methods=["POST"])
def add_multiple_users():
    req = request.get_json()
    users = req.get("users", None)
    for user in users:
        new_user = User(username = user["username"],email = user["email"],hashed_password = user["hashed_password"])
        db.session.add(new_user)
    db.session.commit()

@user_routes.route('/<int:id>')
def get_one_user():
    return {"user": (User.query.get(id)).to_dict()}

@user_routes.route('/')
def get_all_users():
    return {"users": [user.to_dict() for user in User.query.all()]}

@user_routes.route('/<int:id>', methods=["PUT"])
def update_one_users(id):
    req = request.get_json()
    current_user = User.query.get(id)
    current_user.username = req.get("username", None)
    current_user.email = req.get("email", None)
    current_user.hashed_password = req.get("hashed_password", None)
    db.session.commit()

@user_routes.route('/', methods=["PUT"])
def update_multiple_users():
    req = request.get_json()
    users = req.get("users", None)
    for current_user in users:
        temp_user = User.query.get(current_user["id"])
        temp_user.username = current_user["username"]
        temp_user.email = current_user["email"]
        temp_user.hashed_password = current_user["hashed_password"]
        db.session.commit()

@user_routes.route('/<int:id>', methods=["delete"])
def delete_one_user(id):
    User.query.get(id).delete()
    db.session.commit()

@user_routes.route('/', methods=["delete"])
def delete_multiple_users():
    req = request.get_json()
    users = req.get(users)
    for user in users:
        User.query.get(user["id"]).delete()
    db.session.commit()

