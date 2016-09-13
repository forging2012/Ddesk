# -*- coding: utf-8 -*-
"""
__author__ = 'Zhipeng Du'
__mtime__ = '16/9/1' '18:27'
"""
from . import front
from flask import render_template, redirect, url_for, request
from ..forms import ProductDemandForm, DesignDemandForm
from flask_login import login_required, current_user
from app import ding
from ..models import db, Category, Config, Tag, Issue


@front.route('/demand/add', methods=['GET', 'POST'])
@login_required
def add_demand():
    old_title = Config.query.filter_by(key='title').first()
    old_subtitle = Config.query.filter_by(key='subtitle').first()
    web_title = old_title.value if old_title else ''
    web_subtitle = old_subtitle.value if old_subtitle else ''
    if request.args.get('c') == 'p':
        form = ProductDemandForm()
        all_type = Tag.query.filter_by(category_id=10, status=1).all()
        all_audience = Tag.query.filter_by(category_id=11, status=1).all()
        all_source = Tag.query.filter_by(category_id=12, status=1).all()
        categories = Category.query.filter_by(parents_id=3).all()
        form.type.choices = [(tag.id, tag.name) for tag in all_type]
        form.audience.choices = [(tag.id, tag.name) for tag in all_audience]
        form.source.choices = [(tag.id, tag.name) for tag in all_source]
        form.category.choices = [(category.id, category.name) for category in categories]
        form.type.choices.insert(0, (0, '请选择需求类型'))
        form.audience.choices.insert(0, (0, '请选择受众范围'))
        form.source.choices.insert(0, (0, '请选择需求来源'))
        form.category.choices.insert(0, (0, '请选择产品线'))
        if form.validate_on_submit():
            extend = {'class_id': 3, 'audience_id': form.audience.data, 'source_id': form.source.data,
                      'category_id': form.category.data, 'type_id': form.type.data}
            new_issue = Issue(title=form.title.data, details=form.details.data, extend=str(extend), creator_id=current_user.id)
            db.session.add(new_issue)
            db.session.commit()

            audience = Tag.query.get(form.audience.data)
            source = Tag.query.get(form.source.data)
            category = Category.query.get(form.category.data)
            url = 'http://chanpin.xinlonghang.cn/back/demand/edit?id=' + str(new_issue.id) + '&type=html5' + '&class=3'
            data = {'create_customer': current_user.name, 'num': new_issue.id,
                    'type': '产品需求', 'audience': audience.name, 'source': source.name, 'category': category.name}
            ding.msg(category=3, url=url, data=data)
            return redirect(url_for('.commit_success'))
        return render_template('front/demandNewProduct.html', form=form, web_title=web_title, web_subtitle=web_subtitle)
    elif request.args.get('c') == 'd':
        form = DesignDemandForm()
        all_des_type = Tag.query.filter_by(category_id=20, status=1).all()
        form.des_type.choices = [(tag.id, tag.name) for tag in all_des_type]
        form.des_type.choices.insert(0, (0, '请选择设计类型'))
        if form.validate_on_submit():
            extend = {'class_id': 2, 'des_type_id': form.des_type.data,
                      'support_id': {40: form.support1.data, 39: form.support2.data, 38: form.support3.data}}
            new_issue = Issue(title=form.title.data, details=form.details.data, extend=str(extend), creator_id=current_user.id)
            db.session.add(new_issue)
            db.session.commit()

            supports = {40: form.support1.data, 39: form.support2.data, 38: form.support3.data}
            support1 = ''
            support2 = ''
            support3 = ''
            if supports.get(40):
                support1 = '宣传  '
            if supports.get(39):
                support2 = '品牌  '
            if supports.get(38):
                support3 = '设计  '
            support = support1 + support2 + support3
            des_type = Tag.query.get(form.des_type.data)
            url = 'http://chanpin.xinlonghang.cn/back/demand/edit?id=' + str(new_issue.id) + '&type=html5' + '&class=2'
            data = {'create_customer': current_user.name, 'num': new_issue.id,
                    'type': '设计需求', 'support': support, 'des_type': des_type.name}
            ding.msg(category=2, url=url, data=data)
            return redirect(url_for('.commit_success'))
        return render_template('front/demandNewDesign.html', form=form, web_title=web_title, web_subtitle=web_subtitle)

