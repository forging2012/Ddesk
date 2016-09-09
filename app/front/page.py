# -*- coding: utf-8 -*-
from . import front
from flask import render_template, request
from ..models import Article, Config


@front.route('/page')
def page():
    web_title = Config.query.filter_by(key='title').first()
    this_page = Article.query.get_or_404(request.args.get('page_id'))
    return render_template('page.html', this_page=this_page, web_title=web_title)
