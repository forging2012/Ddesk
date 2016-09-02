# -*- coding: utf-8 -*-
from . import admin
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from ..forms import AdminDemandForm
from app import config
from datetime import datetime
from ..models import db, Demand, Admin, Tag, Issue
from ..sdk import alidayu


# 初始化SDK
req = alidayu.AlibabaAliqinFcSmsNumSendRequest(config.TAOBAO_API_KEY, config.TAOBAO_API_SECRET,
                                               'https://eco.taobao.com/router/rest')


def sms_demand(phone_number, name, sub, state, category='「需求」'):
    req.sms_type = "normal"
    req.sms_free_sign_name = "一融需求系统"
    req.rec_num = str(phone_number)
    req.sms_param = str({'name': str(name), 'category': category, 'sub': sub, 'state': state})
    req.sms_template_code = "SMS_8140657"
    try:
        resp = req.getResponse()
    except Exception as e:
        print(e)


def sms_demand_a(phone_number, name1, name2, category='「需求」'):
    req.sms_type = "normal"
    req.sms_free_sign_name = "一融需求系统"
    req.rec_num = str(phone_number)
    req.sms_param = str({'name1': name1, 'name2': name2, 'category': category})
    req.sms_template_code = "SMS_12200742"
    try:
        resp = req.getResponse()
    except Exception as e:
        print(e)


@admin.route('/demand')
@login_required
def demand():
    status_code = request.args.get('status')
    if status_code == 'end':
        all_demand = Demand.query.filter(Demand.status > 9).all()
    else:
        all_demand = Demand.query.filter(Demand.status < 10).all()
    return render_template('admin/demand.html', all_demand=all_demand, DEMAND_STATUS=config.DEMAND_STATUS,
                           status_code=status_code, Tag=Tag)


