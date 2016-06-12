# -*- coding: utf-8 -*-
from . import front
from flask import render_template, request, redirect, url_for
from ..forms import AddQuestionForm
from app import config
from datetime import datetime
import upyun
import json
from flask.ext.login import login_required, current_user
from ..models import db, Question, Category, Config


@front.route('/commit/success')
def commit_success():
    web_title = Config.query.filter_by(key='title').first()
    return render_template('commit.html', web_title=web_title)


@front.route('/question/add', methods=['GET', 'POST'])
@login_required
def add_question():
    web_title = Config.query.filter_by(key='title').first()
    form = AddQuestionForm()
    categories = Category.query.filter_by(parents_id=3).all()
    form.category.choices = [(category.id, category.name) for category in categories]
    form.category.choices.insert(0, (0, '请选择产品线'))
    if form.validate_on_submit():
        new_question = Question(own_customer_id=current_user.id, details=form.details.data, category_id=form.category.data)
        db.session.add(new_question)
        db.session.commit()
        return redirect(url_for('.commit_success'))
    return render_template('new-question.html', form=form, page_name='add_question', web_title=web_title)


# 又拍云配置
up = upyun.UpYun(config.UPYUN_BUCKET, username=config.UPYUN_USERNAME, password=config.UPYUN_PASSWORD)


# 直接传图接口
@front.route('/api/upyun', methods=['POST'])
def api_upyun():
    time = datetime.now()
    time_now = str(time.time())
    data = request.files['detail_img']
    key = '/easyrong/' + str(time.year) + '/' + str(time.month) + '/' + str(time.day) + '/' + time_now
    res = up.put(key, data)
    if res['file-type']:
        return_info = {"success": "true", "file_path": config.UPYUN_DOMAIN + key + "_600px"}
    return json.dumps(return_info)
