# -*- coding: utf-8 -*-
from config import load_config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from app.sdk import dingtalk as dingtalk1
from app.modules import dingtalk
import upyun

app = Flask(__name__)
config = load_config()
app.config.from_object(config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager(app)
login_manager.session_protection = 'strong'
login_manager.login_view = '.login'
login_manager.login_message = '请先登录再操作。'
login_manager.login_message_category = 'alert-danger is-danger'


# 钉钉
ding_msg = dingtalk1.DingTalkMsg(config.DINGTALK_API_CID, config.DINGTALK_API_SECRET, config.DINGTALK_API_MSGID)
ding = dingtalk.DingTalk(config.DINGTALK_API_CID, config.DINGTALK_API_SECRET, config.DINGTALK_API_MSGID)
# 又拍云
up = upyun.UpYun(config.UPYUN_BUCKET, username=config.UPYUN_USERNAME, password=config.UPYUN_PASSWORD)


# login回调函数
@login_manager.user_loader
def load_user(user_id):
    from .models import User, Admin
    return User.query.get(int(user_id)) or Admin.query.get(int(user_id))


from .front import front
from .admin import admin
from .back import back
app.register_blueprint(front)
app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(back, url_prefix='/back')

