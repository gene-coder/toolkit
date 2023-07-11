# _*_ coding:utf-8 _*_
# pdf转图片

import base64
import io
from PIL import Image
from flask import render_template, request, send_file
from app.main.toolkit import toolkit


@toolkit.route('/pic_signature')
def pic_signature():
    return render_template("/page/pic_signature.html")


# 图片去底色
def rgba(im, img_r, img_b, img_g, limit):

    pixdata = im.load()
    for y in range(im.size[1]):
        for x in range(im.size[0]):
            if abs(pixdata[x, y][0] - img_r) > limit or abs(pixdata[x, y][1] - img_b) > limit or abs(pixdata[x, y][2] - img_g) > limit:
            # print(abs(pixdata[x, y][0] - img_r))
                pixdata[x, y] = (255, 255, 255, 0)
    # 将图片转为base64
    buffer = io.BytesIO()
    im.save(buffer, format='PNG')
    encoded_image = base64.b64encode(buffer.getvalue()).decode('ascii')
    base64_image = f"data:image/png;base64,{encoded_image}"
    return base64_image


# 图片上传
@toolkit.route('/pic_signature/upload', methods=['POST', 'GET'])
def pic_signature_upload():
    if request.method == 'POST':

        # 获取上传信息
        color = request.form['color']
        file = request.files['file']

        # 将颜色改成
        color = color.lstrip("#")
        r, g, b = int(color[:2], 16), int(color[2:4], 16), int(color[4:], 16)
        image = Image.open(file).convert('RGBA')
        pics = []
        for i in range(11,1,-1):
            pic=rgba(image, r, g, b, i * 20)
            pics.append(pic)
        image.close()

    return {'status': 'OK',"pics":pics}


# 图片下载
@ toolkit.route('/pic_signature/download/<file_name>')
def pic_signature_download_file(file_name):
    # 去掉，as_attachment=True 会在线预览
    return send_file('./files/templefile/pic_signature/{}.pdf'.format(file_name), as_attachment=True)
