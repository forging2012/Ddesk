# -*- coding: utf-8 -*-
"""
__author__ = 'Zhipeng Du'
__mtime__ = '16/9/1' '18:27'
"""
from . import front
from flask import render_template, request, redirect, url_for, flash
from ..forms import UserLoginForm
from flask_login import login_user, logout_user
from ..models import User, Config


@front.route('/login', methods=['GET', 'POST'])
def login():
    old_title = Config.query.filter_by(key='title').first()
    old_subtitle = Config.query.filter_by(key='subtitle').first()
    web_title = old_title.value if old_title else ''
    web_subtitle = old_subtitle.value if old_subtitle else ''
    form = UserLoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.name.data, tel=form.tel.data).first()
        if user is not None:
            login_user(user)
            return redirect(request.args.get('next') or url_for('.index'))
        else:
            flash('姓名或手机错误，请重新输入。', 'is-danger')
    return render_template('login.html', form=form, web_title=web_title, web_subtitle=web_subtitle)


@front.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('.login'))