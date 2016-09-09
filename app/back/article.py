# -*- coding: utf-8 -*-
"""
__author__ = 'Zhipeng Du'
__mtime__ = '16/9/8' '18:12'
"""
from . import back
from flask_login import login_required, current_user
from flask import render_template, redirect, url_for, flash, request
from ..models import db, Article, Tag, User
from ..forms import ArticleForm
from datetime import datetime


@back.route('/article')
@login_required
def article():
    all_article = Article.query.order_by(Article.modify_time.desc()).all()
    datas = []
    for item in all_article:
        author = User.query.get(item.author_id)
        tags = []
        for tag_id in eval(item.tag_id):
            tag = Tag.query.get(tag_id)
            tags.append(tag.name)
        item_dict = {'id': item.id, 'title': item.title, 'details': item.details, 'tags': tags,
                     'create_time': item.create_time, 'modify_time': item.modify_time, 'author': author.name}
        datas.append(item_dict)
    return render_template('back/article.html', datas=datas)


@back.route('/article/add', methods=['GET', 'POST'])
@login_required
def add_article():
    form = ArticleForm(status=1)
    all_tag = Tag.query.all()
    form.tag_id.choices = [(tag.id, tag.name) for tag in all_tag]
    if form.validate_on_submit():
        new_article = Article(title=form.title.data, details=form.details.data, tag_id='[form.tag_id.data]',
                              author_id=current_user.id)
        db.session.add(new_article)
        db.session.commit()
        flash('文章草稿已成功保存。', 'is-success')
        return redirect(url_for('.edit_article', id=new_article.id))
    return render_template('back/articleAdd.html', form=form)


@back.route('/article/edit', methods=['GET', 'POST'])
@login_required
def edit_article():
    this_article = Article.query.get_or_404(request.args.get('id'))
    if request.args.get('delete') == 'yes':
        db.session.delete(this_article)
        db.session.commit()
        flash('文章已删除。', 'is-success')
        return redirect(url_for('.article'))
    else:

        this_article_tags = eval(this_article.tag_id)[0]
        this_tag = Tag.query.get(this_article_tags)
        form = ArticleForm(title=this_article.title, details=this_article.details, tag_id=this_article_tags,
                           status=this_article.status)
        all_tag = Tag.query.all()
        form.tag_id.choices = [(tag.id, tag.name) for tag in all_tag]
        form.tag_id.choices.remove((this_tag.id, this_tag.name))
        form.tag_id.choices.insert(0, (this_tag.id, this_tag.name))
        if form.validate_on_submit():
            this_article.title = form.title.data
            this_article.details = form.details.data
            this_article.tag_id = str([form.tag_id.data])
            this_article.status = form.status.data
            this_article.author_id = current_user.id
            this_article.modify_time = datetime.now()
            db.session.add(this_article)
            db.session.commit()
            flash('文章信息已更新。', 'is-success')
            return redirect(url_for('.edit_article', id=this_article.id))
    return render_template('back/articleEdit.html', form=form)
