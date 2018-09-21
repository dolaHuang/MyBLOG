*****************欢迎提出您宝贵的建议和批评****************

-------------------------------------------------------------web博客应用-v0.1
Wed Sep 19 2018 23:25:23 GMT+0800 (中国标准时间)
------------------------------
练习题名称：开发BBS+BLOG系统
------------------------------
练习所需知识点：HTML+CSS+jQuery+bootstrap+Django
------------------------------
练习实现的功能：1.基于ajax和用户认证组件实现登陆验证
		2.基于ajax和form组件实现注册功能
		3.系统首页文章列表的渲染
		4.个人站点页面设计
		5.文章详细页的继承
		6.点赞与踩灭
		7.评论功能
		8.富文本比机器的使用
		9.防止xss攻击
		10.修改密码
----------------------------------------------------------------------------------------
***************************************使用前必知***************************************
运行环境
	1）IDE:pycharm2018.1.3专业版
		python3.6.5
		Django2.1
		pyMySQL0.9.2
		jquery3.2.1
		bootstrap3.3.7
		kindeditor4.1.11 文本编辑器
				

	2）数据库软件:MySQL-->version:5.6.40

	3) 浏览器:谷歌浏览器

----------------------------------------------------------------------------------------
以下都将使用（127.0.0.1:8000/ ）演示说明

1、项目文件名：	myblog；
2、主页面地址：127.0.0.1:8000/index/；
3、插入测试数据地址：127.0.0.1:8000
----------------------------------------------------------------------------------------
启动流程

1、启动数据库，创建库文件
2、设置Django数据库连接：Django项目文件夹BM----->settings----->找到DATABASES，设置数据库地址，表名，账号密码等内容
3、迁移数据库，
4、启动Django
5、插入测试数据：地址栏输入localhost:端口号，例如-->127.0.0.1:8000,进入页面点击插入数据，插入数据时间耗时长，还请耐心等待
6、注册账号进行登录，或者使用测试数据账号
账号Jacob密码123456
----------------------------------------------------------------------------------------
项目目录
├─blog
│  │  admin.py
│  │  apps.py
│  │  models.py   	模型
│  │  myforms.py	forms校验组件
│  │  myPaginator.py	分页器
│  │  tests.py
│  │  urls.py		路由
│  │  views.py	视图函数
│  │  __init__.py
│  │  
│  │          
│  ├─templatetags	自定义标签文件夹
│  │  │  my_tags.py	自定义标签
│  │  │  __init__.py
│  │  │  
│  │          
│  ├─utils	自定义工具文件夹
│  │  │  loaditer.py		提取文件内容迭代器，用于提取测试数据
│  │  │  valid_code.py	生成验证码
│  │  │  __init__.py

│          
├─media	用户上传媒体文件
│  │  __init__.py
│  │      
│  └─avatars	用户头像文件
│          default.jpg
│          default.png
│          timg.jpg
│          	
├─myblog	
│  │  settings.py	项目参数配置
│  │  urls.py
│  │  wsgi.py
│  │  __init__.py
├─static	静态文件文件夹
│  │  __init__.py
│  │  
│  ├─blog	博客相关静态文件
│  │  │  __init__.py
│  │  │  
│  │  ├─css
│  │  │      back.css 	后台模板css
│  │  │      blog_base.css	博客页面模板css
│  │  │      home_base_site.css	个人站点模板css
│  │  │      index.css	主页模板css
│  │  │      set_password.css	修改密码模板css
│  │  │      __init__.py
│  │  │      
│  │  ├─js
│  │  │      back.js		后台模板js
│  │  │      blog.js		博客base模板js
│  │  │      home_base.js	博客页面模板js
│  │  │      set_password.js 修改密码模板js
│  │  │      __init__.py
│  │  │      
│  │  └─pic 模板图片
│  │          b.png
│  │          cent_secant_4_1.gif
│  │          default.jpg
│  │          downdown.gif
│  │          icon_addcomment.gif
│  │          icon_form.gif
│  │          img.gif
│  │          indent.png
│  │          InsertCode.gif
│  │          lk.png
│  │          pinglun_line.gif
│  │          quote.gif
│  │          title-yellow.png
│  │          upup.gif
│  │          __init__.py
│  │          
│  ├─bootstrap 	
│  │  │  __init__.py
│  ├─font
│  │      hero.ttf
│  │      __init__.py
│  │      
│  ├─js
│  │      jquery-3.2.1.min.js
│  │      session.js
│  │      __init__.py
│  │      
│  ├─kindeditor	编辑器
│  │  │  kindeditor-all-min.js
│  ├─pic
│  │      favicon.png
│  │      timg.gif
│  │      __init__.py
│  │      
│  └─test_data	测试数据
│          blog
│          category
│          content
│          tag
│          user
│          web_site_category
│          __init__.py
│          
└─templates	模板
    │  article_detail.html
    │  base.html
    │  classification.html
    │  delete_model.html
    │  home_base.html
    │  home_site.html
    │  index.html
    │  login.html
    │  not_found.html
    │  no_article.html
    │  register.html
    │  
    └─back_stage
            add_article.html
            back_base.html
            back_stage.html
            editor_article.html
            set_password.html
            __init__.py
            
