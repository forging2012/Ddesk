# -*- coding: utf-8 -*-
"""
__author__ = 'Zhipeng Du'
__mtime__ = '16/9/1' '18:27'
"""
from . import back
from flask import redirect, url_for


@back.route('/login')
def login():
    return redirect(url_for('admin.login'))