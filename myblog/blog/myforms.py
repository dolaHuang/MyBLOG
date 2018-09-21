#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/9 20:32
# @Author  : DollA
# @File    : myforms.py
# @Software: PyCharm

from django import forms
from django.forms import widgets
from django.core.exceptions import ValidationError
from blog.models import *


# 注册forms组件
class RegForm(forms.Form):
    username = forms.CharField(max_length=32, min_length=4,
                               label='用户名',
                               widget=widgets.TextInput(attrs={"class": "form-control", 'placeholder': "登录用户名，不小于4位"}),
                               error_messages={"required": "用户不能为空", "min_length": "用户名最小长度4位"})
    password = forms.CharField(min_length=6,
                               label='密码',
                               widget=widgets.PasswordInput(
                                   attrs={"class": "form-control", 'placeholder': "请输入登陆密码，不小于6位"}),
                               error_messages={"required": "密码不能为空",
                                               "min_length": "密码最小长度6位",
                                               })
    password_r = forms.CharField(label='确认密码',
                                 widget=widgets.PasswordInput(
                                     attrs={"class": "form-control", 'placeholder': "请输入确认密码"}),
                                 error_messages={"required": "密码不能为空", "min_length": "密码最小长度6位", })
    email = forms.EmailField(label='邮箱',
                             widget=widgets.EmailInput(attrs={"class": "form-control", 'placeholder': "用于激活账户"}),
                             error_messages={"required": "邮箱不能为空", 'invalid': '邮箱格式错误'})

    tel = forms.CharField(label='手机号码', error_messages={'required': '电话不能为空'},
                          widget=widgets.TextInput(attrs={'class': 'form-control', 'placeholder': "用于激活账户"}))
    blog_name = forms.CharField(max_length=32, min_length=4,
                                label='博客名称',
                                widget=widgets.TextInput(attrs={"class": "form-control", 'placeholder': "即显示在博客的昵称"}),
                                error_messages={"required": "用户不能为空", "min_length": "用户名最小长度4位"})

    # 验证密码重复
    def clean(self):
        pwd = self.cleaned_data.get("password")
        pwd_r = self.cleaned_data.get("password_r")
        if pwd and pwd_r:
            if pwd == pwd_r:
                return self.cleaned_data
            else:
                raise ValidationError("两次密码不一致")
        else:
            return self.cleaned_data

    # 验证用户名是否已存在
    def clean_username(self):
        user = self.cleaned_data.get('username')
        user_ret = UserInfo.objects.filter(username=user).first()
        if user_ret:
            raise ValidationError('该用户已注册')
        else:
            return user

    # 验证博客名是否已存在
    def clean_blog_name(self):
        blog_name = self.cleaned_data.get('blog_name')
        user_ret = Blog.objects.filter(title=blog_name).first()
        if user_ret:
            raise ValidationError('该博客名已被使用')
        else:
            return blog_name

    # 验证电话是否合法
    def clean_tel(self):
        val = self.cleaned_data.get('tel')
        if len(val) == 11 and val.isdigit():
            return val
        else:
            raise ValidationError('请输入11位电话号码')


# 添加文章校验
class ArticleForm(forms.Form):
    title = forms.CharField(min_length=1, max_length=32, error_messages={
        'required': '文章标题不能为空', 'max_length': '标题最长32位'})
    content = forms.CharField(min_length=1, error_messages={'required': '文章内容不能为空'})


# 修改密码forms组件
class Set_Password(forms.Form):
    old_password = forms.CharField(min_length=6,
                                   label='密码',
                                   widget=widgets.PasswordInput(
                                       attrs={"class": "form-control", 'placeholder': "请输入登陆密码，不小于6位"}),
                                   error_messages={"required": "旧密码不能为空",
                                                   "min_length": "密码最小长度6位",
                                                   })
    new_password = forms.CharField(min_length=6,
                                   label='密码',
                                   widget=widgets.PasswordInput(
                                       attrs={"class": "form-control", 'placeholder': "请输入登陆密码，不小于6位"}),
                                   error_messages={"required": "新密码不能为空",
                                                   "min_length": "密码最小长度6位",
                                                   })
    new_password_r = forms.CharField(label='确认密码',
                                     widget=widgets.PasswordInput(
                                         attrs={"class": "form-control", 'placeholder': "请输入确认密码"}),
                                     error_messages={"required": "确认密码不能为空", "min_length": "密码最小长度6位", })

    # 验证密码重复
    def clean(self):
        pwd_old = self.cleaned_data.get('old_password')
        pwd_n = self.cleaned_data.get("new_password")
        pwd_n_r = self.cleaned_data.get("new_password_r")
        if pwd_old and pwd_n:
            if pwd_old == pwd_n:
                raise ValidationError("新密码不能和旧密码一样")
            else:
                if pwd_n_r:
                    if pwd_n_r == pwd_n:
                        return self.cleaned_data
                    else:
                        raise ValidationError("新密码和确认密码不一致")
        else:
            return self.cleaned_data
