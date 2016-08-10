# -*- coding: utf-8 -*-
from . import front
from flask import render_template, request, redirect, url_for, flash
from ..forms import LoginForm
from flask_login import login_user
from ..models import Customer, Config


@front.route('/login', methods=['GET', 'POST'])
def login():
    web_title = ''
    web_subtitle = ''
    old_title = Config.query.filter_by(key='title').first()
    old_subtitle = Config.query.filter_by(key='subtitle').first()
    if old_title:
        web_title = old_title.value
    if old_subtitle:
        web_subtitle = old_subtitle.value
    form = LoginForm()
    if form.validate_on_submit():
        user = Customer.query.filter_by(username=form.username.data, tel=form.tel.data).first()
        if user is not None:
            login_user(user)
            return redirect(request.args.get('next') or url_for('.index'))
        else:
            flash('姓名或手机错误，请重新输入。', 'is-danger')
    return render_template('login.html', form=form, web_title=web_title, web_subtitle=web_subtitle)