from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.contrib import auth
from django.db.models import Count, F, Sum
from django.db.models.functions import TruncMonth
from django.db import transaction
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from bs4 import BeautifulSoup
import json
import os
import random
from threading import Thread
from blog.utils import valid_code
from blog.myforms import *
from blog.models import *
from myblog import settings
from blog import myPaginator
from blog.utils.loaditer import fileiter


# Create your views here.


# 插入数据等待页面
def inster_waiting(requset):
    response={}
    if requset.method=='POST':
        print(123)
        inster_test_data(requset)
        response['state']=True
        return JsonResponse(response)

    return render(requset,'wait.html')


# 插入测试数据
def inster_test_data(request):
        path_web_site_category = 'static/test_data/web_site_category'
        path_blog = 'static/test_data/blog'

        # 插入站点分类
        web_site_category_list = []
        web_site_category_file_content = fileiter(path_web_site_category)
        for line in web_site_category_file_content:
            obj = Web_Site_Category(title=line.strip())
            web_site_category_list.append(obj)
        Web_Site_Category.objects.bulk_create(web_site_category_list)
        # 插入博客
        blog_list = []
        blog_file_content = fileiter(path_blog)
        for line in blog_file_content:
            line_list = line.split()
            obj = Blog(title=line_list[0], site_name=line_list[1], theme=line_list[2])
            blog_list.append(obj)
        Blog.objects.bulk_create(blog_list)
        # 插入用户
        path_user = 'static/test_data/user'
        pwd = '123456'
        user_file_content = fileiter(path_user)
        for line in user_file_content:
            line_list = line.split()
            UserInfo.objects.create_user(username=line_list[0], password=pwd, telephone=line_list[1], email=line_list[2],
                                         blog_id=line_list[3])

        # 插入文章分类
        category_list = []
        path_category = 'static/test_data/category'
        with open(path_category, 'r', encoding='utf8') as f:
            for i in range(1, 11):
                f.seek(0)
                for line in f:
                    line_list = line.split()
                    obj = Category(title=line_list[0], blog_id=i)
                    category_list.append(obj)
        Category.objects.bulk_create(category_list)
        # 插入标签分类
        tag_list = []
        path_tag = 'static/test_data/tag'
        with open(path_tag, 'r', encoding='utf8') as f:
            for i in range(1, 11):
                f.seek(0)
                for line in f:
                    line_list = line.split()
                    obj = Tag(title=line_list[0], blog_id=i)
                    tag_list.append(obj)
        Tag.objects.bulk_create(tag_list)
        # 插入文章
        path_content = 'static/test_data/content'
        article_list = []
        # 获取文章文本
        with open(path_content, 'r', encoding='utf8') as f:
            content = f.read()
        soup = BeautifulSoup(content, 'html.parser')
        desc = soup.text[0:100] + '...'
        # 插入测试文章
        for i in range(1, 400):
            obj = Article(title='测试文章%s' % i, content=str(content), desc=desc, user_id=random.randint(1, 10),
                          category_id=random.randint(1, 50), web_site_category_id=random.randint(1, 10))

            article_list.append(obj)
        Article.objects.bulk_create(article_list)
        # 插入article2tag
        a2t_list = []
        for i in range(1, 400):
            obj = Article2Tag(article_id=i, tag_id=random.randint(1, 50))
            a2t_list.append(obj)
        Article2Tag.objects.bulk_create(a2t_list)
        # return redirect('/index/')


# 修改密码
@login_required
def set_password(request):
    user = request.user
    response = {}
    print(request.POST)
    if request.method == 'POST':
        form = Set_Password(request.POST)
        if form.is_valid():
            old_password = request.POST.get('old_password')
            new_password = request.POST.get('new_password')
            new_password_r = request.POST.get('new_password_r')
            if user.check_password(old_password):
                    user.set_password(new_password)
                    user.save()
                    response['state']=True
                    return JsonResponse(response)
            else:
                response['msg'] = {'old_password':'密码错误'}

        else:
            response['msg'] = form.errors

        return JsonResponse(response)

    return render(request, 'back_stage/set_password.html', locals())


