# -*- coding: utf-8 -*-
from app import app
from . import admin
from flask import render_template, redirect, url_for, send_from_directory, request
from flask_login import login_required


@admin.route('/')
@login_required
def index():
    return redirect(url_for('.dashboard'))


@admin.route('/dashboard')
@login_required
def dashboard():
    from ..models import Demand, Customer
    count_demand = Demand.query.filter(Demand.status < 10).count()
    count_customer = Customer.query.count()
    return render_template('admin/dashboard.html', count_question='', count_demand=count_demand,
                           count_customer=count_customer)


@admin.route('/robots.txt')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])