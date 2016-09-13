# -*- coding: utf-8 -*-
"""
__author__ = 'Zhipeng Du'
__mtime__ = '16/9/6' '14:11'
"""
from . import back
from flask_login import login_required, current_user
from flask import render_template, redirect, url_for, flash, request
from ..models import db, User, Tag, Issue, Category
from app import config, alidayu
from ..forms import DemandIssueForm
from datetime import datetime


@back.route('/demand')
@login_required
def demand():
    status_code = request.args.get('status')
    if status_code == '30':
        if current_user.super_admin:
            all_demand = Issue.query.filter_by(status=30).all()
        else:
            all_demand = Issue.query.filter_by(status=30, assignee_id=current_user.id).all()
    else:
        if current_user.super_admin:
            all_demand = Issue.query.filter(Issue.status != 30).all()
        else:
            all_demand = Issue.query.filter(Issue.status != 30, Issue.assignee_id == current_user.id).all()
    datas = []
    for item in all_demand:
        extend = eval(item.extend)
        assignee_name = item.assignee.name if item.assignee_id is not None else ''
        if extend['class_id'] != 1:
            item_dict = {'id': item.id, 'title': item.title, 'status': config.ISSUE_STATUS[item.status],
                         'create_time': item.create_time,
                         'creator': {'name': item.creator.name, 'tel': item.creator.tel},
                         'assignee': {'name': assignee_name}}
            datas.append(item_dict)
    return render_template('back/demand.html', datas=datas, status_code=status_code)


