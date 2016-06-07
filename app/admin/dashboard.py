# -*- coding: utf-8 -*-
from . import admin
from flask import render_template, redirect, url_for
from flask.ext.login import login_required


@admin.route('/')
@login_required
def index():
    return redirect(url_for('.dashboard'))


@admin.route('/dashboard')
@login_required
def dashboard():
    from ..models import Question, Demand, Customer
    count_question = Question.query.filter(Question.status < 3).count()
    count_demand = Demand.query.filter(Demand.status < 10).count()
    count_customer = Customer.query.count()
    return render_template('admin/dashboard.html', count_question=count_question, count_demand=count_demand,
                           count_customer=count_customer)