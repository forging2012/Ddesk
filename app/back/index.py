# -*- coding: utf-8 -*-
"""
__author__ = 'Zhipeng Du'
__mtime__ = '16/8/31' '16:13'
"""
from app import app
from . import back
from flask import render_template, redirect, url_for, send_from_directory, request
from flask_login import login_required


@back.route('/')
@login_required
def index():
    return render_template('back/index.html')


@back.route('/robots.txt')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])