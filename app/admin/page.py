# -*- coding: utf-8 -*-
from . import admin
from app.forms import AdminPageForm
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required


@admin.route('/page')
@login_required
def page():
    from ..models import Page
    all_page = Page.query.all()
    return render_template('admin/page.html', all_page=all_page)


@admin.route('/page/add', methods=['GET', 'POST'])
@login_required
def add_page():
    from ..models import db, Page, Tag
    form = AdminPageForm()
    all_tag = Tag.query.all()
    form.tag_id.choices = [(tag.id, tag.name) for tag in all_tag]
    if form.validate_on_submit():
        new_page = Page(title=form.title.data, text=form.text.data, tag_id=form.tag_id.data)
        db.session.add(new_page)
        db.session.commit()
        flash('添加文章成功。', 'alert-success')
        return redirect(url_for('.page'))
    return render_template('admin/page-add.html', form=form)


@admin.route('/page/edit', methods=['GET', 'POST'])
@login_required
def edit_page():
    from ..models import db, Page, Tag
    old_page = Page.query.get_or_404(request.args.get('page_id'))
    form = AdminPageForm(title=old_page.title, text=old_page.text)
    all_tag = Tag.query.all()
    form.tag_id.choices = [(tag.id, tag.name) for tag in all_tag]
    form.tag_id.choices.remove((old_page.tag.id, old_page.tag.name))
    form.tag_id.choices.insert(0, (old_page.tag.id, old_page.tag.name))
    if form.validate_on_submit():
        old_page.title = form.title.data
        old_page.text = form.text.data
        old_page.tag_id = form.tag_id.data
        db.session.add(old_page)
        db.session.commit()
        flash('文章已更新。', 'alert-success')
        return redirect(url_for('.page'))
    return render_template('admin/page-edit.html', form=form)
