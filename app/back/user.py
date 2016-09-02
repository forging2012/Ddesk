# -*- coding: utf-8 -*-
"""
__author__ = 'Zhipeng Du'
__mtime__ = '16/8/31' '16:26'
"""
from . import back
from app.forms import UserForm
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required
from ..models import db, User, Department
from app import ding
from datetime import datetime


@back.route('/user')
@login_required
def user():
    all_users = User.query.all()
    return render_template('back/user.html', all_users=all_users)


@back.route('/user/add', methods=['GET', 'POST'])
@login_required
def add_user():
    form = UserForm(status=1)
    if form.validate_on_submit():
        new_user = User(username=form.username.data, name=form.name.data, email=form.email.data, tel=form.tel.data,
                        status=True if form.status.data == 1 else False)
        db.session.add(new_user)
        db.session.commit()
        flash('添加用户成功。', 'is-success')
        return redirect(url_for('.user'))
    return render_template('back/addUser.html', form=form)


@back.route('/user/edit', methods=['GET', 'POST'])
@login_required
def edit_user():
    this_user = User.query.get_or_404(request.args.get('id'))
    form = UserForm(username=this_user.username, name=this_user.name, email=this_user.email, tel=this_user.tel,
                    status=1 if this_user.status else 2)
    if form.validate_on_submit():
        this_user.email = form.email.data
        this_user.name = form.name.data
        this_user.tel = form.tel.data
        this_user.status = True if form.status.data == 1 else False
        db.session.add(this_user)
        db.session.commit()
        flash('用户信息已更新。', 'is-success')
        return redirect(url_for('.user'))
    return render_template('back/editUser.html', form=form)


@back.route('/user/sync')
@login_required
def sync_user():
    if request.args.get('do') == '1':
        department_data = ding.get_department()
        oa_department_list = []
        oa_user_list = []

        # 同步新增部门或更新部门的详情
        for item in department_data:
            old_department = Department.query.filter_by(oa_id=item['id']).first()
            oa_department_list.append(str(item['id']))
            if old_department is None:
                new_department = Department(oa_id=item['id'], name=item['name'])
                db.session.add(new_department)
            else:
                old_department.name = item['name']
                db.session.add(old_department)
            db.session.commit()

        # 同步锁定在OA中已被删除的部门。OA系统侧对于已删除再添加的部门,部门ID不能用以前存在过的
        # 同步部门数据的时候,会连同同步部门员工数据
        all_department = Department.query.all()
        all_user = User.query.all()
        for item in all_department:
            if item.oa_id not in oa_department_list:
                item.status = False
                db.session.add(item)
            db.session.commit()

            # 同步新增用户或更新已存在用户的详情
            oa_user_data = ding.get_user(item.oa_id)
            for oa_user in oa_user_data:
                old_user = User.query.filter_by(oa_id=oa_user['userid']).first()
                oa_user_list.append(str(oa_user['userid']))
                if old_user is None:
                    new_user = User(oa_id=oa_user['userid'],
                                    username=oa_user['email'].split('@')[0] if len(oa_user['email']) > 3 else oa_user['userid'],
                                    name=oa_user['name'], email=oa_user['email'],
                                    tel=oa_user['mobile'], department=str(oa_user['department']))
                    db.session.add(new_user)
                else:
                    old_user.name = oa_user['name']
                    old_user.email = oa_user['email']
                    old_user.tel = oa_user['mobile']
                    old_user.department = str(oa_user['department'])
                    old_user.modify_time = datetime.now()
                    db.session.add(old_user)
                db.session.commit()
        for sys_user in all_user:
            if sys_user.oa_id not in oa_user_list:
                sys_user.status = False
                db.session.add(sys_user)
            db.session.commit()
        flash('数据同步完成。', 'is-success')
        return redirect(url_for('.sync_user'))
    return render_template('back/syncUser.html')
