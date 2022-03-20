from validate_email import validate_email
from ..auth_token import guard
from flask import Blueprint, request
from ..models import User, db
auth_routes = Blueprint('auth', __name__)
@auth_routes.route('/login', methods=["POST"])
def login():
    req = request.get_json(force=True)
    email = req.get("email", None)
    password = req.get("password", None)
    user = guard.authenticate(email, password)
    return {"access_token": guard.encode_jwt_token(user), "user": user.to_dict()}
@auth_routes.route('/refresh', methods=["POST"])
def refresh():
    req = request.get_json(force=True)
    old_token = req.get('token', None)
    try:
        x = guard.extract_jwt_token(old_token)
        return {'access_token': old_token}
    except:
        token = guard.refresh_jwt_token(old_token)
        return {'access_token': token}

@auth_routes.route('/signup', methods=['POST'])
def sign_up():
    req = request.get_json(force=True)
    username = req.get('username', None)
    email = req.get('email', None)
    password = req.get('password', None)

    if (any(User.query.filter(User.email == email).all())):
        return {'message': 'email exists'}, 401
    if (not validate_email(email)):
        return {'message': 'email is not valid'}

    new_user = User(username=username, email=email, password=guard.hash_password(password))
    if (not new_user.valid_password(password)[0]):
        return {'message': f' invalid password - {new_user.valid_password(password)[1]}'}, 401

    db.session.add(new_user)
    db.session.commit()
    return {'message': 'success'}
