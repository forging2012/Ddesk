# -*- coding: utf-8 -*-
from . import admin
from app.forms import AdminCategoryForm
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required


@admin.route('/category')
@login_required
def category():
    from ..models import Category
    all_category = Category.query.all()
    return render_template('admin/category.html', all_category=all_category, Category=Category)


@admin.route('/category/add', methods=['GET', 'POST'])
@login_required
def add_category():
    from ..models import db, Category
    form = AdminCategoryForm()
    all_top_category = Category.query.filter_by(parents_id=None).all()
    form.parents_id.choices = [(category.id, category.name) for category in all_top_category]
    form.parents_id.choices.insert(0, (0, '顶级分类'))
    if form.validate_on_submit():
        if form.parents_id.data == 0:
            new_category = Category(name=form.name.data, sequence=form.sequence.data)
        else:
            new_category = Category(name=form.name.data, sequence=form.sequence.data, parents_id=form.parents_id.data)
        db.session.add(new_category)
        db.session.commit()
        flash('新分类已添加。', 'alert-success')
        return redirect(url_for('.category'))
    return render_template('admin/category-add.html', form=form)


@admin.route('/category/edit', methods=['GET', 'POST'])
@login_required
def edit_category():
    from ..models import db, Category
    old_category = Category.query.get_or_404(request.args.get('category_id'))
    form = AdminCategoryForm(name=old_category.name, sequence=old_category.sequence)
    all_top_category = Category.query.filter_by(parents_id=None).all()
    # 查询当前分类是否已有子分类,如果有,不允许设置上级分类
    if Category.query.filter_by(parents_id=old_category.id).first() is None:
        # 查询当前子分类是否已设定上级分类,若设定,则设置默认值
        if old_category.parents_id is not None:
            form.parents_id.choices = [(category.id, category.name) for category in all_top_category]
            form.parents_id.choices.remove((old_category.parents.id, old_category.parents.name))
            form.parents_id.choices.insert(0, (0, '顶级分类'))
            form.parents_id.choices.insert(0, (old_category.parents.id, old_category.parents.name))
        else:
            form.parents_id.choices = [(category.id, category.name) for category in all_top_category]
            form.parents_id.choices.remove((old_category.id, old_category.name))
            form.parents_id.choices.insert(0, (0, '顶级分类'))
    else:
        form.parents_id.choices = [(0, '已有二级分类关联,只允许是顶级分类')]
    if form.validate_on_submit():
        old_category.name = form.name.data
        old_category.sequence = form.sequence.data
        if form.parents_id.data != 0:
            old_category.parents_id = form.parents_id.data
        else:
            old_category.parents_id = None
        db.session.add(old_category)
        db.session.commit()
        flash('分类信息已更新。', 'alert-success')
        return redirect(url_for('.category'))
    return render_template('admin/category-edit.html', form=form)
