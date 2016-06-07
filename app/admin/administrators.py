# -*- coding: utf-8 -*-
"""
__author__ = 'duzhipeng'
__mtime__ = '6/7/16'
# code is far away from bugs with the god animal protecting
    I love animals. They taste delicious.
              ┏┓      ┏┓
            ┏┛┻━━━┛┻┓
            ┃      ☃      ┃
            ┃  ┳┛  ┗┳  ┃
            ┃      ┻      ┃
            ┗━┓      ┏━┛
                ┃      ┗━━━┓
                ┃  神兽保佑    ┣┓
                ┃　永无BUG！   ┏┛
                ┗┓┓┏━┳┓┏┛
                  ┃┫┫  ┃┫┫
                  ┗┻┛  ┗┻┛
"""
from . import admin
from flask.ext.login import login_required
from flask import render_template, redirect, url_for, flash, request
from app.forms import AdminAdminForm, AdminAdminEditForm


@admin.route('/admin')
@login_required
def administrators():
    from ..models import Admin
    all_admin = Admin.query.all()
    return render_template('admin/admin.html', all_admin=all_admin)


@admin.route('/admin/add', methods=['GET', 'POST'])
@login_required
def add_administrators():
    from ..models import db, Admin
    form = AdminAdminForm()
    if form.validate_on_submit():
        new_admin = Admin(username=form.username.data, name=form.name.data, password=form.password.data)
        db.session.add(new_admin)
        db.session.commit()
        flash('添加管理员成功。', 'alert-success')
        return redirect(url_for('.administrators'))
    return render_template('admin/admin-add.html', form=form)


@admin.route('/admin/edit', methods=['GET', 'POST'])
@login_required
def edit_administrators():
    from ..models import db, Admin, Category
    this_admin = Admin.query.get_or_404(request.args.get('id'))
    this_admin_old_line = [line.admin_lines.id for line in this_admin.line.all()]
    form = AdminAdminEditForm(username=this_admin.username, name=this_admin.name, line=this_admin_old_line)
    category_line = Category.query.filter_by(parents_id=3).all()
    print(('产品线', [(line.id, line.name) for line in category_line]))
    form.line.choices = [('产品线', [(line.id, line.name) for line in category_line])]
    if form.validate_on_submit():
        this_admin.name = form.name.data
        if form.password.data:
            this_admin.password = form.password.data
        for old_line in this_admin.line.all():
            # 清除掉老的Tag
            this_admin.del_line(old_line.admin_lines)
        # 更新角色Tag
        for line_id in form.line.data:
            new_line = Category.query.get_or_404(line_id)
            if new_line is not None:
                this_admin.add_line(new_line)
        db.session.add(this_admin)
        db.session.commit()
        flash('管理员信息已更新。', 'alert-success')
        return redirect(url_for('.administrators'))
    return render_template('admin/admin-edit.html', form=form)