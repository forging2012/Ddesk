# -*- coding: utf-8 -*-
from config import load_config
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

app = Flask(__name__)
config = load_config()
app.config.from_object(config)

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.session_protection = 'strong'
login_manager.login_view = '.login'
login_manager.login_message = '请先登录再操作。'
login_manager.login_message_category = 'alert-danger is-danger'


# login回调函数
@login_manager.user_loader
def load_user(user_id):
    from .models import Customer, Admin
    return Customer.query.get(int(user_id)) or Admin.query.get(int(user_id))


from .front import front
from .admin import admin
app.register_blueprint(front)
app.register_blueprint(admin, url_prefix='/admin')
