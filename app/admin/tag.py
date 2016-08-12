# -*- coding: utf-8 -*-
from . import admin
from app.forms import AdminTagForm
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required
from ..models import db, Tag, Category


@admin.route('/tag')
@login_required
def tag():
    status = request.args.get('status')
    all_tags = Tag.query.filter_by(status=status).all()
    return render_template('admin/tag.html', all_tags=all_tags, status=status)


@admin.route('/tag/add', methods=['GET', 'POST'])
@login_required
def add_tag():
    form = AdminTagForm()
    all_category = Category.query.all()
    form.category_id.choices = [(category.id, category.name) for category in all_category]
    if form.validate_on_submit():
        new_tag = Tag(name=form.name.data, sequence=form.sequence.data, category_id=form.category_id.data)
        db.session.add(new_tag)
        db.session.commit()
        flash('添加Tag成功。', 'alert-success')
        return redirect(url_for('.tag', status=1))
    return render_template('admin/tag-add.html', form=form)


@admin.route('/tag/edit', methods=['GET', 'POST'])
@login_required
def edit_tag():
    old_tag = Tag.query.get_or_404(request.args.get('tag_id'))
    form = AdminTagForm(name=old_tag.name, sequence=old_tag.sequence)
    all_category = Category.query.all()
    form.category_id.choices = [(category.id, category.name) for category in all_category]
    form.category_id.choices.remove((old_tag.category.id, old_tag.category.name))
    form.category_id.choices.insert(0, (old_tag.category.id, old_tag.category.name))
    if form.validate_on_submit():
        old_tag.name = form.name.data
        old_tag.sequence = form.sequence.data
        old_tag.category_id = form.category_id.data
        db.session.add(old_tag)
        db.session.commit()
        flash('Tag信息已更新', 'alert-success')
        return redirect(url_for('.tag', status=1))
    return render_template('admin/tag-edit.html', form=form)


@admin.route('/tag/status')
@login_required
def status_tag():
    old_tag = Tag.query.get_or_404(request.args.get('tag_id'))
    if old_tag.status:
        old_tag.status = False
    else:
        old_tag.status = True
    db.session.add(old_tag)
    db.session.commit()
    flash('Tag状态已更新', 'alert-success')
    return redirect(url_for('.tag', status=1))