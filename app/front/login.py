# -*- coding: utf-8 -*-
from . import front
from flask import render_template, request, redirect, url_for
from ..forms import LoginForm
from flask.ext.login import  login_user


@front.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    from ..models import Customer
    if form.validate_on_submit():
        user = Customer.query.filter_by(username=form.username.data, tel=form.tel.data).first()
        if user is not None:
            login_user(user)
            return redirect(request.args.get('next') or url_for('.index'))
    return render_template('login.html', form=form)