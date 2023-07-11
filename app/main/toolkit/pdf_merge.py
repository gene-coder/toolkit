# _*_ coding:utf-8 _*_
# pdf转图片

import os
import PyPDF3
from flask import render_template, request, send_file
from app.main.toolkit import toolkit


@toolkit.route('/pdf_merge')
def pdf_merge():
    return render_template("/page/pdf_merge.html")


# 图片上传
@toolkit.route('/pdf_merge/upload', methods=['POST', 'GET'])
def pdf_merge_upload():
    if request.method == 'POST':

        # 获取上传信息
        uuid = request.form['uuid']
        files =  request.files.getlist('file')
        
        # 新建文件夹
        dir_name = r'./app/files/templefile/pdf_merge'
        if not os.path.exists(dir_name):  # 如果文件夹不存在，则新建
            os.makedirs(dir_name)
        else:
            pass
        
        # 将上传的图片放到转换成pdf，并放到目录中
        for file in files:
            file_name=file.filename
            file.save("{}/{}_{}".format(dir_name,uuid,file_name))
    return {'status': 'OK'}



# 合并文件
@ toolkit.route('/pdf_merge/merge',methods=['POST', 'GET'])
def pdf_merge_merge():
    if request.method == 'POST':
        uuid = request.form["uuid"]
        file_order =  request.form.get('file_order').split(',')

        merger = PyPDF3.PdfFileMerger()

        # 添加要合并的 PDF 文件
        for file in file_order:
            print(file)
            merger.append(open(r'./app/files/templefile/pdf_merge/{}_{}'.format(uuid,file), 'rb'))


        # 保存合并后的 PDF 文件
        with open(r'./app/files/templefile/pdf_merge/{}.pdf'.format(uuid), 'wb') as output_pdf:
            merger.write(output_pdf)

    return  {'status': 'OK', "uuid":uuid}



# 图片下载
@ toolkit.route('/pdf_merge/download/<file_name>')
def pdf_merge_download_file(file_name):
    # 去掉，as_attachment=True 会在线预览
    return send_file('./files/templefile/pdf_merge/{}.pdf'.format(file_name),as_attachment=True)
