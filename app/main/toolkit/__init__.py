# _*_ coding:utf-8 _*_

import json
from flask import Blueprint,render_template


toolkit = Blueprint("toolkit", __name__)

# 首页 按照类型筛选
@toolkit.route('/index/<search_type>/<type>')
def index(search_type,type):
    with open(r'./app/conf/all_web.json',encoding='utf-8') as f:
        all_web = json.load(f)
    files=[]
    if search_type == 'nav':
        dict_type = {'all':'','time':'时间','image':'图片','document':'文档'}
        type_name = dict_type[type]
        for k in all_web:
            if type_name:
                if all_web[k]['type']==type_name:
                    files.append(all_web[k])
            else:
                files.append(all_web[k])
    elif search_type == 'search':
        for k in all_web:
            if type:
                if type in all_web[k]['webname'] or type in all_web[k]['remark']:
                    files.append(all_web[k])
            else:
                files.append(all_web[k])
    return render_template("/index.html",navs=files)


# 时间
import app.main.toolkit.timestamp  # 时间戳转换
import app.main.toolkit.timediff  # 计算时间差

# 文档
import app.main.toolkit.pdf_to_pic # pdf转图片
import app.main.toolkit.pic_to_pdf # 图片转pdf
import app.main.toolkit.pdf_merge # 合并pdf
import app.main.toolkit.pdf_intercept # 分割pdf
import app.main.toolkit.pdf_add_pagenumber # pdf添加页码

# 图片
import app.main.toolkit.pic_cropper # 图片分割
import app.main.toolkit.pic_merge   # 图片拼接
import app.main.toolkit.pic_signature # 生成签名 