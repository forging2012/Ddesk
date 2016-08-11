# -*- coding: utf-8 -*-
from . import front
from flask import render_template, redirect, url_for
from ..forms import FrontQuestionForm
from app import ding_msg
from flask_login import login_required, current_user
from ..models import db, Question, Category, Config
from hashlib import md5
from datetime import datetime


@front.route('/question/add', methods=['GET', 'POST'])
@login_required
def add_question():
    web_title = ''
    web_subtitle = ''
    old_title = Config.query.filter_by(key='title').first()
    old_subtitle = Config.query.filter_by(key='subtitle').first()
    if old_title:
        web_title = old_title.value
    if old_subtitle:
        web_subtitle = old_subtitle.value
    form = FrontQuestionForm()
    categories = Category.query.filter_by(parents_id=3).all()
    form.category.choices = [(category.id, category.name) for category in categories]
    form.category.choices.insert(0, (0, '请选择产品线'))
    if form.validate_on_submit():
        text = str(current_user.id) + str(datetime.now())
        m = md5()
        m.update(text.encode('utf-8'))
        id_hash = m.hexdigest()
        new_question = Question(own_customer_id=current_user.id, details=form.details.data, category_id=form.category.data,
                                id_hash=id_hash)
        db.session.add(new_question)
        db.session.commit()
        this_question = Question.query.filter_by(id_hash=id_hash).first()
        url = 'http://chanpin.xinlonghang.cn/admin/question/edit?question_id=' + str(this_question.id)
        data = {'create_customer': this_question.create_customer.username, 'category': this_question.category.name,
                'num': this_question.id}
        ding_msg.msg(category=1, url=url, data=data)
        return redirect(url_for('.commit_success'))
    return render_template('new-question.html', form=form, page_name='add_question', web_title=web_title, web_subtitle=web_subtitle)



