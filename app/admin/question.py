# -*- coding: utf-8 -*-
from . import admin
from flask import render_template, request, redirect, url_for, flash
from flask.ext.login import login_required
from ..forms import AdminQuestionForm
from app import config
import json
from datetime import datetime
import upyun


@admin.route('/question')
@login_required
def question():
    from ..models import Question
    status_code = request.args.get('status')
    if status_code == '3':
        all_question = Question.query.filter_by(status=3).all()
    else:
        all_question = Question.query.filter(Question.status != 3).all()
    return render_template('admin/question.html', all_question=all_question, QUESTION_STATUS=config.QUESTION_STATUS,
                           status_code=status_code)


@admin.route('/question/edit', methods=['GET', 'POST'])
@login_required
def edit_question():
    from ..models import db, Question, Admin
    this_question = Question.query.get_or_404(request.args.get('question_id'))
    form = AdminQuestionForm(feedback=this_question.feedback, status=this_question.status)
    all_admin = Admin.query.all()
    form.assignee.choices = [(admin.id, admin.name) for admin in all_admin]
    if this_question.assignee_id is None:
        form.assignee.choices.insert(0, (0, '请选择'))
    else:
        form.assignee.choices.remove((this_question.assignee.id, this_question.assignee.name))
        form.assignee.choices.insert(0, (this_question.assignee.id, this_question.assignee.name))
    if form.validate_on_submit():
        this_question.feedback = form.feedback.data
        this_question.status = form.status.data
        this_question.title = form.title.data
        this_question.assignee_id = form.assignee.data
        this_question.modify_time = datetime.now()
        db.session.add(this_question)
        db.session.commit()
        flash('问题信息已更新。', 'alert-success')
        return redirect(url_for('.question'))
    return render_template('admin/question-edit.html', this_question=this_question, QUESTION_STATUS=config.QUESTION_STATUS,
                           form=form)


# 又拍云配置
up = upyun.UpYun(config.UPYUN_BUCKET, username=config.UPYUN_USERNAME, password=config.UPYUN_PASSWORD)


# 直接传图接口
@admin.route('/api/upyun', methods=['POST'])
@login_required
def api_upyun():
    time = datetime.now()
    time_now = str(time.time())
    data = request.files['detail_img']
    key = '/easyrong/' + str(time.year) + '/' + str(time.month) + '/' + str(time.day) + '/' + time_now
    res = up.put(key, data)
    if res['file-type']:
        return_info = {"success": "true", "file_path": config.UPYUN_DOMAIN + key + "_600px"}
    return json.dumps(return_info)