@admin.route('/demand/edit', methods=['GET', 'POST'])
@login_required
def edit_demand():
    this_demand = Demand.query.get(request.args.get('demand_id'))
    type = Tag.query.get(this_demand.type_id)
    try:
        this_issue = Issue.query.get_or_404(this_demand.issues_id)
    except Exception as e:
        if type.id == 47:
            new_issue = Issue(details=this_demand.details, creator_id=current_user.id, extend=str(
                {'category': '', 'tag': [47, this_demand.des_type_id, this_demand.support_id]}), title=this_demand.title)
            db.session.add(new_issue)
            db.session.commit()
            this_demand.issues_id = new_issue.id
            db.session.add(this_demand)
            db.session.commit()
        else:
            new_issue = Issue(details=this_demand.details, creator_id=current_user.id,
                              extend=str({'category': this_demand.category_id, 'tag': [this_demand.type_id, this_demand.audience_id, this_demand.source_id]}),
                              title=this_demand.title)
            db.session.add(new_issue)
            db.session.commit()
            this_issue = new_issue
            this_demand.issues_id = new_issue.id
            db.session.add(this_demand)
            db.session.commit()

    if type.id == 47:
        supports = eval(this_demand.support_id)
        support1 = ''
        support2 = ''
        support3 = ''
        if supports.get(40):
            support1 = '宣传  '
        if supports.get(39):
            support2 = '品牌  '
        if supports.get(38):
            support3 = '设计  '
        support = support1 + support2 + support3
        des_type = Tag.query.get(this_demand.des_type_id)
        form = AdminDemandForm(feedback=this_demand.feedback, status=this_demand.status, title=this_demand.title, p_done_time=this_demand.p_done_time)
        all_admin = Admin.query.all()
        form.assignee.choices = [(admin.id, admin.name) for admin in all_admin]
        if this_demand.assignee_id is None:
            form.assignee.choices.insert(0, (0, '请选择'))
        else:
            form.assignee.choices.remove((this_demand.assignee.id, this_demand.assignee.name))
            form.assignee.choices.insert(0, (this_demand.assignee.id, this_demand.assignee.name))
        if form.validate_on_submit():
            phone_number = this_demand.creator.tel
            name = this_demand.creator.name
            if this_demand.status != form.status.data:
                sms_demand(phone_number=phone_number, name=name, sub=form.title.data,
                       state=config.DEMAND_STATUS[form.status.data])
            if this_demand.assignee_id != form.assignee.data:
                this_admin = Admin.query.get(int(form.assignee.data))
                sms_demand_a(phone_number=this_admin.tel, name1=this_admin.name, name2=name)
            if form.feedback.data:
                this_demand.feedback = form.feedback.data
            if form.p_done_time.data:
                this_demand.p_done_time = form.p_done_time.data
            else:
                this_demand.p_done_time = None
            this_demand.status = form.status.data
            this_demand.title = form.title.data
            this_demand.assignee_id = form.assignee.data
            this_demand.modify_time = datetime.now()
            db.session.add(this_demand)

            issue_status = 10
            if form.status.data < 7:
                issue_status = 20
            elif form.status.data >= 8:
                issue_status = 30

            log = eval(this_issue.log)
            log.append({'date': str(datetime.now()), 'admin': current_user.name, 'data': form.feedback.data})

            extend = eval(this_issue.extend)
            extend['date_due_design'] = str(form.p_done_time.data)

            this_issue.title = form.title.data
            this_issue.feedback = form.feedback.data
            this_issue.assignee_id = form.assignee.data
            this_issue.status = issue_status
            this_issue.extend = str(extend)
            this_issue.log = str(log)
            this_issue.modify_time = datetime.now()
            db.session.add(this_issue)

            db.session.commit()
            flash('需求信息已更新。', 'alert-success')
            return redirect(url_for('.demand'))
        return render_template('admin/demand-edit.html', this_demand=this_demand, DEMAND_STATUS=config.DEMAND_STATUS,
                               form=form, Tag=Tag, type=type.name, support=support, des_type=des_type.name)
    else:
        audience = Tag.query.get(this_demand.audience_id)
        source = Tag.query.get(this_demand.source_id)
        form = AdminDemandForm(feedback=this_demand.feedback, status=this_demand.status, title=this_demand.title, t_done_time=this_demand.t_done_time, p_done_time=this_demand.p_done_time)
        all_admin = Admin.query.all()
        form.assignee.choices = [(admin.id, admin.name) for admin in all_admin]
        if this_demand.assignee_id is None:
            form.assignee.choices.insert(0, (0, '请选择'))
        else:
            form.assignee.choices.remove((this_demand.assignee.id, this_demand.assignee.name))
            form.assignee.choices.insert(0, (this_demand.assignee.id, this_demand.assignee.name))
        if form.validate_on_submit():
            phone_number = this_demand.create_customer.tel
            name = this_demand.create_customer.username
            if this_demand.status != form.status.data:
                sms_demand(phone_number=phone_number, name=name, sub=form.title.data,
                           state=config.DEMAND_STATUS[form.status.data])
            if this_demand.assignee_id != form.assignee.data:
                this_admin = Admin.query.get(int(form.assignee.data))
                sms_demand_a(phone_number=this_admin.tel, name1=this_admin.name, name2=name)
            if form.feedback.data:
                this_demand.feedback = form.feedback.data
            if form.p_done_time.data:
                this_demand.p_done_time = form.p_done_time.data
            else:
                this_demand.p_done_time = None
            if form.t_done_time.data:
                this_demand.t_done_time = form.t_done_time.data
            else:
                this_demand.t_done_time = None
            this_demand.status = form.status.data
            this_demand.title = form.title.data
            this_demand.assignee_id = form.assignee.data
            this_demand.modify_time = datetime.now()
            db.session.add(this_demand)

            issue_status = 10
            if form.status.data < 7:
                issue_status = 20
            elif form.status.data >= 8:
                issue_status = 30

            log = eval(this_issue.log)
            log.append({'date': str(datetime.now()), 'admin': current_user.name, 'data': form.feedback.data})

            extend = eval(this_issue.extend)
            extend['date_due_design'] = str(form.p_done_time.data)
            extend['date_due_online'] = str(form.t_done_time.data)

            this_issue.title = form.title.data
            this_issue.feedback = form.feedback.data
            this_issue.assignee_id = form.assignee.data
            this_issue.status = issue_status
            this_issue.extend = str(extend)
            this_issue.log = str(log)
            this_issue.modify_time = datetime.now()
            db.session.add(this_issue)

            db.session.commit()
            flash('需求信息已更新。', 'alert-success')
            return redirect(url_for('.demand'))
        return render_template('admin/demand-edit.html', this_demand=this_demand, DEMAND_STATUS=config.DEMAND_STATUS,
                               form=form, Tag=Tag, type=type.name, audience=audience.name, source=source.name)
