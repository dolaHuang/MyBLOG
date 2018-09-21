#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/12 11:13
# @Author  : DollA
# @File    : my_tags.py
# @Software: PyCharm
from django import template
from django.db.models import Count
from django.db.models.functions import TruncMonth
from blog.models import *

register = template.Library()


# 主页获取分类、标签、归档数据
# inclustion_tag中引入模板，将数据和模板绑定在了一起
@register.inclusion_tag('classification.html')
def get_classification_style(username):
    user_obj = UserInfo.objects.filter(username=username).first()
    blog_obj = Blog.objects.filter(userinfo=user_obj).first()
    Category.objects.filter(blog=blog_obj).values('pk').annotate(c=Count('article__title'))
    # 文章分类列表
    cata_list = Category.objects.filter(blog=blog_obj).values('pk').annotate(c=Count('article__nid')).values_list('title','c')
    # 标签列表，用于渲染html
    tag_list = Tag.objects.filter(blog=blog_obj) \
        .values('pk').annotate(c=Count('article__nid')) \
        .values_list('title', 'c')
    # 归档时间列表
    date_list = Article.objects.filter(user=user_obj) \
        .annotate(month=TruncMonth('create_time')) \
        .values('month').annotate(c=Count('nid')) \
        .values_list('month', 'c')
    return {'username':username,'blog_obj': blog_obj, 'tag_list': tag_list, 'cata_list': cata_list, 'date_list': date_list}
