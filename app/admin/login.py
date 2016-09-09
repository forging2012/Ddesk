# -*- coding: utf-8 -*-
from app.forms import AdminLoginForm
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user
from . import admin
from app import config


@admin.route('/login')
def login():
    return redirect(url_for('back.login'))



