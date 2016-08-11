# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SubmitField, FloatField, TextAreaField, SelectField, HiddenField, IntegerField, BooleanField, RadioField, DateTimeField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask.ext.wtf.file import FileField, FileAllowed, FileRequired
from wtforms_components import SelectField as SelectField2, SelectMultipleField





class AddDemandForm(Form):
    type = SelectField('需求类型', validators=[DataRequired('请选需求类型。')], coerce=int)
    audience = SelectField('需求受众', validators=[DataRequired('请选需求受众。')], coerce=int)
    source = SelectField('需求来源', validators=[DataRequired('请选需求来源。')], coerce=int)
    category = SelectField('针对产品线', validators=[DataRequired('请选择针对的产品线。')], coerce=int)
    details = TextAreaField('需求', validators=[DataRequired('请描述您的需求。')])
    submit = SubmitField('提交')


class LoginForm(Form):
    username = StringField('姓名', validators=[DataRequired('请填写姓名。')])
    tel = StringField('手机号', validators=[DataRequired('请填写手机号。')])
    submit = SubmitField('登录')


# 登录
class AdminLoginForm(Form):
    username = StringField('用户名', validators=[DataRequired('用户名必填哟！')])
    password = PasswordField('密码', validators=[DataRequired('密码忘记填了？')])
    key = StringField('密令', validators=[DataRequired('密令忘记填了？')])
    submit = SubmitField('')


# 更新问题
class AdminQuestionForm(Form):
    title = StringField('问题概述', validators=[DataRequired('问题概述必填。')])
    feedback = TextAreaField('反馈内容', validators=[DataRequired('反馈内容必填。')])
    status = SelectField('问题状态', validators=[DataRequired('问题状态必选。')], choices=[(0, '请选择'), (1, '待处理'),
                                                                                (2, '处理中'), (3, '已完结')],
                         coerce=int)
    assignee = SelectField('问题当前负责人', validators=[DataRequired('负责人必须指定。')], coerce=int)
    submit = SubmitField('更新')


# 更新需求
class AdminDemandForm(Form):
    title = StringField('需求概述', validators=[DataRequired('需求概述必填。')])
    feedback = TextAreaField('反馈内容')
    status = SelectField('处理进度', validators=[DataRequired('处理进度必选。')], choices=[(0, '请选择'), (100, '不实现'), (1, '待确认'),
                                                                                (2, '待调研'), (3, '排期中'),
                                                                                (4, '设计中'), (5, '研发排期中'),
                                                                                (6, '研发实现中'), (9, '搁置'),
                                                                                (10, '已完成'), (11, '部分完成')],
                         coerce=int)
    assignee = SelectField('需求当前负责人', validators=[DataRequired('负责人必须指定。')], coerce=int)
    submit = SubmitField('更新')


# 版本发布
class AdminVersionForm(Form):
    pro_line = SelectField2('产品线', validators=[DataRequired('产品线必填！')], coerce=int)
    num = StringField('版本号', validators=[DataRequired('版本号必填!')])
    details = TextAreaField('更新详情', validators=[DataRequired('更新详情必填。')])
    pub_time = DateTimeField('发布时间', validators=[DataRequired('发布时间必填。')],  format='%Y-%m-%d')
    is_pre = BooleanField('是预告版本')
    is_new = BooleanField('是最新版本')
    submit = SubmitField('保存')


# 用户管理
class AdminCustomerForm(Form):
    username = StringField('姓名', validators=[DataRequired('姓名必填哟！')])
    tel = StringField('手机号', validators=[DataRequired('手机号需要填写一个。')])
    submit = SubmitField('保存')

    def validate_tel(self, field):
        from .models import Customer
        if Customer.query.filter_by(tel=field.data).first():
            raise ValidationError('手机号已被其他用户使用，请您更换一个。')


# 添加分类
class AdminCategoryForm(Form):
    name = StringField('分类名', validators=[DataRequired('分类名必填哟！')])
    sequence = IntegerField('序号', validators=[DataRequired('序号必填！')])
    parents_id = SelectField('上级分类', coerce=int)
    submit = SubmitField('保存')


# 添加tag
class AdminTagForm(Form):
    name = StringField('Tag名', validators=[DataRequired('Tag名必填哟！')])
    sequence = IntegerField('排序', validators=[DataRequired('排序必填')])
    category_id = SelectField('所属分类', validators=[DataRequired('所属分类必须指定。')], coerce=int)
    submit = SubmitField('保存')


# 添加文章
class AdminPageForm(Form):
    title = StringField('标题', validators=[DataRequired('标题必填哟！')])
    text = TextAreaField('正文', validators=[DataRequired('正文必填哟！')])
    tag_id = SelectField('所属Tag', validators=[DataRequired('所属Tag必须指定。')], coerce=int)
    submit = SubmitField('保存')


# 添加管理员
class AdminAdminForm(Form):
    username = StringField('用户名(登录用)', validators=[DataRequired('用户名必填哟！')])
    name = StringField('姓名', validators=[DataRequired('姓名必填哟！')])
    tel = StringField('手机号', validators=[DataRequired('手机号必填哟！')])
    password = PasswordField('密码', validators=[DataRequired('密码必填哟！'), Length(1, 16, '密码6位以上，16位以下。'), EqualTo('password2', message='两次输入的密码不一致，请您检查后重新输入。')])
    password2 = PasswordField('重复密码')
    submit = SubmitField('保存')

    def validate_username(self, field):
        from .models import Admin
        if Admin.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已被使用，再想一个吧：）')


# 编辑管理员
class AdminAdminEditForm(Form):
    username = StringField('用户名(登录用)')
    name = StringField('姓名', validators=[DataRequired('姓名必填哟！')])
    tel = StringField('手机号', validators=[DataRequired('手机号必填哟！')])
    line = SelectMultipleField('负责产品线', coerce=int)
    password = PasswordField('密码', validators=[EqualTo('password2', message='两次输入的密码不一致，请您检查后重新输入。')])
    password2 = PasswordField('重复密码')
    submit = SubmitField('保存')


# 前言部分

# 新增问题
class FrontQuestionForm(Form):
    category = SelectField('针对产品或业务', validators=[DataRequired('请选择针对产品或业务。')], coerce=int)
    details = TextAreaField('详细说明', validators=[DataRequired('请填写详细说明。')])
    submit = SubmitField('')


# 后台部分

# 网站基本信息配置
class AdminConfigForm(Form):
    title = StringField('网站Title', validators=[DataRequired('网站Title必填！')])
    subtitle = StringField('网站副标题', validators=[DataRequired('网站副标题必填！')])
    submit = SubmitField('更新')







