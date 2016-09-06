# -*- coding: utf-8 -*-
"""
__author__ = 'Zhipeng Du'
__mtime__ = '16/9/6' '14:11'
"""
from . import back
from flask_login import login_required
from flask import render_template, redirect, url_for, flash
from ..models import db, Demand, Admin, Tag, Issue
from app import config, alidayu


@back.route('/demand')
@login_required
def demand():
    status_code = request.args.get('status')
    if status_code == 'end':
        all_demand = Demand.query.filter(Demand.status > 9).all()
    else:
        all_demand = Demand.query.filter(Demand.status < 10).all()
    return render_template('admin/demand.html', all_demand=all_demand, DEMAND_STATUS=config.DEMAND_STATUS,
                           status_code=status_code, Tag=Tag)
