# -*- coding: utf-8 -*-
from flask import Blueprint


front = Blueprint('front', __name__)


from . import index, question, demand, query, version, login, page
