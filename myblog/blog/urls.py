"""myblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('bootstrap/', include('bootstrap.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from blog import views

urlpatterns = [
    # 修改密码
    re_path('set_password/', views.set_password),
    # 插入测试数据
    path('inster_test_data/', views.inster_test_data),
    path('login/', views.login),
    path('index/', views.index),
    path('get_img/', views.get_valid_img),
    path('register/', views.register),
    re_path(r'^$', views.inster_waiting),
    path('logout/', views.logout),

    # 获取评论列表
    path('get_conmment_tree/', views.get_conmment_tree),
    # 评论
    path('conmment/', views.conmment),
    # 点赞, 放在下面会出错，凡在这里正常，会返回找不到站点页面的not_found页面
    path('digg/', views.digg),
    # 后台管理
    path('back_stage/', views.back_stage),
    path('add_article/', views.add_article),
    path('upload/', views.upload),
    path('article/<int:id>/delete',views.delete_article),
    path('article/<int:id>/editor',views.editor_article),
    path('add_new_condition/',views.add_new_condition),
    # 主页站点分类文章
    path('index/<int:cate>/',views.index),
    # 个人站点URL
    re_path(r'^(?P<username>\w+)/$', views.home_site),
    # 个人站点中的跳转
    re_path(r'^(?P<username>\w+)/(?P<conditon>tag|category|archive)/(?P<param>.*)/$', views.home_site),
    # 文章详情页
    re_path(r'^(?P<username>\w+)/articles/(?P<article_id>\d+)/$', views.article_detail),
]
