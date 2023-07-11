# _*_ coding:utf-8 _*_
# pdf转图片

import uuid
import time
import os
import zipfile
from io import BytesIO
from flask import render_template, request, send_file
from app.main.toolkit import toolkit
from pdf2image import convert_from_bytes


@toolkit.route('/pdf_to_pic')
def pdf_to_pic():
    return render_template("/page/pdf_to_pic.html")


# 图片上传
@toolkit.route('/pdf_to_pic/upload', methods=['POST', 'GET'])
def pdf_to_pic_upload():
    if request.method == 'POST':
        starttime= time.time()
        file = request.files['file']

        # 新建文件夹
        dir_name = r'./app/files/templefile/pdf_to_pic'
        if not os.path.exists(dir_name):  # 如果文件夹不存在，则新建
            os.makedirs(dir_name)
        else:
            pass
        # 确定压缩文件名称
        save_time = time.strftime('%Y%m%d%H%M%S', time.localtime())
        file_id = str(uuid.uuid4()).split('-')[0]
        file_name = file.filename.split('.')[0]
        zip_filename = r'./app/files/templefile/pdf_to_pic/{}_{}_{}.zip'.format(
            file_name, save_time, file_id)

        # 将 PDF 文件转换为图像列表
        images = convert_from_bytes(file.read())
        

        # 图片保存到zip文件中
        f = zipfile.ZipFile(zip_filename, 'a', zipfile.ZIP_DEFLATED)
        for i, img in enumerate(images):
            img_bytes = BytesIO()
            img.save(img_bytes, format='JPEG')
            f.writestr(f'page_{i+1}.jpg', img_bytes.getvalue())
            img_bytes.close()
        f.close()
        endtime = time.time()
    return {'status': 'OK', "filename": file.filename, "page_number": len(images),
            "zip_filename": '{}_{}_{}.zip'.format(file_name, save_time, file_id),"interval":int(endtime-starttime) }


# 图片下载
@ toolkit.route('/pdf_to_pic/download/<file_name>')
def pdf_to_pic_download_file(file_name):
    return send_file('./files/templefile/pdf_to_pic/'+ file_name)
