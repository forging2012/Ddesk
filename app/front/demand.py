# -*- coding: utf-8 -*-
from . import front
from flask import render_template, redirect, url_for, request
from ..forms import AddProDemandForm, AddDesDemandForm
from flask_login import login_required, current_user
from app import ding_msg
from ..models import db, Demand, Category, Config, Tag
from hashlib import md5
from datetime import datetime


@front.route('/demand/add', methods=['GET', 'POST'])
@login_required
def add_demand():
    web_title = ''
    web_subtitle = ''
    old_title = Config.query.filter_by(key='title').first()
    old_subtitle = Config.query.filter_by(key='subtitle').first()
    if old_title:
        web_title = old_title.value
    if old_subtitle:
        web_subtitle = old_subtitle.value
    if request.args.get('c') == 'p':
        form = AddProDemandForm()
        all_type = Tag.query.filter_by(category_id=10, status=1).all()
        all_audience = Tag.query.filter_by(category_id=11, status=1).all()
        all_source = Tag.query.filter_by(category_id=12, status=1).all()
        categories = Category.query.filter_by(parents_id=3).all()
        form.type.choices = [(tag.id, tag.name) for tag in all_type]
        form.audience.choices = [(tag.id, tag.name) for tag in all_audience]
        form.source.choices = [(tag.id, tag.name) for tag in all_source]
        form.category.choices = [(category.id, category.name) for category in categories]
        form.type.choices.insert(0, (0, '请选择需求类型'))
        form.audience.choices.insert(0, (0, '请选择受众范围'))
        form.source.choices.insert(0, (0, '请选择需求来源'))
        form.category.choices.insert(0, (0, '请选择产品线'))
        if form.validate_on_submit():
            text = str(current_user.id) + str(datetime.now())
            m = md5()
            m.update(text.encode('utf-8'))
            id_hash = m.hexdigest()
            new_demand = Demand(type_id=form.type.data, audience_id=form.audience.data, source_id=form.source.data,
                                own_customer_id=current_user.id, details=form.details.data, category_id=form.category.data,
                                id_hash=id_hash)
            db.session.add(new_demand)
            db.session.commit()
            this_demand = Demand.query.filter_by(id_hash=id_hash).first()
            type = Tag.query.get(this_demand.type_id)
            audience = Tag.query.get(this_demand.audience_id)
            source = Tag.query.get(this_demand.source_id)
            url = 'http://chanpin.xinlonghang.cn/admin/demand/edit?demand_id=' + str(this_demand.id)
            data = {'create_customer': this_demand.create_customer.username, 'num': this_demand.id,
                    'type': type.name, 'audience': audience.name, 'source': source.name, 'category': this_demand.category.name}
            ding_msg.msg(category=2, url=url, data=data)
            return redirect(url_for('.commit_success'))
        return render_template('new-demand-p.html', form=form,  web_title=web_title, web_subtitle=web_subtitle)
    elif request.args.get('c') == 'd':
        form = AddDesDemandForm()
        all_des_type = Tag.query.filter_by(category_id=20, status=1).all()
        form.des_type.choices = [(tag.id, tag.name) for tag in all_des_type]
        form.des_type.choices.insert(0, (0, '请选择设计类型'))
        if form.validate_on_submit():
            text = str(current_user.id) + str(datetime.now())
            m = md5()
            m.update(text.encode('utf-8'))
            id_hash = m.hexdigest()
            support_id = {40: form.support1.data, 39: form.support2.data, 38: form.support3.data}
            new_demand = Demand(type_id=47, support_id=str(support_id), des_type_id=form.des_type.data,
                                own_customer_id=current_user.id, details=form.details.data,
                                id_hash=id_hash)
            db.session.add(new_demand)
            db.session.commit()
            this_demand = Demand.query.filter_by(id_hash=id_hash).first()
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
            url = 'http://chanpin.xinlonghang.cn/admin/demand/edit?demand_id=' + str(this_demand.id)
            data = {'create_customer': this_demand.create_customer.username, 'num': this_demand.id,
                    'type': '设计需求', 'support': support, 'des_type': des_type.name}
            ding_msg.msg(category=3, url=url, data=data)
            return redirect(url_for('.commit_success'))
        return render_template('new-demand-d.html', form=form, web_title=web_title, web_subtitle=web_subtitle)

