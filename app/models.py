# -*- coding: utf-8 -*-
from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class AdminLine(db.Model):
    __tablename__ = 'admin_line'
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'), primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.now)


class Admin(UserMixin, db.Model):
    __tablename__ = 'admin'  # 内部用户表
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), unique=True)  # 用户名
    name = db.Column(db.String(10))  # 真实姓名
    tel = db.Column(db.String(20), unique=True)  # 电话
    password_hash = db.Column(db.String(128))  # 密码
    email = db.Column(db.String(64), unique=True)  # 用户邮箱
    create_time = db.Column(db.DateTime, default=datetime.now)  # 账号创建时间
    modify_time = db.Column(db.DateTime, default=datetime.now)  # 账号修改时间
    question = db.relationship('Question', backref='assignee')  # 名下问题
    demand = db.relationship('Demand', backref='assignee')  # 名下需求
    status = db.Column(db.Boolean, default=True)  # 账号状态:锁死\正常
    line = db.relationship('AdminLine', backref=db.backref('line_admins', lazy='joined'), lazy='dynamic',
                           cascade='all, delete-orphan')

    @property
    def password(self):
        raise AttributeError('不能直接获取明文密码！')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def has_line(self, line):
        return self.line.filter_by(category_id=line.id).first() is not None

    def add_line(self, line):
        if not self.has_line(line):
            new_line = AdminLine(line_admins=self, admin_lines=line)
            db.session.add(new_line)
            db.session.commit()

    def del_line(self, line):
        old_line = self.line.filter_by(category_id=line.id).first()
        db.session.delete(old_line)
        db.session.commit()

    def __repr__(self):
        return "<Admin '{:s}>".format(self.username)


class Customer(UserMixin, db.Model):
    __tablename__ = 'customer'
    id = db.Column(db.Integer, primary_key=True)
    tel = db.Column(db.String(20), unique=True)  # 电话
    email = db.Column(db.String(64), unique=True)  # 邮箱
    password_hash = db.Column(db.String(128))  # 密码
    username = db.Column(db.String(12))  # 姓名
    department = db.Column(db.String(12))  # 部门
    question = db.relationship('Question', backref='create_customer')  # 名下问题
    demand = db.relationship('Demand', backref='create_customer')  # 名下需求
    create_time = db.Column(db.DateTime, default=datetime.now)  # 账号创建时间
    modify_time = db.Column(db.DateTime, default=datetime.now)  # 账号修改时间
    status = db.Column(db.Boolean, default=True)  # 账号状态:锁死\正常

    @property
    def password(self):
        raise AttributeError('不能直接获取明文密码！')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "<Member '{0}>".format(self.username)


class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True)
    id_hash = db.Column(db.String(128), unique=True)
    own_customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))  # 问题所属用户
    assignee_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # 问题负责人
    title = db.Column(db.String(60))  # 标题
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))  # 所属分类ID
    details = db.Column(db.Text, default='')  # 问题详情
    status = db.Column(db.Integer, default=1)
    '''
    1 待处理
    2 处理中
    3 已完结
    '''
    feedback = db.Column(db.Text, default='')  # 反馈详情
    create_time = db.Column(db.DateTime, default=datetime.now)  # 账号创建时间
    modify_time = db.Column(db.DateTime, default=datetime.now)  # 账号修改时间

    def __repr__(self):
        return "<Question '{0}>".format(self.id)


class Demand(db.Model):
    __tablename__ = 'demand'
    id = db.Column(db.Integer, primary_key=True)
    id_hash = db.Column(db.String(128), unique=True)
    own_customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))  # 需求所属用户
    assignee_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # 问题负责人
    title = db.Column(db.String(60))  # 需求标题
    type_id = db.Column(db.Integer)  # 需求类型
    audience_id = db.Column(db.Integer)  # 需求受众
    source_id = db.Column(db.Integer)  # 需求来源
    support_id = db.Column(db.String(100))  # 支持内容
    des_type_id = db.Column(db.Integer)  # 设计类型
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))  # 所属分类ID
    details = db.Column(db.Text, default='')  # 需求详情
    attachment = db.Column(db.Text, default='')  # 附件地址
    status = db.Column(db.Integer, default=1)
    '''
    1 待确认
    2 待调研
    3 产品排期中
    4 设计中
    5 研发排期中
    6 研发实现中
    9 搁置
    10 已实现
    100 不实现
    '''
    feedback = db.Column(db.Text, default='')  # 反馈详情
    create_time = db.Column(db.DateTime, default=datetime.now)  # 创建时间
    modify_time = db.Column(db.DateTime, default=datetime.now)  # 最后修改时间
    p_done_time = db.Column(db.DateTime)  # 产品预计完成时间
    t_done_time = db.Column(db.DateTime)  # 技术预计完成时间

    def __repr__(self):
        return "<Question '{:s}>".format(self.id)


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
    questions = db.relationship('Question', backref='category')  # 分类下问题
    demands = db.relationship('Demand', backref='category')  # 分类下需求
    admins = db.relationship('AdminLine', backref=db.backref('admin_lines', lazy='joined'), lazy='dynamic',
                             cascade='all, delete-orphan')  # 当分类被当做业务领域使用时,对应的管理员

    def __repr__(self):
        return "<Category '{:s}>".format(self.name)


class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))  # tag名
    sequence = db.Column(db.Integer, default=0)  # 排序:小数靠前,大数靠后
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))  # 所属分类ID
    page = db.relationship('Page', backref='tag')  # tag下所属文章
    version = db.relationship('Version', backref='tag')  # tag下所属版本
    status = db.Column(db.Boolean, default=1)  # 启用/弃用

    def __repr__(self):
        return "<Tag '{:s}>".format(self.name)


class Page(db.Model):
    __tablename__ = 'page'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20))  # 文章标题
    text = db.Column(db.Text)  # 正文
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))  # 所属Tag的ID
    create_time = db.Column(db.DateTime, default=datetime.now)  # 账号创建时间
    modify_time = db.Column(db.DateTime, default=datetime.now)  # 账号修改时间

    def __repr__(self):
        return "<Page '{:s}>".format(self.title)



# 重写表
class Config(db.Model):
    __tablename__ = 'configs'
    key = db.Column(db.String(64), primary_key=True)  # 配置名
    value = db.Column(db.Text)  # 配置值