# -*- coding: utf-8 -*-
"""
__author__ = 'Zhipeng Du'
__mtime__ = '16/9/5' '17:42'
"""
from .models import db, Question, Issue, Customer, User, Admin, Demand


# 管理员用户数据迁移
def admin_to_user():
    all_admin = Admin.query.all()
    for item in all_admin:
        this_user = User.query.filter_by(name=item.name).first()
        if this_user is not None:
            this_user.admin = True
            this_user.password_hash = item.password_hash
            db.session.add(this_user)
            db.session.commit()
    print('管理员转用户数据转换成功')


# 问题迁移工单
def question_to_issue():
    all_question = Question.query.all()
    for item in all_question:
        if item.status == 1:
            status = 10
        elif item.status == 2:
            status = 20
        elif item.status == 3:
            status = 30
        this_customer = Customer.query.get(item.own_customer_id)
        this_user = User.query.filter_by(name=this_customer.username).first()
        if this_user is None:
            new_user = User(oa_id=this_customer.tel,
                            username=this_customer.tel,
                            name=this_customer.username,
                            tel=this_customer.tel,
                            create_time=this_customer.create_time, status=False)
            db.session.add(new_user)
            db.session.commit()
            this_user = new_user
        extend = str({'class_id': 1, 'category_id': item.category_id})
        old_assignee = Admin.query.get(item.assignee_id)
        new_assignee = User.query.filter_by(name=old_assignee.name).first()
        new_issue = Issue(title=item.title,
                          details=item.details,
                          feedback=item.feedback,
                          status=status,
                          extend=extend,
                          create_time=item.create_time,
                          modify_time=item.modify_time,
                          creator_id=this_user.id, assignee_id=new_assignee.id)
        db.session.add(new_issue)
        db.session.commit()
    print('问题转工单成功')


# 需求提出人ID转移
def demand_own_to_creator():
    all_demand = Demand.query.all()
    for item in all_demand:
        own_user = Customer.query.get(item.own_customer_id)
        creator = User.query.filter_by(name=own_user.username).first()
        if creator is None:
            new_user = User(oa_id=own_user.tel, username=own_user.tel, name=own_user.username,
                            tel=own_user.tel, create_time=own_user.create_time, status=False)
            db.session.add(new_user)
            db.session.commit()
            item.creator_id = new_user.id
        else:
            item.creator_id = creator.id
        db.session.add(item)
        db.session.commit()
    print('需求提出人ID转移成功')


# 需求迁移为工单
def page_to_article():
    pass


# 需求迁移为工单
def demand_to_issue():
    all_demand = Demand.query.all()
    for item in all_demand:
        pass
