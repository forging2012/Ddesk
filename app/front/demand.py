# -*- coding: utf-8 -*-
from . import front
from flask import render_template, request, redirect, url_for
from ..forms import AddDemandForm
from flask.ext.login import login_required, current_user
import upyun
from app import config
from datetime import datetime
from werkzeug.utils import secure_filename
from ..models import db, Demand, Category, Config, Tag


up = upyun.UpYun(config.UPYUN_BUCKET, username=config.UPYUN_USERNAME, password=config.UPYUN_PASSWORD)


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
        if form.attachment.data:
            time = datetime.now()
            time_now = str(time.time())
            data = form.attachment.data
            filename = secure_filename(form.attachment.data.filename)
            key = '/easyrong/' + str(time.year) + '/' + str(time.month) + '/' + str(time.day) + '/' + time_now + '/' + filename
            res = up.put(key, data)
            if res == {}:
                return_info = config.UPYUN_DOMAIN + key
                new_demand = Demand(type_id=form.type.data, audience_id=form.audience.data, source_id=form.source.data,
                                    own_customer_id=current_user.id, details=form.details.data,
                                    category_id=form.category.data, attachment=return_info)
        else:
            new_demand = Demand(type_id=form.type.data, audience_id=form.audience.data, source_id=form.source.data,
                                own_customer_id=current_user.id, details=form.details.data, category_id=form.category.data)
        db.session.add(new_demand)
        db.session.commit()
        return redirect(url_for('.commit_success'))
    return render_template('new-demand.html', form=form, page_name='add_demand', web_title=web_title)


