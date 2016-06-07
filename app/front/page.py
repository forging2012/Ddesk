# -*- coding: utf-8 -*-
from . import front
from flask import render_template, request


@front.route('/page')
def page():
    from ..models import Page
    this_page = Page.query.get_or_404(request.args.get('page_id'))
    return render_template('page.html', this_page=this_page)
