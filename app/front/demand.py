# -*- coding: utf-8 -*-
from . import front
from flask import render_template, redirect, url_for
from ..forms import AddDemandForm
from flask.ext.login import login_required, current_user
import upyun
from app import config
from ..models import db, Demand, Category, Config, Tag
from app.sdk import dingtalk
from hashlib import md5
from datetime import datetime


# 初始化SDK
up = upyun.UpYun(config.UPYUN_BUCKET, username=config.UPYUN_USERNAME, password=config.UPYUN_PASSWORD)
ding_msg = dingtalk.DingTalkMsg(config.DINGTALK_API_CID, config.DINGTALK_API_SECRET, config.DINGTALK_API_MSGID)


@front.route('/demand/add', methods=['GET', 'POST'])
@login_required
def add_demand():
    web_title = Config.query.filter_by(key='title').first()
    form = AddDemandForm()
    all_type = Tag.query.filter_by(category_id=10).all()
    all_audience = Tag.query.filter_by(category_id=11).all()
    all_source = Tag.query.filter_by(category_id=12).all()
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
    return render_template('new-demand.html', form=form, page_name='add_demand', web_title=web_title)


