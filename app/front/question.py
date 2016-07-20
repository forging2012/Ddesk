# -*- coding: utf-8 -*-
from . import front
from flask import render_template, request, redirect, url_for
from ..forms import AddQuestionForm
from app import config
import upyun
import json
from flask.ext.login import login_required, current_user
from ..models import db, Question, Category, Config
from app.sdk import dingtalk
from hashlib import md5
from datetime import datetime


ding_msg = dingtalk.DingTalkMsg(config.DINGTALK_API_CID, config.DINGTALK_API_SECRET, config.DINGTALK_API_MSGID)


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
        text = str(current_user.id) + str(datetime.now())
        m = md5()
        m.update(text.encode('utf-8'))
        id_hash = m.hexdigest()
        new_question = Question(own_customer_id=current_user.id, details=form.details.data, category_id=form.category.data,
                                id_hash=id_hash)
        db.session.add(new_question)
        db.session.commit()
        this_question = Question.query.filter_by(id_hash=id_hash).first()
        url = 'http://chanpin.xinlonghang.cn/admin/question/edit?question_id=' + str(this_question.id)
        data = {'create_customer': this_question.create_customer.username, 'category': this_question.category.name,
                'num': this_question.id}
        ding_msg.msg(category=1, url=url, data=data)
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
