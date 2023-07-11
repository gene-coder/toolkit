# _*_ coding:utf-8 _*_
# pdf转图片

import uuid
import time
import os
import PyPDF3
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from io import BytesIO
from flask import render_template, request, send_file
from app.main.toolkit import toolkit



@toolkit.route('/pdf_add_pagenumber')
def pdf_add_pagenumber():
    return render_template("/page/pdf_add_pagenumber.html")


# 图片上传
@toolkit.route('/pdf_add_pagenumber/upload', methods=['POST', 'GET'])
def pdf_add_pagenumber_upload():
    if request.method == 'POST':
        file = request.files['file']

        # 新建文件夹
        dir_name = r'./app/files/templefile/pdf_add_pagenumber'
        if not os.path.exists(dir_name):  # 如果文件夹不存在，则新建
            os.makedirs(dir_name)
        else:
            pass
        
        # 确定文件名称
        save_time = time.strftime('%Y%m%d%H%M%S', time.localtime())
        file_id = str(uuid.uuid4()).split('-')[0]
        file_name = file.filename.split('.')[0]
        res_name = r'./app/files/templefile/pdf_add_pagenumber/{}_{}_{}.pdf'.format(
            file_name, save_time, file_id)


        # 获取表单数据
        pdf_min = int(request.form["pdf_min"])
        pdf_max = int(request.form["pdf_max"])
        startnumber = request.form.get("startnumber")  
        position = request.form.get('position')
        format = int(request.form.get("format"))  

        
        # 读取pdf
        pdf_reader = PyPDF3.PdfFileReader(BytesIO(file.read()))
        pdf_writer = PyPDF3.PdfFileWriter()
        num_pages = pdf_reader.getNumPages()

        # 防止写的页面过多
        pdf_min = num_pages if pdf_min > num_pages else pdf_min
        pdf_max = num_pages if pdf_max > num_pages else pdf_max
        

        # 遍历PDF页面
    for page_num in range(num_pages):
        # 设置宋体字体
        pdfmetrics.registerFont(TTFont('SimSun', r'.\simsun.ttc'))
        # 获取当前页面
        current_page = pdf_reader.getPage(page_num)
        if page_num in range(pdf_min -1 ,pdf_max):
            
            # 获取当前页面的大小
            page_width = current_page.mediaBox.getWidth()
            page_height = current_page.mediaBox.getHeight()
            
            # 创建一个PDF文件缓冲区
            packet = BytesIO()
            
            # 创建一个Canvas对象,并添加文字
            can = canvas.Canvas(packet, pagesize=current_page.mediaBox)
            can.setFont("SimSun", 8)
            # 在Canvas上添加文本
            if int(format) == 0:
                text = '{}'.format(int(startnumber) + page_num - int(pdf_min) + 1)
            elif int(format) == 1:
                text = '-{}-'.format(int(startnumber) + page_num - int(pdf_min) + 1)
            elif int(format) == 2:
                text = '第{}页'.format(int(startnumber) + page_num - int(pdf_min) + 1)
            elif int(format) == 3:
                text = '{}/{}'.format(int(startnumber) + page_num - int(pdf_min) + 1,num_pages)
            elif int(format) == 4:
                text = '第{}页/共{}页'.format(int(startnumber) + page_num - int(pdf_min) + 1,num_pages)
            else:
                pass

            # 确定添加文本的位置
            if int(position) in [0,1,2]:
                position_y = float(page_height) * 0.97
            else:
                position_y = float(page_height) * 0.03
            
            if int(position) in [0,3]:
                position_x = float(page_width) * 0.05
            elif int(position) in [1,4]:
                position_x = float(page_width) /2
            else:
                position_x = float(page_width) * 0.95
            can.drawCentredString(int(position_x), int(position_y), text)

            # 保存Canvas内容
            can.save()

            # 移动到初始位置并读取缓冲区内容
            packet.seek(0)
            new_pdf = PyPDF3.PdfFileReader(packet)

            # 将新页面合并到当前页面中
            current_page.mergePage(new_pdf.getPage(0))

        # 将本页添加到页面中
        pdf_writer.addPage(current_page)
    
    with open(res_name, 'wb') as f2:
            pdf_writer.write(f2)

    return {'status': 'OK', "filename": r'{}_{}_{}.pdf'.format(file_name, save_time, file_id), "page_number": num_pages, 
            "res_name": '{}_{}_{}.pdf'.format(file_name, save_time, file_id) }


# 图片下载
@ toolkit.route('/pdf_add_pagenumber/download/<file_name>')
def pdf_add_pagenumber_download_file(file_name):
    return send_file('./files/templefile/pdf_add_pagenumber/'+ file_name ,as_attachment=True)
