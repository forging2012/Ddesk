# -*- coding: utf-8 -*-
from . import front
from flask import render_template, request, redirect, url_for
from ..forms import AddDemandForm
from flask.ext.login import login_required, current_user
import upyun
from app import config
from datetime import datetime
from werkzeug.utils import secure_filename


up = upyun.UpYun(config.UPYUN_BUCKET, username=config.UPYUN_USERNAME, password=config.UPYUN_PASSWORD)


@front.route('/demand/add', methods=['GET', 'POST'])
@login_required
def add_demand():
    from ..models import db, Demand, Category
    form = AddDemandForm()
    categories = Category.query.filter_by(parents_id=3).all()
    form.category.choices = [(category.id, category.name) for category in categories]
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
                new_demand = Demand(own_customer_id=current_user.id, details=form.details.data,
                                    category_id=form.category.data, attachment=return_info)
        else:
            new_demand = Demand(own_customer_id=current_user.id, details=form.details.data, category_id=form.category.data)
        db.session.add(new_demand)
        db.session.commit()
        return redirect(url_for('.commit_success'))
    return render_template('new-demand.html', form=form, page_name='add_demand')


