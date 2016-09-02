# -*- coding: utf-8 -*-
"""
__author__ = 'Zhipeng Du'
__mtime__ = '8/31/16'
"""
from . import back
from flask_login import login_required
from flask import render_template, redirect, url_for, flash
from ..forms import AppConfigForm
from ..models import db, Config


@back.route('/config', methods=['GET', 'POST'])
@login_required
def config():
    old_title = Config.query.filter_by(key='title').first()
    old_subtitle = Config.query.filter_by(key='subtitle').first()
    title = old_title if old_title is not None else ''
    subtitle = old_subtitle if old_subtitle is not None else ''
    form = AppConfigForm(title=title.value, subtitle=subtitle.value)
    if form.validate_on_submit():
        if old_title is None:
            title = Config(key='title', value=form.title.data)
            subtitle = Config(key='subtitle', value=form.subtitle.data)
        else:
            title.value = form.title.data
            subtitle.value = form.subtitle.data
        db.session.add(title)
        db.session.add(subtitle)
        db.session.commit()
        flash('网站设置已更新。', 'is-success')
        return redirect(url_for('.config'))
    return render_template('back/editConfig.html', form=form)