@back.route('/demand/edit', methods=['GET', 'POST'])
@login_required
def edit_demand():
    this_issue = Issue.query.get_or_404(request.args.get('id'))
    all_admin = User.query.filter_by(admin=True).all()
    extend = eval(this_issue.extend)
    datas = {'id': this_issue.id, 'status': config.ISSUE_STATUS[this_issue.status], 'title': this_issue.title,
             'creator': {'name': this_issue.creator.name, 'tel': this_issue.creator.tel},
             'create_time': this_issue.create_time, 'details': this_issue.details, 'class_id': extend['class_id']}
    if extend['class_id'] == 2:
        supports = extend['support_id']
        support1 = ''
        support2 = ''
        support3 = ''
        if supports.get(40):
            support1 = '宣传  '
        if supports.get(39):
            support2 = '品牌  '
        if supports.get(38):
            support3 = '设计  '
        datas['support'] = support1 + support2 + support3
        des_type = Tag.query.get(extend['des_type_id'])
        datas['des_type_name'] = des_type.name
        form = DemandIssueForm(feedback=this_issue.feedback, status=this_issue.status,
                               title=this_issue.title, design_done_time=extend.get('design_done_time'))
        form.assignee.choices = [(admin.id, admin.name) for admin in all_admin]
        if this_issue.assignee_id is None:
            form.assignee.choices.insert(0, (0, '请选择'))
        else:
            form.assignee.choices.remove((this_issue.assignee.id, this_issue.assignee.name))
            form.assignee.choices.insert(0, (this_issue.assignee.id, this_issue.assignee.name))
        if form.validate_on_submit():
            phone_number = this_issue.creator.tel
            name = this_issue.creator.name
            if form.design_done_time.data is not None and extend.get('design_done_time') != form.design_done_time.data:
                alidayu.send_sms(phone_number, "SMS_8140657",
                                 {'name': str(name), 'category': '需求',
                                  'sub': '预计' + str(form.design_done_time.data) + '前处理完毕。目前状态：',
                                  'state': config.ISSUE_STATUS[form.status.data]})
            if this_issue.assignee_id != form.assignee.data:
                this_admin = User.query.get(int(form.assignee.data))
                alidayu.send_sms(this_admin.tel, "SMS_12200742",
                                 {'name1': this_admin.name, 'name2': name, 'category': '需求'})

            log = eval(this_issue.log)
            log.append({'date': str(datetime.now()), 'admin': current_user.name, 'data': form.feedback.data})
            this_issue.log = str(log)
            extend = eval(this_issue.extend)
            extend['design_done_time'] = str(form.design_done_time.data)
            this_issue.extend = str(extend)
            this_issue.feedback = form.feedback.data
            this_issue.assignee_id = form.assignee.data
            this_issue.status = form.status.data
            this_issue.title = form.title.data
            this_issue.modify_time = datetime.now()
            db.session.add(this_issue)
            db.session.commit()
            flash('工单信息已成功更新。', 'is-success')
            if request.args.get('type') != 'html5':
                return redirect(url_for('.demand'))
        if request.args.get('type') == 'html5':
            return render_template('back/demandEditH5.html', datas=datas, form=form)
        else:
            return render_template('back/demandEdit.html', datas=datas, form=form)
    else:
        audience = Tag.query.get(extend['audience_id'])
        source = Tag.query.get(extend['source_id'])
        d_type = Tag.query.get(extend['type_id'])
        category = Category.query.get(extend['category_id'])
        datas['audience_name'] = audience.name
        datas['source'] = source.name
        datas['type'] = d_type.name
        datas['category'] = category.name
        form = DemandIssueForm(feedback=this_issue.feedback, status=this_issue.status, title=this_issue.title,
                               design_done_time=extend.get('design_done_time'),
                               online_time=extend.get('online_time'))
        form.assignee.choices = [(admin.id, admin.name) for admin in all_admin]
        if this_issue.assignee_id is None:
            form.assignee.choices.insert(0, (0, '请选择'))
        else:
            form.assignee.choices.remove((this_issue.assignee.id, this_issue.assignee.name))
            form.assignee.choices.insert(0, (this_issue.assignee.id, this_issue.assignee.name))
        if form.validate_on_submit():
            phone_number = this_issue.creator.tel
            name = this_issue.creator.name
            if form.design_done_time.data is not None and extend.get('design_done_time') != form.design_done_time.data:
                alidayu.send_sms(phone_number, "SMS_8140657",
                                 {'name': str(name), 'category': '需求',
                                  'sub': '预计' + str(form.design_done_time.data) + '前产品设计处理完毕。目前状态：',
                                  'state': config.ISSUE_STATUS[form.status.data]})
            if form.online_time.data is not None and extend.get('online_time') != form.online_time.data:
                alidayu.send_sms(phone_number, "SMS_8140657",
                                 {'name': str(name), 'category': '需求',
                                  'sub': '预计' + str(form.online_time.data) + '左右上线。目前状态：',
                                  'state': config.ISSUE_STATUS[form.status.data]})
            if this_issue.assignee_id != form.assignee.data:
                this_admin = User.query.get(int(form.assignee.data))
                alidayu.send_sms(this_admin.tel, "SMS_12200742",
                                 {'name1': this_admin.name, 'name2': name, 'category': '需求'})

            log = eval(this_issue.log)
            log.append({'date': str(datetime.now()), 'admin': current_user.name, 'data': form.feedback.data})
            this_issue.log = str(log)
            extend = eval(this_issue.extend)
            extend['design_done_time'] = str(form.design_done_time.data)
            extend['online_time'] = str(form.online_time.data)
            this_issue.extend = str(extend)
            this_issue.feedback = form.feedback.data
            this_issue.assignee_id = form.assignee.data
            this_issue.status = form.status.data
            this_issue.title = form.title.data
            this_issue.modify_time = datetime.now()
            db.session.add(this_issue)
            db.session.commit()
            flash('工单信息已成功更新。', 'is-success')
            if request.args.get('type') != 'html5':
                return redirect(url_for('.demand'))
        if request.args.get('type') == 'html5':
            return render_template('back/demandEditH5.html', datas=datas, form=form)
        else:
            return render_template('back/demandEdit.html', datas=datas, form=form)
