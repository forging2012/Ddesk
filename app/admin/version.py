# -*- coding: utf-8 -*-
from . import admin
from app.forms import AdminVersionForm
from flask import render_template, redirect, flash, url_for, request
from flask_login import login_required


@admin.route('/version')
@login_required
def version():
    from ..models import Version
    all_version = Version.query.all()
    return render_template('admin/version.html', all_version=all_version)


@admin.route('/version/add', methods=['GET', 'POST'])
@login_required
def add_version():
    from ..models import db, Version, Category
    form = AdminVersionForm()
    form_pro_line_choice = []
    category_line = Category.query.filter_by(parents_id=3).all()
    for category in category_line:
        all_category_tag = category.tag
        tag_choice = (category.name, [(tag.id, tag.name) for tag in all_category_tag])
        form_pro_line_choice.append(tag_choice)
    form.pro_line.choices = form_pro_line_choice
    if form.validate_on_submit():
        new_version = Version(pro_line=form.pro_line.data, num=form.num.data, is_new=form.is_new.data,
                              is_pre=form.is_pre.data, details=form.details.data, pub_time=form.pub_time.data)
        db.session.add(new_version)
        db.session.commit()
        flash('版本信息已保存。', 'alert-success')
        return redirect(url_for('.version'))
    return render_template('admin/version-add.html', form=form)


@admin.route('/version/edit', methods=['GET', 'POST'])
@login_required
def edit_version():
    from ..models import db, Version, Category
    this_version = Version.query.get_or_404(request.args.get('version_id'))
    form = AdminVersionForm(pro_line=this_version.pro_line, num=this_version.num, is_new=this_version.is_new,
                            is_pre=this_version.is_pre, details=this_version.details, pub_time=this_version.pub_time)
    form_pro_line_choice = []
    category_line = Category.query.filter_by(parents_id=3).all()
    for category in category_line:
        all_category_tag = category.tag
        tag_choice = (category.name, [(tag.id, tag.name) for tag in all_category_tag])
        form_pro_line_choice.append(tag_choice)
    form.pro_line.choices = form_pro_line_choice
    if form.validate_on_submit():
        this_version.pro_line = form.pro_line.data
        this_version.num = form.num.data
        this_version.is_pre = form.is_pre.data
        this_version.is_new = form.is_new.data
        this_version.details = form.details.data
        this_version.pub_time = form.pub_time.data
        db.session.add(this_version)
        db.session.commit()
        flash('版本信息已保存。', 'alert-success')
        return redirect(url_for('.version'))
    return render_template('admin/version-edit.html', form=form)