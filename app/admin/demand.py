# -*- coding: utf-8 -*-
from . import admin
from flask import render_template, request, redirect, url_for, flash
from flask.ext.login import login_required
from ..forms import AdminDemandForm
from app import config
from datetime import datetime
from ..models import db, Demand, Admin, Tag


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
    audience = Tag.query.get(this_demand.audience_id)
    source = Tag.query.get(this_demand.source_id)
    form = AdminDemandForm(feedback=this_demand.feedback, status=this_demand.status, title=this_demand.title)
    all_admin = Admin.query.all()
    form.assignee.choices = [(admin.id, admin.name) for admin in all_admin]
    if this_demand.assignee_id is None:
        form.assignee.choices.insert(0, (0, '请选择'))
    else:
        form.assignee.choices.remove((this_demand.assignee.id, this_demand.assignee.name))
        form.assignee.choices.insert(0, (this_demand.assignee.id, this_demand.assignee.name))
    if form.validate_on_submit():
        if form.feedback.data:
            this_demand.feedback = form.feedback.data
        this_demand.status = form.status.data
        this_demand.title = form.title.data
        this_demand.assignee_id = form.assignee.data
        this_demand.modify_time = datetime.now()
        db.session.add(this_demand)
        db.session.commit()
        flash('需求信息已更新。', 'alert-success')
        return redirect(url_for('.demand'))
    return render_template('admin/demand-edit.html', this_demand=this_demand, DEMAND_STATUS=config.DEMAND_STATUS,
                           form=form, Tag=Tag, type=type.name, audience=audience.name, source=source.name)
