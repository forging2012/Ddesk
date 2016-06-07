# -*- coding: utf-8 -*-
from . import admin
from app.forms import AdminTagForm
from flask import render_template, redirect, url_for, flash, request
from flask.ext.login import login_required


@admin.route('/tag')
@login_required
def tag():
    from ..models import Tag
    all_tags = Tag.query.all()
    return render_template('admin/tag.html', all_tags=all_tags)


@admin.route('/tag/add', methods=['GET', 'POST'])
@login_required
def add_tag():
    from ..models import db, Tag, Category
    form = AdminTagForm()
    all_category = Category.query.all()
    form.category_id.choices = [(category.id, category.name) for category in all_category]
    if form.validate_on_submit():
        new_tag = Tag(name=form.name.data, sequence=form.sequence.data, category_id=form.category_id.data)
        db.session.add(new_tag)
        db.session.commit()
        flash('添加Tag成功。', 'alert-success')
        return redirect(url_for('.tag'))
    return render_template('admin/tag-add.html', form=form)


@admin.route('/tag/edit', methods=['GET', 'POST'])
@login_required
def edit_tag():
    from ..models import db, Tag, Category
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
        return redirect(url_for('.tag'))
    return render_template('admin/tag-edit.html', form=form)
