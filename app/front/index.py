# -*- coding: utf-8 -*-
from app import app
from . import front
from flask import render_template, request, send_from_directory
from ..models import Config


web_title = Config.query.filter_by(key='title').first()


@front.route('/')
def index():
    from ..models import Page
    this_page = Page.query.get_or_404(1)
    return render_template('index.html', page_name='index', this_page=this_page, web_title=web_title)


@front.route('/robots.txt')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])
