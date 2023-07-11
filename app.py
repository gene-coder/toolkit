#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import  render_template,redirect
from app import create_app
app = create_app()


# 登入页面
@app.route('/')
def hello_world():
    return redirect('/toolkit/index/nav/all')


if __name__ == '__main__':

    app.run(host="0.0.0.0", port=8001, debug=True)
