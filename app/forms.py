# -*- coding: utf-8 -*-
from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, IntegerField, BooleanField, DateTimeField, RadioField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, Email
from wtforms_components import SelectField as SelectField2, SelectMultipleField




# 版本发布
class AdminVersionForm(Form):
    pro_line = SelectField2('产品线', validators=[DataRequired('产品线必填！')], coerce=int)
    num = StringField('版本号', validators=[DataRequired('版本号必填!')])
    details = TextAreaField('更新详情', validators=[DataRequired('更新详情必填。')])
    pub_time = DateTimeField('发布时间', validators=[DataRequired('发布时间必填。')],  format='%Y-%m-%d')
    is_pre = BooleanField('是预告版本')
    is_new = BooleanField('是最新版本')
    submit = SubmitField('保存')


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





"""
V1.0
新版本重新设计表单
"""


# 网站基本信息配置
class AppConfigForm(Form):
    title = StringField('网站标题', validators=[DataRequired('网站标题不能为空。')])
    subtitle = StringField('网站副标题', validators=[DataRequired('网站副标题不能为空。')])
    submit = SubmitField('保存')


# 用户管理
class UserForm(Form):
    username = StringField('用户名', validators=[DataRequired('用户名必填。')])
    name = StringField('姓名', validators=[DataRequired('姓名必填。')])
    email = StringField('邮箱', validators=[DataRequired('邮箱必填。'), Email('Email格式不正确。')])
    tel = StringField('电话', validators=[DataRequired('电话必填。')])
    password = PasswordField('密码', validators=[EqualTo('re_password', message='两次输入的密码不一致，请您检查后重新输入。')])
    re_password = PasswordField('重复密码')
    status = RadioField('状态', validators=[DataRequired('状态必选。')], choices=[(1, '正常'), (2, '锁定')], coerce=int)
    admin = BooleanField('开通管理员')
    submit = SubmitField('保存')


# 用户登录
class UserLoginForm(Form):
    name = StringField('姓名', validators=[DataRequired('请填写姓名。')])
    tel = StringField('手机号', validators=[DataRequired('请填写手机号。')])
    submit = SubmitField('登录')


# 新增问题
class QuestionForm(Form):
    category = SelectField('针对产品或业务', validators=[DataRequired('请选择针对产品或业务。')], coerce=int)
    title = StringField('问题或建议', validators=[DataRequired('需求概述必填。')])
    details = TextAreaField('补充说明')
    submit = SubmitField('提交')


# 处理问题类工单
class QuestionIssueForm(Form):
    title = StringField('概述', validators=[DataRequired('概述必填。')])
    feedback = TextAreaField('反馈内容', validators=[DataRequired('反馈内容必填。')])
    status = SelectField('当前处理进度', validators=[DataRequired('当前处理进度必选。')], choices=[(0, '请选择'), (10, '待处理'),
                                                                                (20, '处理中'), (30, '处理完毕')], coerce=int)
    assignee = SelectField('负责人', validators=[DataRequired('负责人必须指定。')], coerce=int)
    submit = SubmitField('更新')


# 新增产品需求
class ProductDemandForm(Form):
    type = SelectField('需求类型', validators=[DataRequired('请选择需求类型。')], coerce=int)
    audience = SelectField('需求受众', validators=[DataRequired('请选择需求受众。')], coerce=int)
    source = SelectField('需求来源', validators=[DataRequired('请选择需求来源。')], coerce=int)
    category = SelectField('针对产品线或业务', validators=[DataRequired('请选择针对的产品线。')], coerce=int)
    title = StringField('需求概述', validators=[DataRequired('需求概述必填。')])
    details = TextAreaField('补充说明')
    submit = SubmitField('提交')


# 新增设计需求
class DesignDemandForm(Form):
    support1 = BooleanField('宣传')
    support2 = BooleanField('品牌')
    support3 = BooleanField('设计')
    des_type = SelectField('设计类型', validators=[DataRequired('请选择设计类型。')], coerce=int)
    title = StringField('需求概述', validators=[DataRequired('需求概述必填。')])
    details = TextAreaField('补充说明')
    submit = SubmitField('提交')


# 处理需求类工单d
class DemandIssueForm(Form):
    title = StringField('概述', validators=[DataRequired('概述必填。')])
    design_done_time = StringField('预计设计完成时间')
    online_time = StringField('预计发版上线时间')
    feedback = TextAreaField('反馈内容')
    status = SelectField('当前处理进度', validators=[DataRequired('处理进度必选。')],
                         choices=[(0, '请选择'), (10, '待处理'), (20, '处理中'), (30, '处理完毕')], coerce=int)
    assignee = SelectField('需求当前负责人', validators=[DataRequired('负责人必须指定。')], coerce=int)
    submit = SubmitField('更新')


# 管理后台登录
class AdminLoginForm(Form):
    username = StringField('用户名', validators=[DataRequired('用户名必填哟！')])
    password = PasswordField('密码', validators=[DataRequired('密码忘记填了？')])
    token = StringField('密令', validators=[DataRequired('密令忘记填了？')])
    submit = SubmitField('')


# 添加文章
class ArticleForm(Form):
    title = StringField('标题', validators=[DataRequired('标题必填。')])
    details = TextAreaField('正文', validators=[DataRequired('正文必填。')])
    tag_id = SelectField('所属Tag', validators=[DataRequired('所属Tag必须指定。')], coerce=int)
    status = BooleanField('正式发布')
    submit = SubmitField('保存')
