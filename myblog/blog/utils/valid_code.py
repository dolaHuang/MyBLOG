#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/9 17:56
# @Author  : DollA
# @File    : valid_code.py
# @Software: PyCharm
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import random


# 返回随机颜色函数
def get_random_color():

    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


# 生成验证码
def get_valid_code(request):
    # 生成随机颜色，固定大小的图片
    img = Image.new('RGB', (270, 40), color=(get_random_color()))
    # 生成画笔对象
    draw = ImageDraw.Draw(img)
    # 生成字体对象，通过下载好的字体，设定字体大小
    hero_font = ImageFont.truetype('static/font/hero.ttf', size=40)
    # 定义验证码空字符串
    valid_code_str = ''
    for i in range(5):
        random_num = str(random.randint(0, 9))
        random_low_alpha = chr(random.randint(97, 122))
        random_upper_alpha = chr(random.randint(65, 90))
        random_char = random.choice([random_num, random_low_alpha, random_upper_alpha])
        # 文字写入图片
        draw.text((i * 50 + 30, 5), random_char, get_random_color(), font=hero_font)
        # 保存验证码字符串
        valid_code_str += random_char
        # 将验证码存储在session中
    request.session['valid_code_str'] = valid_code_str

    # 添加噪点和噪线
    width = 270
    height = 40
    # # 画线
    for i in range(1):
        x1 = random.randint(0, width)
        x2 = random.randint(0, width)
        y1 = random.randint(0, height)
        y2 = random.randint(0, height)
        draw.line((x1, y1, x2, y2), fill=get_random_color())
    # # 画点
    for i in range(1):
        draw.point([random.randint(0, width), random.randint(0, height)], fill=get_random_color())
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.arc((x, y, x + 4, y + 4), 0, 90, fill=get_random_color())

    # 内存空间对象
    f = BytesIO()
    img.save(f, 'png')
    data = f.getvalue()
    return data


