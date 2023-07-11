# _*_ coding:utf-8 _*_
# pdf转图片

import os
from io import BytesIO
from PIL import Image
import img2pdf
import PyPDF3
from flask import render_template, request, send_file
from app.main.toolkit import toolkit


@toolkit.route('/pic_to_pdf')
def pic_to_pdf():
    return render_template("/page/pic_to_pdf.html")


# 上传
@toolkit.route('/pic_to_pdf/upload', methods=['POST', 'GET'])
def pic_to_pdf_upload():
    if request.method == 'POST':

        # 获取上传信息
        uuid = request.form['uuid']
        files =  request.files.getlist('file')
        
        # 新建文件夹
        dir_name = r'./app/files/templefile/pic_to_pdf'
        if not os.path.exists(dir_name):  # 如果文件夹不存在，则新建
            os.makedirs(dir_name)
        else:
            pass
        
        # 将上传的图片放到转换成pdf，并放到目录中
        for file in files:
            file_name=file.filename
            img = Image.open(file)
            img_bytes = BytesIO()
            if file_name.endswith('.png'):
                img = img.convert('RGB')
            img.save(img_bytes, format='JPEG')
            img_bytes.seek(0)
            with open("{}/{}_{}".format(dir_name,uuid,file_name),"wb") as f:
                f.write(img2pdf.convert(img_bytes))
    return {'status': 'OK'}



# 合并文件
@ toolkit.route('/pic_to_pdf/merge',methods=['POST', 'GET'])
def pic_to_pdf_merge():
    if request.method == 'POST':
        uuid = request.form["uuid"]
        file_order =  request.form.get('file_order').split(',')

        merger = PyPDF3.PdfFileMerger()

        # 添加要合并的 PDF 文件
        for file in file_order:
            merger.append(open(r'./app/files/templefile/pic_to_pdf/{}_{}'.format(uuid,file), 'rb'))


        # 保存合并后的 PDF 文件
        with open(r'./app/files/templefile/pic_to_pdf/{}.pdf'.format(uuid), 'wb') as output_pdf:
            merger.write(output_pdf)

    return  {'status': 'OK', "uuid":uuid}



# 图片下载
@ toolkit.route('/pic_to_pdf/download/<file_name>')
def pic_to_pdf_download_file(file_name):
    # 去掉，as_attachment=True 会在线预览
    return send_file('./files/templefile/pic_to_pdf/{}.pdf'.format(file_name),as_attachment=True)
