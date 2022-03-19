import re
import os
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
        self.lines = []
        self.include_jwt = True

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

    def create_lines(self, model):
        self.lines = []

        self.lines.append('from .db import db\n')

        if (any([key for key in model['keys'] if key['type'] == 'JSON'])):
            self.lines.append('from sqlalchemy.dialects.postgresql import JSON\n')

        if (model['table_name'] == 'users'):
            self.lines.append('from flask_login import UserMixin\n\n')
            self.lines.append('class User(db.Model, UserMixin):\n')
        else:
            self.lines.append(f'\nclass {model["table_name"][0].upper()}{p.singular_noun(model["table_name"][1:])}(db.Model):\n')

        self.lines.append(f'    __tablename__ = "{model["table_name"]}"\n')

        for key in model["keys"]:
            self.lines.append(f'    {key["name"]} = db.Column({key["type"]}, primary_key={key["primary"]}, nullable={not key["not_null"]})\n')

        self.lines.append('\n\n')

        self.lines.append('    def to_dict(self):\n')
        self.lines.append('        return {\n')
        for key in model['keys']:
            if 'password' in key["name"]:
                continue
            self.lines.append(f'            "{key["name"]}": self.{key["name"]},\n')
        self.lines.append("        }\n\n")

        if (model['table_name'] == "users" and self.include_jwt):
            self.lines.append('    def valid_password(self, password):\n')
            self.lines.append("        if (not (any([char for char in password if char in '01234567890']))):\n")
            self.lines.append("            return [False, 'a number']\n")
            self.lines.append("        if (not (any([char for char in password if char in '`~!@#$%^&*()_-+={[}]|\\;:\\'\",<.>/?']))):\n")
            self.lines.append("            return [False, 'any special characters']\n")
            self.lines.append("        if (not any([char for char in password if char in [letter.upper() for letter in 'abcdefghijklmnoppqrstuvwxyz']])):\n")
            self.lines.append("            return [False, 'any upper case letters']\n")
            self.lines.append("        if (len(password) < 8):\n")
            self.lines.append("            return [False, 'at least 8 characters']\n")
            self.lines.append("        return [True, '']\n\n")

            self.lines.append("    @property\n")
            self.lines.append("    def password(self):\n")
            self.lines.append("        return self.hashed_password\n\n")

            self.lines.append("    @password.setter\n")
            self.lines.append("    def password(self, password):\n")
            self.lines.append("        self.hashed_password = password\n\n")

            self.lines.append("    @property\n")
            self.lines.append("    def identity(self):\n")
            self.lines.append("        return self.id\n\n")

            self.lines.append("    @property\n")
            self.lines.append("    def rolenames(self):\n")
            self.lines.append("        try:\n")
            self.lines.append("            return self.roles.split(\",\")\n")
            self.lines.append("        except Exception:\n")
            self.lines.append("            return []\n\n")

            self.lines.append("    @classmethod\n")
            self.lines.append("    def lookup(cls, username):\n")
            self.lines.append("        return cls.query.filter_by(email=username).one_or_none()\n\n")

            self.lines.append("    @classmethod\n")
            self.lines.append("    def identify(cls, id):\n")
            self.lines.append("        return cls.query.get(id)\n\n")

            self.lines.append("    def is_valid(self):\n")
            self.lines.append("        return self.is_active\n\n")

    def create_files(self):
        for model in self.models:
            if ('table_name' in model):
                f = open(f'app/models/{model["table_name"]}.py', 'a')
                self.create_lines(model)
                f.writelines(self.lines)
                f.close()
                f = open('app/models/__init__.py', 'a')
                f.writelines(f'from .{model["table_name"]} import {model["table_name"][0].upper()}{p.singular_noun(model["table_name"][1:])}\n')

    def delete_files(self):
        for model in self.models:
            if ('table_name' in model and os.path.exists(f'app/models/{model["table_name"]}')):
                os.remove(f'app/models/{model["table_name"]}')

model = Model()
model.set_models()
model.delete_files()
model.create_files()
