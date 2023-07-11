# _*_ coding: utf-8 _*_
# 时间戳转换

from flask import render_template
from app.main.toolkit import toolkit


@toolkit.route('/timediff')
def timediff():
    return render_template("/page/timediff.html")
