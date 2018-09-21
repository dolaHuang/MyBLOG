#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/31 19:56
# @Author  : DollA
# @Site    : 
# @File    : myPaginator.py
# @Software: PyCharm
from django.core.paginator import Paginator


# Create your views here.


def paginator(request, obj_list):
    """

    :param request:
    :return:
    """
    # 生成分页器对象
    paginator = Paginator(obj_list, 8)
    # 获取浏览器端请求的页码,需要设置默认值
    current_page_num = int(request.GET.get('page', 1))
    # 当前页的所有书对象
    current_page = paginator.page(current_page_num)
    # 页码列表，可迭代
    # 分页过多，需要用条件判断显示的页码
    if paginator.num_pages > 11:  # 11就是显示的固定个数
        if current_page_num - 5 < 1:  # 接近最小页码时，固定页码，否则会出现负数
            page_range = range(1, 12)
        elif current_page_num + 5 > paginator.num_pages:  # 接近最大页码时，根据最大页码限制页码数，否则会出现不存在的页码
            page_range = range(paginator.num_pages - 10, paginator.num_pages + 1)
        else:
            page_range = range(current_page_num - 5, current_page_num + 6)  # 其他情况，显示当前的挨着的几个
    else:
        page_range = paginator.page_range  # 页码总数不足时，显示全部，即不会超宽

    return current_page, page_range
