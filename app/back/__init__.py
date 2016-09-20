# -*- coding: utf-8 -*-
"""
__author__ = 'Zhipeng Du'
__mtime__ = '16/8/31' '16:03'
"""
from flask import Blueprint


back = Blueprint('back', __name__)

from . import config, user, question, login, demand, article, index
