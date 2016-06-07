# -*- coding: utf-8 -*-
from . import front
from flask import render_template, request, redirect, url_for


@front.route('/version')
def version():
    from ..models import Version
    all_line1_version = Version.query.filter_by(pro_line=1).order_by(Version.pub_time.desc()).all()
    all_line2_version = Version.query.filter_by(pro_line=2).order_by(Version.pub_time.desc()).all()
    return render_template('releases.html', all_line1_version=all_line1_version, all_line2_version=all_line2_version)
