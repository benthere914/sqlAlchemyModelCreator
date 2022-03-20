from operator import mod
import re
import os
from statistics import mode
import inflect

p = inflect.engine()

class Model():
    def __init__(self):
        self.models = []
        self.current_model = {}
        self.types = {
            "db.Integer": ['int', 'INT', 'SERIAL', 'serial', 'integer' 'INTEGER'],
            "db.String(255)": ['VARCHAR', 'varchar', 'str'],
            "db.Boolean": ['boolean', "BOOLEAN", 'bool', 'BOOL'],
            "JSON": ['json', 'JSON', 'map', 'MAP'],
            "db.DateTime": ["DATETIME", "TIMESTAMP", "datetime", "timestamp"]
        }
        self.model_lines = []
        self.route_lines = []
        self.main_lines = []
        self.include_jwt = True
        self.table_name = ""
        self.class_name = ""
        self.keys = []

    def init_models(self):
        f = open('app/models/__init__.py', 'w')
        f.write('from .db import db\n')
        f.close()
        f = open('app/models/db.py', 'w')
        f.write('from flask_sqlalchemy import SQLAlchemy\n\ndb = SQLAlchemy')
        f.close()

    def create_auth_route(self):
        auth_lines = []
        auth_lines.append('from validate_email import validate_email\n')
        auth_lines.append('from ..auth_token import guard\n')
        auth_lines.append('from flask import Blueprint, request\n')
        auth_lines.append('from ..models import User, db\n')
        auth_lines.append('auth_routes = Blueprint(\'auth\', __name__)\n')
        auth_lines.append('@auth_routes.route(\'/login\', methods=["POST"])\n')
        auth_lines.append('def login():\n')
        auth_lines.append('    req = request.get_json(force=True)\n')
        auth_lines.append('    email = req.get("email", None)\n')
        auth_lines.append('    password = req.get("password", None)\n')
        auth_lines.append('    user = guard.authenticate(email, password)\n')
        auth_lines.append('    return {"access_token": guard.encode_jwt_token(user), "user": user.to_dict()}\n')
        auth_lines.append('@auth_routes.route(\'/refresh\', methods=["POST"])\n')
        auth_lines.append('def refresh():\n')
        auth_lines.append('    req = request.get_json(force=True)\n')
        auth_lines.append('    old_token = req.get(\'token\', None)\n')
        auth_lines.append('    try:\n')
        auth_lines.append('        x = guard.extract_jwt_token(old_token)\n')
        auth_lines.append('        return {\'access_token\': old_token}\n')
        auth_lines.append('    except:\n')
        auth_lines.append('        token = guard.refresh_jwt_token(old_token)\n')
        auth_lines.append('        return {\'access_token\': token}\n\n')
        auth_lines.append('@auth_routes.route(\'/signup\', methods=[\'POST\'])\n')
        auth_lines.append('def sign_up():\n')
        auth_lines.append('    req = request.get_json(force=True)\n')
        auth_lines.append('    username = req.get(\'username\', None)\n')
        auth_lines.append('    email = req.get(\'email\', None)\n')
        auth_lines.append('    password = req.get(\'password\', None)\n\n')
        auth_lines.append('    if (any(User.query.filter(User.email == email).all())):\n')
        auth_lines.append('        return {\'message\': \'email exists\'}, 401\n')
        auth_lines.append('    if (not validate_email(email)):\n')
        auth_lines.append('        return {\'message\': \'email is not valid\'}\n\n')
        auth_lines.append('    new_user = User(username=username, email=email, password=guard.hash_password(password))\n')
        auth_lines.append('    if (not new_user.valid_password(password)[0]):\n')
        auth_lines.append('        return {\'message\': f\' invalid password - {new_user.valid_password(password)[1]}\'}, 401\n\n')
        auth_lines.append('    db.session.add(new_user)\n')
        auth_lines.append('    db.session.commit()\n')
        auth_lines.append('    return {\'message\': \'success\'}\n')
        f = open('app/routes/auth.py', 'w')
        f.writelines(auth_lines)
        f.close()

    def create_auth_token_file(self):
        f = open('app/auth_token.py', 'w')
        f.writelines('from flask_praetorian import Praetorian, auth_required, current_user\nguard = Praetorian()')
        f.close()

    def create_config_file(self):
        config_lines = []
        config_lines.append('import os\n')
        config_lines.append('from os.path import join, dirname\n')
        config_lines.append('from dotenv import load_dotenv\n\n')
        config_lines.append('dotenv_path = join(dirname(__file__), \'.env\')\n')
        config_lines.append('load_dotenv(dotenv_path)\n\n\n')
        config_lines.append('class Config:\n')
        config_lines.append('    SECRET_KEY = os.environ.get("SECRET")\n')
        config_lines.append('    SQLALCHEMY_TRACK_MODIFICATIONS = False\n')
        config_lines.append('    SQLALCHEMY_DATABASE_URI = f\'postgresql://{os.environ.get("DATABASE_URL")[11:]}\'\n')
        f = open('app/config.py', 'w')
        f.writelines(config_lines)
        f.close()

    def create_procfile(self):
        f = open('Procfile', 'w')
        f.write('web: gunicorn wsgi:app')
        f.close()

    def create_runtime(self):
        f = open('runtime.txt', 'w')
        f.write('python-3.10.0')
        f.close()

    def create_wsgi(self):
        f = open('wsgi.py', 'w')
        f.write('from app.main import app\n\nif __name__ == "__main__":\n    app.run()')
        f.close()

    def create_gitignore(self):
        f = open('.gitignore', 'w')
        f.write('.env')
        f.write('__pycache__')
        f.write('postgre.sql')
        f.close()


    def init_routes(self):
        self.create_auth_route()
        f = open('app/routes/__init__.py', 'w')
        f.write('from .auth import auth\n')
        f.close()

    def create_structure(self):
        os.mkdir('app')
        os.mkdir('app/models')
        os.mkdir('app/routes')
        self.init_models()
        self.init_routes()
        self.create_auth_token_file()
        self.create_config_file()
        self.create_procfile()
        self.create_runtime()
        self.create_wsgi()
        self.create_gitignore()
        self.create_main_file()
        self.set_models()
        self.create_files()

    def startModel(self, string):
        self.current_model["table_name"] = string[14:-4]

    def end_model(self, string):
        self.models.append(self.current_model)
        return {}

    def get_type(self, string):
        words = string.split()
        for type_ in self.types:
            if any([item for item in self.types[type_] if item in words[1]]):
                return type_

    def get_key(self, string, result):
        if not 'keys' in self.current_model:
            self.current_model['keys'] = []
        self.current_model['keys'].append({
            "name": result.group(1),
            'type': self.get_type(string),
            "primary": ("PRIMARY" in string),
            "not_null": ("NOT NULL" in string)
            })

    def set_models(self):
        f = open("postgre.sql", "r")
        for x in f:
            started = ("CREATE TABLE" in x)
            finished = (");" in x)
            result = re.search('\"(.*)\"', x)
            if (started):
                self.startModel(x)
            elif (finished):
                self.current_model = self.end_model(x)
            elif (bool(result)):
                self.get_key(x, result)
        f.close

    def create_main_file(self):
        self.main_lines.append('from flask import Flask\n')
        self.main_lines.append('from flask_cors import CORS\n')
        self.main_lines.append('from .config import Config\n')
        self.main_lines.append('from .models import db, User\n')
        self.main_lines.append('from .routes import auth_routes\n')
        self.main_lines.append('from .auth_token import guard\n\n')
        self.main_lines.append('# import any blueprints from routes folder\n')
        self.main_lines.append('app = Flask(__name__)\n\n')
        self.main_lines.append('app.config.from_object(Config)\n')
        self.main_lines.append('@app.route(\'/\')\n')
        self.main_lines.append('def home_route():\n')
        self.main_lines.append('    return {"message": "got to the home route"}\n\n')
        self.main_lines.append('app.register_blueprint(auth_routes, url_prefix=\'/auth\')\n\n')
        self.main_lines.append('# register blueprints to app\n\n')
        self.main_lines.append('guard.init_app(app, User)\n')
        self.main_lines.append('db.init_app(app)\n')
        self.main_lines.append('CORS(app)\n\n')
        self.main_lines.append('if __name__ == "__main__":\n')
        self.main_lines.append('    app.debug = True\n')
        self.main_lines.append('    app.run(threaded=True)')
        f = open('app/main.py', 'w')
        f.writelines(self.main_lines)
        f.close()

    def create_model_files(self, model):
        f = open(f'app/models/{model["table_name"]}.py', 'a')
        self.model_lines = []
        self.model_lines.append('from .db import db\n')
        if (any([key for key in model['keys'] if key['type'] == 'JSON'])):
            self.model_lines.append('from sqlalchemy.dialects.postgresql import JSON\n')
        if (model['table_name'] == 'users'):
            self.model_lines.append('from flask_login import UserMixin\n\n')
            self.model_lines.append('class User(db.Model, UserMixin):\n')
        else:
            self.model_lines.append(f'\nclass {self.class_name}(db.Model):\n')

        self.model_lines.append(f'    __tablename__ = "{model["table_name"]}"\n')

        for key in model["keys"]:
            self.model_lines.append(f'    {key["name"]} = db.Column({key["type"]}, primary_key={key["primary"]}, nullable={not key["not_null"]})\n')

        self.model_lines.append('\n\n')

        self.model_lines.append('    def to_dict(self):\n')
        self.model_lines.append('        return {\n')
        for key in model['keys']:
            if 'password' in key["name"]:
                continue
            self.model_lines.append(f'            "{key["name"]}": self.{key["name"]},\n')
        self.model_lines.append("        }\n\n")

        if (model['table_name'] == "users" and self.include_jwt):
            self.model_lines.append('    def valid_password(self, password):\n')
            self.model_lines.append("        if (not (any([char for char in password if char in '01234567890']))):\n")
            self.model_lines.append("            return [False, 'a number']\n")
            self.model_lines.append("        if (not (any([char for char in password if char in '`~!@#$%^&*()_-+={[}]|\\;:\\'\",<.>/?']))):\n")
            self.model_lines.append("            return [False, 'any special characters']\n")
            self.model_lines.append("        if (not any([char for char in password if char in [letter.upper() for letter in 'abcdefghijklmnoppqrstuvwxyz']])):\n")
            self.model_lines.append("            return [False, 'any upper case letters']\n")
            self.model_lines.append("        if (len(password) < 8):\n")
            self.model_lines.append("            return [False, 'at least 8 characters']\n")
            self.model_lines.append("        return [True, '']\n\n")

            self.model_lines.append("    @property\n")
            self.model_lines.append("    def password(self):\n")
            self.model_lines.append("        return self.hashed_password\n\n")

            self.model_lines.append("    @password.setter\n")
            self.model_lines.append("    def password(self, password):\n")
            self.model_lines.append("        self.hashed_password = password\n\n")

            self.model_lines.append("    @property\n")
            self.model_lines.append("    def identity(self):\n")
            self.model_lines.append("        return self.id\n\n")

            self.model_lines.append("    @property\n")
            self.model_lines.append("    def rolenames(self):\n")
            self.model_lines.append("        try:\n")
            self.model_lines.append("            return self.roles.split(\",\")\n")
            self.model_lines.append("        except Exception:\n")
            self.model_lines.append("            return []\n\n")

            self.model_lines.append("    @classmethod\n")
            self.model_lines.append("    def lookup(cls, username):\n")
            self.model_lines.append("        return cls.query.filter_by(email=username).one_or_none()\n\n")

            self.model_lines.append("    @classmethod\n")
            self.model_lines.append("    def identify(cls, id):\n")
            self.model_lines.append("        return cls.query.get(id)\n\n")

            self.model_lines.append("    def is_valid(self):\n")
            self.model_lines.append("        return self.is_active\n\n")

        f.writelines(self.model_lines)
        f.close()
        f = open('app/models/__init__.py', 'a')
        f.writelines(f'from .{self.table_name} import {self.class_name}\n')
        f.close()

    def create_one_route(self):
        self.route_lines.append(f'@{self.blueprint}.route(\'/\', methods=["POST"])\n')
        self.route_lines.append(f'def add_one_{self.item_name}():\n')
        self.route_lines.append(f'    req = request.get_json()\n')
        add_one_string = ""
        for key in self.keys:
            if (key["name"] == "id"):
                continue
            self.route_lines.append(f'    {key["name"]} = req.get("{key["name"]}", None)\n')
            add_one_string += f'{key["name"]} = {key["name"]},'
        self.route_lines.append(f'    new_{self.item_name} = {self.class_name}({add_one_string[:-1]})\n')
        self.route_lines.append(f'    db.session.add(new_{self.item_name})\n')
        self.route_lines.append(f'    db.session.commit()\n\n')

    def create_multiple_route(self):
        self.route_lines.append(f'@{self.blueprint}.route(\'/\', methods=["POST"])\n')
        self.route_lines.append(f'def add_multiple_{self.table_name}():\n')
        self.route_lines.append(f'    req = request.get_json()\n')
        self.route_lines.append(f'    {self.table_name} = req.get("{self.table_name}", None)\n')
        self.route_lines.append(f'    for {self.item_name} in {self.table_name}:\n')
        add_multiple_string = ""
        for key in self.keys:
            if (key["name"] == "id"):
                continue
            add_multiple_string += f'{key["name"]} = {self.item_name}["{key["name"]}"],'
        self.route_lines.append(f'        new_{self.item_name} = {self.class_name}({add_multiple_string[:-1]})\n')
        self.route_lines.append(f'        db.session.add(new_{self.item_name})\n')
        self.route_lines.append(f'    db.session.commit()\n\n')

    def create_post_routes(self):
        self.create_one_route()
        self.create_multiple_route()

    def get_one_route(self):
        self.route_lines.append(f'@{self.blueprint}.route(\'/<int:id>\')\n')
        self.route_lines.append(f'def get_one_{self.item_name}():\n')
        self.route_lines.append(f'    return {{"{self.item_name}": ({self.class_name}.query.get(id)).to_dict()}}\n\n')

    def get_multiple_route(self):
        self.route_lines.append(f'@{self.blueprint}.route(\'/\')\n')
        self.route_lines.append(f'def get_all_{self.table_name}():\n')
        self.route_lines.append(f'    return {{\"{self.table_name}": [{self.item_name}.to_dict() for {self.item_name} in {self.class_name}.query.all()]}}\n\n')

    def create_get_routes(self):
        self.get_one_route()
        self.get_multiple_route()

    def update_one_route(self):
        self.route_lines.append(f'@{self.blueprint}.route(\'/<int:id>\', methods=["PUT"])\n')
        self.route_lines.append(f'def update_one_{self.table_name}(id):\n')
        self.route_lines.append(f'    req = request.get_json()\n')
        self.route_lines.append(f'    current_{self.item_name} = {self.class_name}.query.get(id)\n')
        for key in self.keys:
            if (key["name"] == "id"):
                continue
            self.route_lines.append(f'    current_{self.item_name}.{key["name"]} = req.get("{key["name"]}", None)\n')
        self.route_lines.append(f'    db.session.commit()\n\n')

    def update_multiple_route(self):
        self.route_lines.append(f'@{self.blueprint}.route(\'/\', methods=["PUT"])\n')
        self.route_lines.append(f'def update_multiple_{self.table_name}():\n')
        self.route_lines.append(f'    req = request.get_json()\n')
        self.route_lines.append(f'    {self.table_name} = req.get("{self.table_name}", None)\n')
        self.route_lines.append(f'    for current_{self.item_name} in {self.table_name}:\n')
        self.route_lines.append(f'        temp_{self.item_name} = {self.class_name}.query.get(current_{self.item_name}["id"])\n')
        for key in self.keys:
            if (key["name"] == "id"):
                continue
            self.route_lines.append(f'        temp_{self.item_name}.{key["name"]} = current_{self.item_name}["{key["name"]}"]\n')
        self.route_lines.append(f'        db.session.commit()\n\n')

    def create_put_routes(self):
        self.update_one_route()
        self.update_multiple_route()

    def delete_one_route(self):
        self.route_lines.append(f'@{self.blueprint}.route(\'/<int:id>\', methods=["delete"])\n')
        self.route_lines.append(f'def delete_one_{self.item_name}(id):\n')
        self.route_lines.append(f'    {self.class_name}.query.get(id).delete()\n')
        self.route_lines.append(f'    db.session.commit()\n\n')

    def delete_multiple_route(self):
        self.route_lines.append(f'@{self.blueprint}.route(\'/\', methods=["delete"])\n')
        self.route_lines.append(f'def delete_multiple_{self.table_name}():\n')
        self.route_lines.append(f'    req = request.get_json()\n')
        self.route_lines.append(f'    {self.table_name} = req.get({self.table_name})\n')
        self.route_lines.append(f'    for {self.item_name} in {self.table_name}:\n')
        self.route_lines.append(f'        {self.class_name}.query.get({self.item_name}["id"]).delete()\n')
        self.route_lines.append(f'    db.session.commit()\n\n')

    def create_delete_routes(self):
        self.delete_one_route()
        self.delete_multiple_route()

    def init_route(self, model):
        self.route_lines = []
        self.keys = model["keys"]
        self.item_name = p.singular_noun(model["table_name"])
        self.table_name = model['table_name']
        self.class_name = f'{model["table_name"][0].upper()}{self.item_name[1:]}'
        self.blueprint = f'{self.item_name}_routes'
        self.route_lines.append('from flask import Blueprint, request\n')
        self.route_lines.append('from ..auth_token import auth_required\n')
        self.route_lines.append(f'from ..models import {self.class_name}, db\n')
        self.route_lines.append(f'{self.blueprint} = Blueprint(\'{self.table_name}\', __name__)\n\n')

    def create_routes(self, model):
        f = open(f'app/routes/{model["table_name"]}.py', 'a')
        self.init_route(model)
        self.create_post_routes()
        self.create_get_routes()
        self.create_put_routes()
        self.create_delete_routes()
        f.writelines(self.route_lines)
        f.close()
        f = open(f'app/routes/__init__.py', 'a')
        f.writelines(f'from .{self.table_name} import {self.blueprint}\n')
        f.close()
        f = open(f'app/main.py', 'r')
        data = f.readlines()
        data[4] = f'{data[4][:-1]}, {self.blueprint}\n'
        data[15] += f'app.register_blueprint({self.blueprint}, url_prefix="/{self.table_name}")\n'
        f.close()
        f = open(f'app/main.py', 'w')
        f.writelines(data)
        f.close()

    def create_files(self):
        for model in self.models:
            if ('table_name' in model):
                self.create_routes(model)
                self.create_model_files(model)

    def delete_files(self):
        for model in self.models:
            if ('table_name' in model and os.path.exists(f'app/models/{model["table_name"]}')):
                os.remove(f'app/models/{model["table_name"]}')

model = Model()
model.create_structure()
# model.create_main_file()
# model.set_models()
# model.delete_files()
# model.create_files()
