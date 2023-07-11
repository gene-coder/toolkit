# _*_ coding: utf-8 _*_
# 时间戳转换

from flask import render_template
from app.main.toolkit import toolkit


@toolkit.route('/timestamp')
def timestamp():
    return render_template("/page/timestamp.html")
