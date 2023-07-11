# _*_ Coding:utf-8 _*_

from flask import Flask

def create_app():
    app = Flask(__name__)

    from app.main.toolkit import toolkit
    app.register_blueprint(toolkit,url_prefix='/toolkit') #工具箱


    return app
