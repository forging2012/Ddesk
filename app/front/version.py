# -*- coding: utf-8 -*-
from . import front
from flask import render_template, request
from ..models import Version, Config, Category


@front.route('/version')
def version():
    web_title = Config.query.filter_by(key='title').first()
    all_category = Category.query.filter_by(parents_id=3).all()
    line_id = request.args.get('id')
    if line_id:
        this_category = Category.query.get(int(line_id))
        all_tag = this_category.tag
    else:
        all_tag = 0
    return render_template('releases.html',
                           web_title=web_title, all_category=all_category, all_tag=all_tag, Version=Version)
