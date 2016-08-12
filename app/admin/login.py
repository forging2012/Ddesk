# -*- coding: utf-8 -*-
from app.forms import AdminLoginForm
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user
from . import admin
from app import config


@admin.route('/login', methods=['get', 'post'])
def login():
    from ..models import Admin
    form = AdminLoginForm()
    if form.validate_on_submit():
        if form.key.data == config.LOGIN_TOKEN:
            user = Admin.query.filter_by(username=form.username.data).first()
            if user is not None and user.verify_password(form.password.data):
                login_user(user)
                return redirect(request.args.get('next') or url_for('.index'))
            else:
                flash('用户名或密码错误，请重新输入。', 'alert-danger')
        else:
            flash('密令不正确。', 'alert-danger')
    return render_template('admin/login.html', form=form)


@admin.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('.login'))


