*****************��ӭ���������Ľ��������****************

-------------------------------------------------------------web����Ӧ��-v0.1
Wed Sep 19 2018 23:25:23 GMT+0800 (�й���׼ʱ��)
------------------------------
��ϰ�����ƣ�����BBS+BLOGϵͳ
------------------------------
��ϰ����֪ʶ�㣺HTML+CSS+jQuery+bootstrap+Django
------------------------------
��ϰʵ�ֵĹ��ܣ�1.����ajax���û���֤���ʵ�ֵ�½��֤
		2.����ajax��form���ʵ��ע�Ṧ��
		3.ϵͳ��ҳ�����б����Ⱦ
		4.����վ��ҳ�����
		5.������ϸҳ�ļ̳�
		6.���������
		7.���۹���
		8.���ı��Ȼ�����ʹ��
		9.��ֹxss����
		10.�޸�����
----------------------------------------------------------------------------------------
***************************************ʹ��ǰ��֪***************************************
���л���
	1��IDE:pycharm2018.1.3רҵ��
		python3.6.5
		Django2.1
		pyMySQL0.9.2
		jquery3.2.1
		bootstrap3.3.7
		kindeditor4.1.11 �ı��༭��
				

	2�����ݿ����:MySQL-->version:5.6.40

	3) �����:�ȸ������

----------------------------------------------------------------------------------------
���¶���ʹ�ã�127.0.0.1:8000/ ����ʾ˵��

1����Ŀ�ļ�����	myblog��
2����ҳ���ַ��127.0.0.1:8000/index/��
3������������ݵ�ַ��127.0.0.1:8000
----------------------------------------------------------------------------------------
��������

1���������ݿ⣬�������ļ�
2������Django���ݿ����ӣ�Django��Ŀ�ļ���BM----->settings----->�ҵ�DATABASES���������ݿ��ַ���������˺����������
3��Ǩ�����ݿ⣬
4������Django
5������������ݣ���ַ������localhost:�˿ںţ�����-->127.0.0.1:8000,����ҳ�����������ݣ���������ʱ���ʱ�����������ĵȴ�
6��ע���˺Ž��е�¼������ʹ�ò��������˺�
�˺�Jacob����123456
----------------------------------------------------------------------------------------
��ĿĿ¼
����blog
��  ��  admin.py
��  ��  apps.py
��  ��  models.py   	ģ��
��  ��  myforms.py	formsУ�����
��  ��  myPaginator.py	��ҳ��
��  ��  tests.py
��  ��  urls.py		·��
��  ��  views.py	��ͼ����
��  ��  __init__.py
��  ��  
��  ��          
��  ����templatetags	�Զ����ǩ�ļ���
��  ��  ��  my_tags.py	�Զ����ǩ
��  ��  ��  __init__.py
��  ��  ��  
��  ��          
��  ����utils	�Զ��幤���ļ���
��  ��  ��  loaditer.py		��ȡ�ļ����ݵ�������������ȡ��������
��  ��  ��  valid_code.py	������֤��
��  ��  ��  __init__.py

��          
����media	�û��ϴ�ý���ļ�
��  ��  __init__.py
��  ��      
��  ����avatars	�û�ͷ���ļ�
��          default.jpg
��          default.png
��          timg.jpg
��          	
����myblog	
��  ��  settings.py	��Ŀ��������
��  ��  urls.py
��  ��  wsgi.py
��  ��  __init__.py
����static	��̬�ļ��ļ���
��  ��  __init__.py
��  ��  
��  ����blog	������ؾ�̬�ļ�
��  ��  ��  __init__.py
��  ��  ��  
��  ��  ����css
��  ��  ��      back.css 	��̨ģ��css
��  ��  ��      blog_base.css	����ҳ��ģ��css
��  ��  ��      home_base_site.css	����վ��ģ��css
��  ��  ��      index.css	��ҳģ��css
��  ��  ��      set_password.css	�޸�����ģ��css
��  ��  ��      __init__.py
��  ��  ��      
��  ��  ����js
��  ��  ��      back.js		��̨ģ��js
��  ��  ��      blog.js		����baseģ��js
��  ��  ��      home_base.js	����ҳ��ģ��js
��  ��  ��      set_password.js �޸�����ģ��js
��  ��  ��      __init__.py
��  ��  ��      
��  ��  ����pic ģ��ͼƬ
��  ��          b.png
��  ��          cent_secant_4_1.gif
��  ��          default.jpg
��  ��          downdown.gif
��  ��          icon_addcomment.gif
��  ��          icon_form.gif
��  ��          img.gif
��  ��          indent.png
��  ��          InsertCode.gif
��  ��          lk.png
��  ��          pinglun_line.gif
��  ��          quote.gif
��  ��          title-yellow.png
��  ��          upup.gif
��  ��          __init__.py
��  ��          
��  ����bootstrap 	
��  ��  ��  __init__.py
��  ����font
��  ��      hero.ttf
��  ��      __init__.py
��  ��      
��  ����js
��  ��      jquery-3.2.1.min.js
��  ��      session.js
��  ��      __init__.py
��  ��      
��  ����kindeditor	�༭��
��  ��  ��  kindeditor-all-min.js
��  ����pic
��  ��      favicon.png
��  ��      timg.gif
��  ��      __init__.py
��  ��      
��  ����test_data	��������
��          blog
��          category
��          content
��          tag
��          user
��          web_site_category
��          __init__.py
��          
����templates	ģ��
    ��  article_detail.html
    ��  base.html
    ��  classification.html
    ��  delete_model.html
    ��  home_base.html
    ��  home_site.html
    ��  index.html
    ��  login.html
    ��  not_found.html
    ��  no_article.html
    ��  register.html
    ��  
    ����back_stage
            add_article.html
            back_base.html
            back_stage.html
            editor_article.html
            set_password.html
            __init__.py
            
