# -*- coding: utf-8 -*-
from . import admin
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from ..forms import AdminQuestionForm
from app import config
import json
import upyun
from ..sdk import alidayu
from datetime import datetime


req2 = alidayu.AlibabaAliqinFcSmsNumSendRequest(config.TAOBAO_API_KEY, config.TAOBAO_API_SECRET,
                                               'https://eco.taobao.com/router/rest')


def sms_question(phone_number, name, sub, state, category='「问题」'):
    req2.sms_type = "normal"
    req2.sms_free_sign_name = "一融需求系统"
    req2.rec_num = str(phone_number)
    req2.sms_param = str({'name': str(name), 'category': category, 'sub': sub, 'state': state})
    req2.sms_template_code = "SMS_8140657"
    try:
        resp = req2.getResponse()
    except Exception as e:
        return e


def sms_question_a(phone_number, name1, name2, category='「问题」'):
    req2.sms_type = "normal"
    req2.sms_free_sign_name = "一融需求系统"
    req2.rec_num = str(phone_number)
    req2.sms_param = str({'name1': name1, 'name2': name2, 'category': category})
    req2.sms_template_code = "SMS_12200742"
    try:
        resp = req2.getResponse()
    except Exception as e:
        return e


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
    from ..models import db, Question, Admin, Issue
    this_question = Question.query.get_or_404(request.args.get('question_id'))
    try:
        this_issue = Issue.query.get_or_404(this_question.issues_id)
    except Exception as e:
        new_issue = Issue(details=this_question.details, creator_id=current_user.id, extend=str({'category': this_question.category_id}))
        db.session.add(new_issue)
        db.session.commit()
        this_issue = new_issue
    form = AdminQuestionForm(feedback=this_question.feedback, status=this_question.status, title=this_question.title)
    all_admin = Admin.query.all()
    form.assignee.choices = [(admin.id, admin.name) for admin in all_admin]
    if this_question.assignee_id is None:
        form.assignee.choices.insert(0, (0, '请选择'))
    else:
        form.assignee.choices.remove((this_question.assignee.id, this_question.assignee.name))
        form.assignee.choices.insert(0, (this_question.assignee.id, this_question.assignee.name))
    if form.validate_on_submit():
        phone_number = this_question.creator.tel
        name = this_question.creator.name
        if this_question.status != form.status.data:
            sms_question(phone_number=phone_number, name=name, sub=form.title.data,
                         state=config.QUESTION_STATUS[form.status.data])
        if this_question.assignee_id != form.assignee.data:
            this_admin = Admin.query.get(int(form.assignee.data))
            sms_question_a(phone_number=this_admin.tel, name1=this_admin.name, name2=name)
        this_question.feedback = form.feedback.data
        this_question.status = form.status.data
        this_question.title = form.title.data
        this_question.assignee_id = form.assignee.data
        this_question.modify_time = datetime.now()
        db.session.add(this_question)

        issue_status = 10
        if form.status.data == 2:
            issue_status = 20
        elif form.status.data == 3:
            issue_status = 30

        log = eval(this_issue.log)
        log.append({'date': str(datetime.now()), 'admin': current_user.name, 'data': form.feedback.data})

        this_issue.title = form.title.data
        this_issue.feedback = form.feedback.data
        this_issue.assignee_id = form.assignee.data
        this_issue.status = issue_status
        this_issue.log = str(log)
        this_issue.modify_time = datetime.now()
        db.session.add(this_issue)

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

