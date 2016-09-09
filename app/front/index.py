# -*- coding: utf-8 -*-
from . import front
from flask import render_template
from ..models import Config
from flask_login import login_required


@front.route('/')
@login_required
def index():
    web_title = Config.query.filter_by(key='title').first()
    from ..models import Article
    this_page = Article.query.get(1)
    return render_template('index.html', page_name='index', this_page=this_page, web_title=web_title)



