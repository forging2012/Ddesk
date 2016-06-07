# -*- coding: utf-8 -*-
from . import admin
from app.forms import AdminCustomerForm
from flask import render_template, redirect, url_for, flash, request
from flask.ext.login import login_required
from ..models import db, Customer


@admin.route('/customer')
@login_required
def customer():
    from ..models import Customer
    all_customer = Customer.query.all()
    return render_template('admin/customer.html', all_customer=all_customer)


@admin.route('/customer/add', methods=['GET', 'POST'])
@login_required
def add_customer():
    form = AdminCustomerForm()
    if form.validate_on_submit():
        new_customer = Customer(username=form.username.data, tel=form.tel.data)
        db.session.add(new_customer)
        db.session.commit()
        flash('添加用户成功。', 'alert-success')
        return redirect(url_for('.customer'))
    return render_template('admin/customer-add.html', form=form)


@admin.route('/customer/edit', methods=['GET', 'POST'])
@login_required
def edit_customer():
    this_customer = Customer.query.get_or_404(request.args.get('customer_id'))
    form = AdminCustomerForm(username=this_customer.username, tel=this_customer.tel)
    if form.validate_on_submit():
        this_customer.username = form.username.data
        this_customer.tel = form.tel.data
        db.session.add(this_customer)
        db.session.commit()
        flash('更新用户信息成功。', 'alert-success')
        return redirect(url_for('.customer'))
    return render_template('admin/customer-edit.html', form=form)