# 添加新分类和标签
def add_new_condition(request):
    response = {}
    condition_dict = {
        'category': [Category, '该文章分类已存在'],
        'tag': [Tag, '该文章标签已存在']
    }
    title = request.POST.get('title')
    condition = request.POST.get('conditon')
    response['conditon'] = condition
    res = condition_dict[condition][0].objects.filter(title=title)
    if res:
        response['state'] = False
        response['msg'] = condition_dict[condition][1]
        return JsonResponse(response)
    response['state'] = True
    condition_dict[condition][0].objects.create(title=title, blog_id=request.user.blog_id)
    return JsonResponse(response)


# 编辑文章
@login_required
def editor_article(request, id):
    article_content = list(Article.objects.filter(pk=id).values('content', 'title'))
    if request.method == "POST":
        response = {}
        # editor_state定义是否编辑文章
        editor_state = request.POST.get('editor')
        title = request.POST.get('title')
        content = request.POST.get('content')

        if editor_state:
            # 过滤非法标签
            soup = BeautifulSoup(content, 'html.parser')
            for tag in soup.find_all():
                if tag.name == 'script':
                    tag.decompose()
            Article.objects.filter(pk=id).update(title=title, content=str(soup))
            response['editor_state'] = True
        response['article'] = article_content
        return JsonResponse(response, safe=False)
    return render(request, 'back_stage/editor_article.html', locals())


# 删除文章
@login_required
def delete_article(request, id):
    # 该文章的评论和点赞
    with transaction.atomic():
        Comment.objects.filter(article_id=id).delete()
        ArticleUpDown.objects.filter(article_id=id).delete()
        Article2Tag.objects.filter(article_id=id).delete()
        Article.objects.filter(pk=id).delete()
    return redirect('/back_stage/')


# 后台管理
@login_required
def back_stage(request):
    article_list = Article.objects.filter(user=request.user)
    current_page, page_range = myPaginator.paginator(request, article_list)
    return render(request, 'back_stage/back_stage.html', locals())


# 添加新文章
@login_required
def add_article(request):
    # 获取各种标签列表，渲染选择框
    web_site_category_list = Web_Site_Category.objects.all()
    category_list = Category.objects.filter(blog_id=request.user.blog_id)
    tag_list = Tag.objects.filter(blog_id=request.user.blog_id)

    article_form = ArticleForm()

    if request.method == 'POST':
        response = {}
        # 校验标题和文章内容
        article_form = ArticleForm(request.POST)
        # print(article_form.cleaned_data)
        if article_form.is_valid():
            blog_id = request.user.blog_id
            title = request.POST.get('title')
            content = request.POST.get('content')
            category = request.POST.get('category')
            web_site_category = request.POST.get('web_site_category')
            tag_str_list = request.POST.getlist('tag')
            # 根据返回的数据获取标签对象，用于将文章插入数据库
            category_obj = Category.objects.filter(blog_id=blog_id, title=category).first()
            web_site_category_obj = Web_Site_Category.objects.filter(title=web_site_category).first()
            tag_obj_list = []
            # 返回的标签是个数组，需要循环，
            for tag in tag_str_list:
                obj = Tag.objects.filter(blog_id=blog_id, title=tag).first()
                tag_obj_list.append(obj)

            # 使用BeautifulSoup 解析内容拿出文本，去除script
            soup = BeautifulSoup(content, 'html.parser')
            # 过滤不合法内容
            for tag in soup.find_all():
                if tag.name == 'script':
                    tag.decompose()

            dsec = soup.text[0:150] + '...'
            with transaction.atomic():
                article_obj = Article.objects.create(title=title, content=str(soup), desc=dsec, user=request.user,
                                                     category=category_obj, web_site_category=web_site_category_obj)
                for tag_obj in tag_obj_list:
                    Article2Tag.objects.create(article=article_obj, tag=tag_obj)
            response['state'] = True
            return JsonResponse(response)
        else:
            response['msg'] = article_form.errors
            return JsonResponse(response)
    return render(request, 'back_stage/add_article.html', locals())


# 文章文件上传
def upload(request):
    img = request.FILES.get('up_load_img')

    path = os.path.join(settings.MEDIA_ROOT, 'add_article_img', img.name)
    with open(path, 'wb') as f:
        for line in img:
            f.write(line)

    response = {
        'error': 0,
        'url': '/media/add_article_img/%s' % img.name
    }

    return JsonResponse(response)


