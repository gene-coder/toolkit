# _*_ coding:utf-8 _*_
# pdf转图片

import os
from PIL import Image
import math
from flask import render_template, request, send_file
from app.main.toolkit import toolkit


@toolkit.route('/pic_merge')
def pic_merge():
    return render_template("/page/pic_merge.html")


# 上传
@toolkit.route('/pic_merge/upload', methods=['POST', 'GET'])
def pic_merge_upload():
    if request.method == 'POST':

        # 获取上传信息
        uuid = request.form['uuid']
        files =  request.files.getlist('file')
        
        # 新建文件夹
        dir_name = r'./app/files/templefile/pic_merge'
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
@ toolkit.route('/pic_merge/merge',methods=['POST', 'GET'])
def pic_merge_merge():
    if request.method == 'POST':
        dir_name = r'./app/files/templefile/pic_merge'
        row_num = int(request.form["row_num"])
        uuid = request.form["uuid"]
        file_order =  request.form.get('file_order').split(',')
        print(uuid,file_order)
        pic_num = len(file_order)

        # 新建底图，不判断图片张数与要求行数的数量关系
        with Image.open("{}/{}_{}".format(dir_name,uuid,file_order[0])) as pic:
            pic_size_x = pic.size[0]
            pic_size_y = pic.size[1]

        base_img_x = pic_size_x * row_num
        base_img_y = pic_size_y * math.ceil(pic_num / row_num)
        base_img = Image.new('RGB',(base_img_x,base_img_y),(255,255,255))

        # 粘贴图片
        
        for pic in range(0,pic_num):
            location_x = pic % row_num * pic_size_x
            location_y = pic // row_num * pic_size_y
            box_pic = (location_x, location_y, location_x + pic_size_x, location_y + pic_size_y)
            with Image.open("{}/{}_{}".format(dir_name,uuid,file_order[pic])) as pic_read:
                pic_read = pic_read.resize((pic_size_x,pic_size_y))
                base_img.paste(pic_read, box_pic)


        base_img.save(r'{}/{}.png'.format(dir_name,uuid) )

    return  {'status': 'OK', "uuid":uuid}



# 图片下载
@ toolkit.route('/pic_merge/download/<file_name>')
def pic_merge_download_file(file_name):
    # 去掉，as_attachment=True 会在线预览
    return send_file('./files/templefile/pic_merge/{}.png'.format(file_name),as_attachment=True)
