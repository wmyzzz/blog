from io import BytesIO

from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from utils.image_code import check_code
from utils.pagination import Pagination
from web import models
from web.forms.account import RegisterModelForm, LoginForm
from web.forms.blog import BlogModelForm, BlogListModelForm, CommentReplyModelForm


def index(request):
    """首页"""
    return render(request, "layout/basic.html")


def register(request):
    """注册"""
    if request.method == "GET":
        form = RegisterModelForm()
        return render(request, "register.html", {'form': form})
    form = RegisterModelForm(request.POST)
    if form.is_valid():
        instance = form.save()
        print("存入数据库")
        return JsonResponse({'status': True, 'data': '/login/'})
    return JsonResponse({'status': False, 'error': form.errors})


def login(request):
    """登录"""
    if request.method == "GET":
        form = LoginForm(request)
        return render(request, "login.html", {'form': form})
    form = LoginForm(request, data=request.POST)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        user_object = models.UserInfo.objects.filter(Q(mobile_phone=username) | Q(email=username)).filter(
            password=password).first()

        if user_object:
            request.session['user_id'] = user_object.id
            request.session['user_name'] = user_object.username
            request.session.set_expiry(60 * 60 * 24 * 14)

            return redirect('index')
        form.add_error('username', '用户名或密码错误')

    return render(request, 'login.html', {'form': form})


def image_code(request):
    """生成验证码"""
    image_object, code = check_code()

    request.session['image_code'] = code
    request.session.set_expiry(60)  # 主动修改session的过期时间为60s

    # 将图片存入内存
    stream = BytesIO()
    image_object.save(stream, 'png')
    return HttpResponse(stream.getvalue())


def logout(request):
    request.session.flush()
    return redirect('index')


def blog(request):
    """创建博客"""
    if not request.session.get('user_id'):
        return redirect('login')
    if request.method == "GET":
        form = BlogModelForm()
        return render(request, 'blog.html', {'form': form})
    form = BlogModelForm(request.POST)
    if form.is_valid():
        print("写入数据库")
        user_id = request.session.get('user_id')
        user = models.UserInfo.objects.filter(id=user_id).first()
        form.instance.creator = user
        form.save()
        return JsonResponse({'status': True, 'data': '/blog/list/'})

    return JsonResponse({'status': False, 'error': form.errors})


def blog_list(request):

    # 查找所有blog
    queryset = models.Blog.objects.all()
    page_object = Pagination(
        current_page=request.GET.get('page'),
        all_count=queryset.count(),
        base_url=request.path_info,
        query_params=request.GET,
        per_page=50
    )
    blog_object_list = queryset[page_object.start:page_object.end]
    form = BlogListModelForm()
    content = {
        'blog_object_list': blog_object_list,
        'page_html': page_object.page_html(),
        'form': form
    }
    return render(request, 'blog_list.html', content)


def blog_detail(request, blog_id):
    """展示博客"""
    blog_object = models.Blog.objects.filter(id=blog_id).first()
    # 点击量+1
    blog_object.click_nums += 1
    blog_object.save()
    return render(request, 'blog_detail.html', {'blog_object': blog_object})


def blog_delete(request, blog_id):
    """删除博客"""
    models.Blog.objects.filter(id=blog_id).delete()

    return redirect('/blog/list/')


def blog_update(request, blog_id):
    """更新博客"""
    blog_object = models.Blog.objects.filter(id=blog_id).first()

    if request.method == "GET":
        form = BlogModelForm(instance=blog_object)
        return render(request, 'blog_update.html', {'form': form, 'blog_object': blog_object})
    form = BlogModelForm(data=request.POST, instance=blog_object)
    if form.is_valid():
        form.save()

        return redirect('blog_list')

    return render(request, 'blog_update.html', {'form': form})


@csrf_exempt
def comment_record(request, blog_id):
    """评论"""
    if request.method == "GET":
        # 查找评论
        comment_list = models.Comment.objects.filter(blog_id=blog_id)
        # 将queryset转换为json格式
        data_list = []
        for row in comment_list:
            data = {
                'id': row.id,
                'content': row.content,
                'creator': row.creator.username,
                'datetime': row.create_datetime.strftime("%Y-%m-%d %H:%M"),
                'parent_id': row.comment_id
            }
            data_list.append(data)

        return JsonResponse({'status': True, 'data': data_list})
    form = CommentReplyModelForm(data=request.POST)
    if form.is_valid():
        form.instance.blog_id = blog_id

        user_id = request.session.get('user_id')
        user = models.UserInfo.objects.filter(id=user_id).first()
        form.instance.creator = user
        instance = form.save()

        info = {
            'id': instance.id,
            'content': instance.content,
            'creator': instance.creator.username,
            'datetime': instance.create_datetime.strftime("%Y-%m-%d %H:%M"),
            'parent_id': instance.comment_id
        }

        return JsonResponse({'status': True, 'data': info})
    return JsonResponse({'status': False, 'error': form.errors})