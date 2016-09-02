# -*- coding: utf-8 -*-
"""
__author__ = 'Zhipeng Du'
__mtime__ = '16/9/1' '18:27'
"""
from . import front
from flask import render_template, redirect, url_for
from ..forms import QuestionForm
from app import ding_msg
from flask_login import login_required, current_user
from ..models import db, Question, Category, Config, Issue, Customer


@front.route('/question/add', methods=['GET', 'POST'])
@login_required
def add_question():
    old_user = Customer.query.filter_by(username=current_user.name).first()

    old_title = Config.query.filter_by(key='title').first()
    old_subtitle = Config.query.filter_by(key='subtitle').first()
    web_title = old_title.value if old_title else ''
    web_subtitle = old_subtitle.value if old_subtitle else ''
    form = QuestionForm()
    categories = Category.query.filter_by(parents_id=3).all()
    form.category.choices = [(category.id, category.name) for category in categories]
    form.category.choices.insert(0, (0, '请选择产品线'))
    if form.validate_on_submit():
        new_issue = Issue(details=form.details.data, creator_id=current_user.id, extend=str({'category': form.category.data}))
        db.session.add(new_issue)
        db.session.commit()

        new_question = Question(creator_id=current_user.id, details=form.details.data, category_id=form.category.data, issues_id=new_issue.id, own_customer_id=old_user.id if old_user is not None else 8)
        db.session.add(new_question)
        db.session.commit()

        url = 'http://chanpin.xinlonghang.cn/admin/question/edit?question_id=' + str(new_question.id)
        data = {'create_customer': new_question.creator.name, 'category': new_question.category.name,
                'num': new_question.id}
        ding_msg.msg(category=1, url=url, data=data)
        return redirect(url_for('.commit_success'))
    return render_template('front/new-question.html', form=form, page_name='add_question',
                           web_title=web_title, web_subtitle=web_subtitle)



