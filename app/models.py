# -*- coding: utf-8 -*-
from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime







class Version(db.Model):
    __tablename__ = 'version'
    id = db.Column(db.Integer, primary_key=True)
    pro_line = db.Column(db.Integer, db.ForeignKey('tag.id'))  # 产品线
    num = db.Column(db.String(10))  # 版本号
    is_new = db.Column(db.Boolean, default=False)  # 是否最新版本
    is_pre = db.Column(db.Boolean, default=False)  # 是否预告版本
    details = db.Column(db.Text)  # 更新内容
    pub_time = db.Column(db.DateTime, default=datetime.now)  # 版本发布时间

    def __repr__(self):
        return "<Version '{:s}>".format(self.num)


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10))  # 类目名
    parents = db.relationship('Category', uselist=False, remote_side=id)  # 上级分类对象
    parents_id = db.Column(db.Integer, db.ForeignKey('category.id'))  # 上级分类ID
    sequence = db.Column(db.Integer, default=1)  # 排序:小数靠前,大数靠后
    tag = db.relationship('Tag', backref='category')  # 分类下tags

    def __repr__(self):
        return "<Category '{:s}>".format(self.name)


class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))  # tag名
    sequence = db.Column(db.Integer, default=0)  # 排序:小数靠前,大数靠后
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))  # 所属分类ID
    version = db.relationship('Version', backref='tag')  # tag下所属版本
    status = db.Column(db.Boolean, default=1)  # 启用/弃用

    def __repr__(self):
        return "<Tag '{:s}>".format(self.name)



"""
V1.0
新版本重新定义数据库表结构
"""


# 配置表
class Config(db.Model):
    """
        configs:记录网站的一些个性化配置信息,采用键值对方式,value以字典方式存储一些配置信息
    """
    __tablename__ = 'configs'
    key = db.Column(db.String(64), primary_key=True)  # 配置名
    value = db.Column(db.Text)  # 配置值

    def __repr__(self):
        return "<Config '{0}>".format(self.key)


# 组织架构
class Department(db.Model):
    __tablename__ = 'departments'
    id = db.Column(db.Integer, primary_key=True)
    oa_id = db.Column(db.String(128), unique=True)  # OA系统的ID,默认是钉钉的部门ID
    name = db.Column(db.String(30))  # 部门名称
    status = db.Column(db.Boolean, default=True)  # 账号状态:正常 / 冻结

    def __repr__(self):
        return "<Department '{0}>".format(self.name)


# 工单表
class Issue(db.Model):
    __tablename__ = 'issues'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))  # 标题
    details = db.Column(db.Text, default='')  # 问题详情
    feedback = db.Column(db.Text, default='')  # 反馈详情
    status = db.Column(db.Integer, default=10)  # 问题处理进度
    extend = db.Column(db.Text, default='')  # 扩展字段,用来存储其他信息
    log = db.Column(db.Text, default='[]')  # 处理日志
    create_time = db.Column(db.DateTime, default=datetime.now)  # 工单创建时间
    modify_time = db.Column(db.DateTime, default=datetime.now)  # 工单最近一次更新时间

    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # 创建人
    assignee_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # 当前负责人

    def __repr__(self):
        return "<Issue '{0}>".format(self.title)


# 用户表
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    oa_id = db.Column(db.String(128), unique=True)  # OA系统的ID,默认是钉钉的员工ID
    username = db.Column(db.String(64), unique=True)  # 用户名
    password_hash = db.Column(db.String(128))  # 密码
    name = db.Column(db.String(12), default='')  # 姓名
    email = db.Column(db.String(64), default='')  # 邮箱
    tel = db.Column(db.String(20), default='')  # 电话
    department = db.Column(db.Text)  # 部门
    create_time = db.Column(db.DateTime, default=datetime.now)  # 账号创建时间
    modify_time = db.Column(db.DateTime, default=datetime.now)  # 账号修改时间
    admin = db.Column(db.Boolean, default=False)  # 是否管理员
    super_admin = db.Column(db.Boolean, default=False)  # 是否超级管理员
    status = db.Column(db.Boolean, default=True)  # 账号状态:正常 / 冻结

    issue = db.relationship('Issue', backref='creator', foreign_keys=[Issue.creator_id])  # 名下工单
    assign_issue = db.relationship('Issue', backref='assignee', foreign_keys=[Issue.assignee_id])  # 指派的工单

    @property
    def password(self):
        raise AttributeError('不能直接获取明文密码！')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "<Users '{0}>".format(self.username)


# 文章
class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20))  # 文章标题
    details = db.Column(db.Text)  # 正文
    tag_id = db.Column(db.Text, default='[]')  # 文章Tags
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # 作者
    status = db.Column(db.Boolean, default=False)  # 账号状态:草稿 / 发布
    create_time = db.Column(db.DateTime, default=datetime.now)  # 文章发布时间
    modify_time = db.Column(db.DateTime, default=datetime.now)  # 文章最后修改时间

    def __repr__(self):
        return "<Article '{:s}>".format(self.title)
