import json
import os

from flask import Flask, Response, redirect
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.peewee import ModelView
from flask_admin.form import JSONField
from flask_basicauth import BasicAuth
from jinja2 import Markup
from werkzeug.exceptions import HTTPException

from task_2 import models

app = Flask(__name__)

app.config['FLASK_ADMIN_SWATCH'] = 'flatly'
app.config['SECRET_KEY'] = b'secret'
app.config['BASIC_AUTH_USERNAME'] = 'admin'
app.config['BASIC_AUTH_PASSWORD'] = 'admin'
app.config['BASIC_AUTH_FORCE'] = True

# Add administrative views here
basic_auth = BasicAuth(app)


class AuthException(HTTPException):
    def __init__(self, message):
        super().__init__(message, Response(
            "You could not be authenticated. Please refresh the page.", 401,
            {'WWW-Authenticate': 'Basic realm="Login Required"'}))


def json_formatter(view, context, model, name):
    value = getattr(model, name)
    json_value = json.dumps(value, ensure_ascii=False, indent=2)
    return Markup('<pre>{}</pre>'.format(json_value))


class JSONField2(JSONField):
    def _value(self):
        if self.raw_data:
            return self.raw_data[0]
        elif self.data:
            return json.dumps(self.data, ensure_ascii=False, indent=2)
        else:
            return '{}'


class MyModelView(ModelView):
    form_overrides = {
        'extra': JSONField2,
        'kwargs': JSONField2,
        'pending_tasks': JSONField2,
        'extremum': JSONField2,
        'encoding': JSONField2,
        'stop_cond': JSONField2,
        'action_log': JSONField2,
    }
    column_formatters = {
        'extra': json_formatter,
        'kwargs': json_formatter,
        'pending_tasks': json_formatter,
        'extremum': json_formatter,
        'encoding': json_formatter,
        'stop_cond': json_formatter,
        'action_log': json_formatter,
    }

    def is_accessible(self):
        if not basic_auth.authenticate():
            raise AuthException('Not authenticated.')
        else:
            return True

    def inaccessible_callback(self, name, **kwargs):
        return redirect(basic_auth.challenge())


class MyAdminIndexView(AdminIndexView):

    def is_accessible(self):
        if not basic_auth.authenticate():
            raise AuthException('Not authenticated.')
        else:
            return True

    def inaccessible_callback(self, name, **kwargs):
        return redirect(basic_auth.challenge())


admin = Admin(app, name='GenAlgo', template_mode='bootstrap3', index_view=MyAdminIndexView())

admin.add_view(MyModelView(models.Log))
admin.add_view(MyModelView(models.Task))
admin.add_view(MyModelView(models.ParamSet))

app.run(host='0.0.0.0', port=os.environ.get('PORT', '1249'))
