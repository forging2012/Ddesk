# -*- coding: utf-8 -*-
from . import front
from flask import render_template, request
from app import config
from flask_login import current_user, login_required
from ..models import Config, Issue


@front.route('/query')
@login_required
def query():
    old_title = Config.query.filter_by(key='title').first()
    old_subtitle = Config.query.filter_by(key='subtitle').first()
    web_title = old_title.value if old_title else ''
    web_subtitle = old_subtitle.value if old_subtitle else ''
    all_issue = Issue.query.filter_by(status=request.args.get('status'), creator_id=current_user.id).all()
    return render_template('front/query.html', all_issue=all_issue, web_title=web_title, web_subtitle=web_subtitle,
                           status=request.args.get('status'))


@front.route('/query/details')
@login_required
def query_details():
    old_title = Config.query.filter_by(key='title').first()
    old_subtitle = Config.query.filter_by(key='subtitle').first()
    web_title = old_title.value if old_title else ''
    web_subtitle = old_subtitle.value if old_subtitle else ''
    this_issue = Issue.query.get(request.args.get('id'))
    logs = eval(this_issue.log)
    extend = eval(this_issue.extend)
    return render_template('front/queryDetails.html', this_issue=this_issue, web_title=web_title,
                           web_subtitle=web_subtitle, status=config.ISSUE_STATUS, logs=logs, extend=extend)