# _*_ coding:utf-8 _*_
# pdf转图片

import uuid
import time
import os
import PyPDF3
from io import BytesIO
from flask import render_template, request, send_file
from app.main.toolkit import toolkit



@toolkit.route('/pdf_intercept')
def pdf_intercept():
    return render_template("/page/pdf_intercept.html")


# 图片上传
@toolkit.route('/pdf_intercept/upload', methods=['POST', 'GET'])
def pdf_intercept_upload():
    if request.method == 'POST':
        file = request.files['file']

        # 新建文件夹
        dir_name = r'./app/files/templefile/pdf_intercept'
        if not os.path.exists(dir_name):  # 如果文件夹不存在，则新建
            os.makedirs(dir_name)
        else:
            pass
        
        # 确定压缩文件名称
        save_time = time.strftime('%Y%m%d%H%M%S', time.localtime())
        file_id = str(uuid.uuid4()).split('-')[0]
        file_name = file.filename.split('.')[0]
        res_name = r'./app/files/templefile/pdf_intercept/{}_{}_{}.pdf'.format(
            file_name, save_time, file_id)

        # 获取表单数据
        pdf_min = int(request.form["pdf_min"])
        pdf_max = int(request.form["pdf_max"])   
        
        # pdf 截取
        pdf_reader = PyPDF3.PdfFileReader(BytesIO(file.read()))
        pdf_writer = PyPDF3.PdfFileWriter()
        num_pages = pdf_reader.getNumPages()

        # 防止写的页面过多
        pdf_min = num_pages if pdf_min > num_pages else pdf_min
        pdf_max = num_pages if pdf_max > num_pages else pdf_max
        

        for page in range(pdf_min -1 , pdf_max):
                pdf_writer.addPage(pdf_reader.getPage(page))
        with open(res_name, 'wb') as f2:
                pdf_writer.write(f2)
    return {'status': 'OK', "filename": r'{}_{}_{}.pdf'.format(file_name, save_time, file_id), "page_number": num_pages, "intercept":pdf_max - pdf_min + 1,
            "res_name": '{}_{}_{}.pdf'.format(file_name, save_time, file_id) }


# 图片下载
@ toolkit.route('/pdf_intercept/download/<file_name>')
def pdf_intercept_download_file(file_name):
    return send_file('./files/templefile/pdf_intercept/'+ file_name)
