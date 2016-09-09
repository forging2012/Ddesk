# -*- coding: utf-8 -*-
"""
__author__ = 'Zhipeng Du'
__mtime__ = '16/9/1' '18:27'
"""
from . import back
from flask import redirect, url_for, render_template, request, flash
from flask_login import login_user, logout_user
from ..forms import AdminLoginForm
from app import config
from ..models import User


@back.route('/login', methods=['GET', 'POST'])
def login():
    form = AdminLoginForm()
    if form.validate_on_submit():
        if form.token.data == config.LOGIN_TOKEN:
            user = User.query.filter_by(username=form.username.data).first()
            if user is not None and user.verify_password(form.password.data):
                if user.admin:
                    login_user(user)
                else:
                    flash('您没有权限。', 'is-danger')
                return redirect(request.args.get('next') or url_for('admin.index'))
            else:
                flash('用户名或密码错误，请重新输入。', 'is-danger')
        else:
            flash('密令不正确。', 'is-danger')
    return render_template('back/login.html', form=form)


@back.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('.login'))
