# -*- coding: utf-8 -*-
from . import front
from flask import render_template
from ..models import Version, Config


@front.route('/version')
def version():
    web_title = Config.query.filter_by(key='title').first()
    all_line1_version = Version.query.filter_by(pro_line=1).order_by(Version.pub_time.desc()).all()
    all_line2_version = Version.query.filter_by(pro_line=2).order_by(Version.pub_time.desc()).all()
    return render_template('releases.html', all_line1_version=all_line1_version, all_line2_version=all_line2_version,
                           web_title=web_title)
