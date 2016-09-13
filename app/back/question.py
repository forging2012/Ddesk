# -*- coding: utf-8 -*-
"""
__author__ = 'Zhipeng Du'
__mtime__ = '16/9/5' '15:06'
"""
from . import back
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from ..forms import QuestionIssueForm
from app import config, alidayu
from datetime import datetime
from ..models import db, Issue, Category, User


@back.route('/question')
@login_required
def question():
    status_code = request.args.get('status')
    if status_code == '30':
        if current_user.super_admin:
            all_question = Issue.query.filter_by(status=30).all()
        else:
            all_question = Issue.query.filter_by(status=30, assignee_id=current_user.id).all()
    else:
        if current_user.super_admin:
            all_question = Issue.query.filter(Issue.status != 30).all()
        else:
            all_question = Issue.query.filter(Issue.status != 30, Issue.assignee_id == current_user.id).all()
    datas = []
    for item in all_question:
        extend = eval(item.extend)
        this_category_name = '没有指定'
        assignee_name = item.assignee.name if item.assignee_id is not None else ''
        if extend['class_id'] == 1:
            category_id = extend['category_id']
            if category_id:
                this_category = Category.query.get(category_id)
                this_category_name = this_category.name
            item_dict = {'id': item.id, 'title': item.title, 'status': config.ISSUE_STATUS[item.status],
                         'category_name': this_category_name, 'create_time': item.create_time,
                         'creator': {'name': item.creator.name, 'tel': item.creator.tel},
                         'assignee': {'name': assignee_name}}
            datas.append(item_dict)
    return render_template('back/question.html', datas=datas, status_code=status_code)


@back.route('/question/edit', methods=['GET', 'POST'])
@login_required
def edit_question():
    this_issue = Issue.query.get_or_404(request.args.get('id'))
    extend = eval(this_issue.extend)
    this_category_name = '没有指定'
    if extend['class_id'] == 1:
        category_id = extend['category_id']
        if category_id:
            this_category = Category.query.get(category_id)
            this_category_name = this_category.name
    datas = {'id': this_issue.id, 'status': config.ISSUE_STATUS[this_issue.status], 'title': this_issue.title,
             'creator': {'name': this_issue.creator.name, 'tel': this_issue.creator.tel},
             'category_name': this_category_name, 'create_time': this_issue.create_time, 'details': this_issue.details}
    form = QuestionIssueForm(feedback=this_issue.feedback, status=this_issue.status, title=this_issue.title)
    all_admin = User.query.filter_by(admin=True).all()
    form.assignee.choices = [(admin.id, admin.name) for admin in all_admin]
    if this_issue.assignee_id is None:
        form.assignee.choices.insert(0, (0, '请选择'))
    else:
        form.assignee.choices.remove((this_issue.assignee.id, this_issue.assignee.name))
        form.assignee.choices.insert(0, (this_issue.assignee.id, this_issue.assignee.name))
    if form.validate_on_submit():
        phone_number = this_issue.creator.tel
        name = this_issue.creator.name
        # 发短信
        if this_issue.status != form.status.data:
            alidayu.send_sms(phone_number, "SMS_8140657",
                             {'name': str(name), 'category': '问题', 'sub': form.title.data,
                              'state': config.ISSUE_STATUS[form.status.data]})
        if this_issue.assignee_id != form.assignee.data:
            this_admin = User.query.get(int(form.assignee.data))
            alidayu.send_sms(this_admin.tel, "SMS_12200742",
                             {'name1': this_admin.name, 'name2': name, 'category': '问题'})
        # 更新工单数据
        log = eval(this_issue.log)
        log.append({'date': str(datetime.now()), 'admin': current_user.name, 'data': form.feedback.data})
        this_issue.log = str(log)
        this_issue.feedback = form.feedback.data
        this_issue.status = form.status.data
        this_issue.title = form.title.data
        this_issue.assignee_id = form.assignee.data
        this_issue.modify_time = datetime.now()
        db.session.add(this_issue)
        db.session.commit()
        flash('工单信息已成功更新。', 'is-success')
        if request.args.get('type') != 'html5':
            return redirect(url_for('.question'))
    if request.args.get('type') == 'html5':
        return render_template('back/questionEditH5.html', datas=datas, form=form)
    else:
        return render_template('back/questionEdit.html', datas=datas, form=form)