# 评论
@login_required
def conmment(request):
    response = {'msg': None}
    parent_id = request.POST.get('parent_id')
    article_id = request.POST.get('article_id')
    user = request.POST.get('user')
    conmment_content = request.POST.get('comment_content')
    article_obj = Article.objects.filter(pk=article_id).first()
    # 事务操作
    with transaction.atomic():
        res = Comment.objects.create(content=conmment_content, article_id=article_id, user_id=user,
                                     parent_comment_id=parent_id)
        # 文章表中刷新纪录
        Article.objects.filter(pk=article_id).update(comment_count=F('comment_count') + 1)

        if res:
            response['msg'] = True
            response['pk'] = res.nid
            response['avatar'] = str(request.user.avatar)
            response['content'] = res.content
            response['parent_comment_id'] = res.parent_comment_id
            response['user'] = res.user.username
            response['create_time'] = res.create_time.strftime('%Y-%m-%d %H:%M')
    # 发送邮件
    # 开启线程
    t = Thread(target=send_mail, args=(
        '您的文章%s新增了一条评论' % article_obj.title,
        conmment_content,
        settings.EMAIL_HOST_USER,
        ['471313931@qq.com']
    ))
    t.start()
    return JsonResponse(response)


# 获取评论树
def get_conmment_tree(request):
    article_id = request.GET.get('article_id')
    response = list(Comment.objects.filter(article_id=article_id).order_by('pk').values('pk',
                                                                                        'user__username',
                                                                                        'content',
                                                                                        'create_time__year',
                                                                                        'create_time__month',
                                                                                        'create_time__day',
                                                                                        'create_time__hour',
                                                                                        'create_time__minute',
                                                                                        'parent_comment',
                                                                                        'user__avatar'))
    return JsonResponse(response, safe=False)


# 点赞
@login_required
def digg(request):
    response = {'state': None, 'handle': None, 'msg': None}

    article_id = request.POST.get('article_id')
    is_up = json.loads(request.POST.get('is_up'))
    # 点赞人即是登录人
    user_id = request.user.pk

    # 判断是不是用户自己的文章
    res = Article.objects.filter(pk=article_id, user_id=user_id)
    if res:
        response['state'] = False
        response['msg'] = '不能操作自己的文章'
        return JsonResponse(response)
    # 判断当前文章id和登录人是不是在表中有记录，即是否操作过该文章
    obj = ArticleUpDown.objects.filter(article_id=article_id, user_id=user_id).first()
    if not obj:
        response['state'] = True
        with transaction.atomic():
            # 在表中生成记录
            ArticleUpDown.objects.create(user_id=user_id, article_id=article_id, is_up=is_up)
            # 同步到文章表中
            current_article = Article.objects.filter(pk=article_id)
            if is_up:
                current_article.update(up_count=F('up_count') + 1)
            else:
                current_article.update(down_count=F('down_count') + 1)
    else:
        response['state'] = False
        # 拿到之前该用户对改文章的的操作状态
        response['handle'] = obj.is_up

    return JsonResponse(response)


# 文章详情页
def article_detail(request, username, article_id):
    """
    1、左侧和顶部样式和个人站点一样
    使用模板继承，自定义标签来复用代码，并且使样式和数据一体
    :param request:
    :param username:
    :param article_id:
    :return:
    """
    user_obj = UserInfo.objects.filter(username=username).first()
    blog_obj = Blog.objects.filter(userinfo=user_obj).first()
    article_obj = Article.objects.filter(pk=article_id).first()
    return render(request, 'article_detail.html', locals())


# 获取分类、标签、归档数据的函数，也可以放在自定义标签中
def get_classification_data(username):
    user_obj = UserInfo.objects.filter(username=username).first()

    blog_obj = Blog.objects.filter(userinfo=user_obj).first()
    cata_list = Category.objects.filter(blog=blog_obj) \
        .values('pk').annotate(c=Count('article__title')) \
        .values_list('title', 'c')
    tag_list = Tag.objects.filter(blog=blog_obj) \
        .values('pk').annotate(c=Count('article')) \
        .values_list('blog__tag', 'c')

    date_list = Article.objects.filter(user=user_obj) \
        .annotate(month=TruncMonth('create_time')) \
        .values('month').annotate(c=Count('nid')) \
        .values_list('month', 'c')
    return {'blog_obj': blog_obj, 'tag_list': tag_list, 'cata_list': cata_list, 'date_list': date_list}


