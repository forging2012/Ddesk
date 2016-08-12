# -*- coding: utf-8 -*-
"""
__author__ = 'duzhipeng'
__mtime__ = '6/7/16'
# code is far away from bugs with the god animal protecting
    I love animals. They taste delicious.
              ┏┓      ┏┓
            ┏┛┻━━━┛┻┓
            ┃      ☃      ┃
            ┃  ┳┛  ┗┳  ┃
            ┃      ┻      ┃
            ┗━┓      ┏━┛
                ┃      ┗━━━┓
                ┃  神兽保佑    ┣┓
                ┃　永无BUG！   ┏┛
                ┗┓┓┏━┳┓┏┛
                  ┃┫┫  ┃┫┫
                  ┗┻┛  ┗┻┛
"""
from . import admin
from flask_login import login_required
from flask import render_template, redirect, url_for, flash
from ..forms import AdminConfigForm
from ..models import db, Config


@admin.route('/config', methods=['GET', 'POST'])
@login_required
def config():
    title = ''
    subtitle = ''
    old_title = Config.query.filter_by(key='title').first()
    old_subtitle = Config.query.filter_by(key='subtitle').first()
    if old_title:
        title = old_title.value
    if old_subtitle:
        subtitle = old_subtitle.value
    form = AdminConfigForm(title=title, subtitle=subtitle)
    if form.validate_on_submit():
        if old_title:
            old_title.value = form.title.data
            db.session.add(old_title)
        else:
            new_title = Config(key='title', value=form.title.data)
            db.session.add(new_title)
        if old_subtitle:
            old_subtitle.value = form.subtitle.data
            db.session.add(old_subtitle)
        else:
            new_subtitle = Config(key='subtitle', value=form.subtitle.data)
            db.session.add(new_subtitle)
        db.session.commit()
        flash('网站基本配置已更新。', 'alert-success')
        return redirect(url_for('.config'))
    return render_template('admin/config.html', form=form)
