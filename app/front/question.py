# -*- coding: utf-8 -*-
"""
__author__ = 'Zhipeng Du'
__mtime__ = '16/9/1' '18:27'
"""
from . import front
from flask import render_template, redirect, url_for
from ..forms import QuestionForm
from app import ding
from flask_login import login_required, current_user
from ..models import db, Category, Config, Issue


@front.route('/question/add', methods=['GET', 'POST'])
@login_required
def add_question():
    old_title = Config.query.filter_by(key='title').first()
    old_subtitle = Config.query.filter_by(key='subtitle').first()
    web_title = old_title.value if old_title else ''
    web_subtitle = old_subtitle.value if old_subtitle else ''
    form = QuestionForm()
    categories = Category.query.filter_by(parents_id=3).all()
    form.category.choices = [(category.id, category.name) for category in categories]
    form.category.choices.insert(0, (0, '请选择产品线'))
    if form.validate_on_submit():
        new_issue = Issue(title=form.title.data, details=form.details.data, creator_id=current_user.id,
                          extend=str({'class_id': 1, 'category_id': form.category.data}))
        db.session.add(new_issue)
        db.session.commit()
        url = 'http://chanpin.xinlonghang.cn/back/question/edit?id=' + str(new_issue.id) + '&type=html5'
        print(url)
        this_category = Category.query.get(form.category.data)
        data = {'create_customer': new_issue.creator.name, 'category': this_category.name,
                'num': new_issue.id}
        ding.msg(category=1, url=url, data=data)
        return redirect(url_for('.commit_success'))
    return render_template('front/questionNew.html', form=form, web_title=web_title, web_subtitle=web_subtitle)