# 个人站点
def home_site(request, username, **kwargs):
    user_obj = UserInfo.objects.filter(username=username).first()
    # 不存在的用户，跳转到not_found页面
    if not user_obj:
        return render(request, 'not_found.html')
    # 当前站点对象，一对一的关系
    blog_obj = Blog.objects.filter(userinfo=user_obj).first()
    # 当前站点所有文章，一对多
    article_list = Article.objects.filter(user=user_obj)
    if not article_list:
        return render(request, 'no_article.html', locals())
    if kwargs:
        conditon = kwargs.get('conditon')
        param = kwargs.get('param')
        if conditon == 'tag':
            article_list = article_list.filter(tags__title=param)
        elif conditon == 'category':

            article_list = article_list.filter(category__title=param)

        else:
            year, month = param.split('/')
            article_list = article_list.filter(create_time__year=year, create_time__month=month)

    current_page, page_range = myPaginator.paginator(request, article_list)

    return render(request, 'home_site.html', locals())


# 注销
def logout(request):
    auth.logout(request)

    return redirect('/index/')


# 注册页面
def register(request):
    # 两种方式都可以
    if request.method == 'POST':
        response = {'user': None, 'msg': None}
        # 先用forms组件校验
        form = RegForm(request.POST)
        if form.is_valid():
            response['user'] = form.cleaned_data.get('username')
            # 生成记录表，创建用户
            # 取出校验过的字段
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            email = form.cleaned_data.get('email')
            blog_name = form.cleaned_data.get('blog_name')
            # 取出文件
            avatar_obj = request.FILES.get('avator')
            extra = {}  # 其他字段字典
            # 判断用户是不是上传了文件
            if avatar_obj:
                extra['avatar'] = avatar_obj

            with transaction.atomic():
                blog_obj = Blog.objects.create(title=blog_name, site_name=username)
                UserInfo.objects.create_user(username=username, password=password, email=email, blog=blog_obj, **extra)
        else:
            response['msg'] = form.errors

        return JsonResponse(response)

    form = RegForm()
    return render(request, 'register.html', locals())


# 主页index
def index(request, **kwargs):
    # 文章列表
    article_list = Article.objects.all()
    # 站点文章分类
    web_site_category_list = Web_Site_Category.objects.all()
    # 最热博客，1、获取博客所有文章的点赞数，2，按用户id分组，3、获取用户点赞数，排序，取前10
    # article_hot_list = Article.objects.order_by('user_id').aggregate(c=Sum('up_count'))
    # Django实际流程是如下简单
    article_hot_list = Article.objects.values('user__blog__title').annotate(c=Sum('up_count')).order_by('c').values(
        'user__username', 'user__blog__title', 'c').reverse()[
                       0:21]
    if kwargs:
        cate = kwargs['cate']
        article_list = Article.objects.filter(web_site_category=cate)

    current_page, page_range = myPaginator.paginator(request, article_list)
    return render(request, 'index.html', locals())


# 登陆
def login(requset):
    if requset.method == 'POST':
        response = {'user': None, 'msg': None}

        user = requset.POST.get('user')
        pwd = requset.POST.get('pwd')
        valid_code = requset.POST.get('valid_code')
        # 将存储在session中的验证码取出来
        valid_code_str = requset.session.get('valid_code_str')

        if valid_code.upper() == valid_code_str.upper():
            user = auth.authenticate(username=user, password=pwd)

            if user:
                # 注册session
                auth.login(requset, user)
                response['user'] = requset.user.username
            else:
                response['msg'] = {'username': ' 账号或者密码错误', 'password': '账号或者密码错误'}
        else:
            response['msg'] = {'valid': '验证码错误'}
        # 直接使用JsonResponse，不用json转换,前端也不用
        return JsonResponse(response)
    return render(requset, 'login.html')


# 获取验证码
def get_valid_img(request):
    data = valid_code.get_valid_code(request)

    return HttpResponse(data)
