from django.shortcuts import HttpResponse
from django.shortcuts import render, redirect
from django import forms
from django.forms import fields
from django.forms import widgets
from app import models
import datetime
import json


# Create your views here.
class User(forms.Form):
    # 登录界面的用户名框，error_messages为fields包的参数，输入为空时的提示，widget为该input标签的属性
    username = fields.CharField(error_messages={'required': '用户名不能为空'},
                                widget=widgets.Input(attrs={'type': "text", 'class': "form-control", 'name': "username",
                                                            'id': "username", 'placeholder': "请输入用户名"}))
    # 密码框的定制
    password = fields.CharField(error_messages={'required': '密码不能为空.'},
                                widget=widgets.Input(
                                    attrs={'type': "password", 'class': "form-control", 'name': "password",
                                           'id': "password",
                                           'placeholder': "请输入密码"}))


class Newuser(forms.Form):
    # 注册界面用户名框最长长度不能超过9，最小不能小于3，且不能为空
    username = fields.CharField(max_length=9, min_length=3,
                                error_messages={'required': '用户名不能为空', 'max_length': '用户名长度不能大于9',
                                                'min_length': '用户名长度不能小于3'},
                                widget=widgets.Input(attrs={'type': "text", 'class': "form-control", 'name': "username",
                                                            'id': "username", 'placeholder': "请输入用户名"}))
    # 注册界面密码框最长长度不能超过12，最小不能小于6，且不能为空
    password = fields.CharField(max_length=12, min_length=6,
                                error_messages={'required': '密码不能为空.', 'max_length': '密码长度不能大于12',
                                                'min_length': '密码长度不能小于6'},
                                widget=widgets.Input(
                                    attrs={'type': "password", 'class': "form-control", 'name': "password",
                                           'id': "password",
                                           'placeholder': "请输入密码"})
                                )
    # 注册界面再次输入密码框最长长度不能超过9，并与前一个密码框内容比较，两次不一致提示“两次密码不一致”，最小不能小于3，且不能为空
    confirm_password = fields.CharField(max_length=12, min_length=6,
                                        error_messages={'required': '不能为空.', 'max_length': '两次密码不一致',
                                                        'min_length': '两次密码不一致'},
                                        widget=widgets.Input(
                                            attrs={'type': "password", 'class': "form-control",
                                                   'name': "confirm_password",
                                                   'id': "confirm_password",
                                                   'placeholder': "请重新输入密码"})
                                        )


def login(request):
    """
        登陆
        :param request:
        :return:
        """
    # 定义空字符串，以便向前端页面提示错误
    s = ''
    # Get请求，返回login.html界面，输入框规则参照制定的User()并实列化
    if request.method == 'GET':
        obj = User()
        return render(request, 'login.html', {'obj': obj})
    # POST请求，通过实例化User()表单验证输入是否符合要求，并把用户名和密码提交到后端验证，
    # 与数据库比较是否存在该用户且密码正确，分别给出相应提示
    if request.method == 'POST':
        obj = User(request.POST)
        u = request.POST.get('username')
        t1 = models.User.objects.filter(username=u)
        if t1:
            pwd = request.POST.get('password')
            if pwd == t1[0].pwd:
                request.session['user'] = u
                request.session['is_login'] = True
                return redirect('/blogs/')
            else:
                s = '''
                      <script>alert('密码错误!!!请重新输入!!!');</script>
                  '''
        # 输入的用户名不存在
        else:
            s = '''
               <script>alert('该用户名不存在!!!请检查是否正确!!!');</script>
                                    '''
        return render(request, 'login.html', {'obj': obj, 's': s})


def register(request):
    """
       注册
       :param request:
       :return:
       """
    # 定义空字符串，以便向前端页面提示错误
    er = ''
    # 如果是GET请求，实例化类Newuser(),即进行注册的表单验证
    if request.method == 'GET':
        obj = Newuser()
        return render(request, 'register.html', {'obj': obj, 'er': er})
    if request.method == 'POST':
        # form表单验证
        obj = Newuser(request.POST)
        # 该方法表示输入框的值是否都符合定制的规范，是则返回True，否则False
        r = obj.is_valid()
        if r:
            # 获取用户名框中内容并与数据库比较，若存在该用户，向像前端返回s，提示用户已经存在，不存在则继续验证
            user = request.POST.get('username')
            u = models.User.objects.filter(username=user)
            if u:
                s = '''
                       <script>alert('用户名已经存在，请从新输入用户名！');
                   </script>
                       '''
            else:
                # 验证输入框两次密码是否相同，不相同则提示不一致
                pwd1 = request.POST.get('password')
                pwd2 = request.POST.get('confirm_password')
                if pwd1 != pwd2:
                    s = '''
                           <script>alert('两次密码不一致，请核对重新输入！');</script>'''
                # 两次密码相同且用户不存在，注册成功，向前端提示成功
                else:
                    models.User.objects.create(username=user, pwd=pwd1)
                    s = '''
                           <script>alert('注册成功！');
                           </script>'''
            return render(request, 'register.html', {'obj': obj, 'er': er, 's': s})
            # 输入不符合定制的form表单验证，提示格式不正确
        else:
            s = '''
               <script>alert('信息格式不正确,注册失败！');
                   </script>'''
            return render(request, 'register.html', {'obj': obj, 'er': er, 's': s})


def blog(request):
    '''
    我的主页
    :param request: 
    :return: 
    '''
    # f和u均为session验证，为登录成功放在服务器端的字段，有f这个字段且正确才能访问该界面，即登录成功才能访问
    f = request.session.get('is_login', None)
    u = request.session.get('user', None)
    er = ''
    if f:
        # 取出用户id
        id = models.User.objects.filter(username=u)[0].id
        if request.method == 'GET':
            obj = models.Blogs.objects.filter(author_id=id)
            return render(request, 'blog.html', {'obj': obj, 'er': er, 'user': u})
        elif request.method == 'POST':
            d_id = request.POST.get('d_id')
            models.Blogs.objects.filter(id=d_id).delete()
            obj = models.Blogs.objects.filter(author_id=id)
            er = '''alert('删除成功！！！！');'''
            return HttpResponse(json.dumps({'status': True, 'msg': "haha"}))
            # return render(request, 'blog.html', {'obj': obj, 'er': er, 'user': u})
    # 未登录则返回登录界面，无法访问该界面
    else:
        obj = User()
        return render(request, 'login.html', {'obj': obj})


def add(request):
    '''
    添加博客
    :param request: 
    :return: 
    '''
    # f和u均为session验证，为登录成功放在服务器端的字段，有f这个字段且正确才能访问该界面，即登录成功才能访问
    f = request.session.get('is_login', None)
    u = request.session.get('user', None)
    er = ''
    if f:
        tags = models.Tags.objects.filter(user__username=u)
        if request.method == 'GET':
            return render(request, 'add.html', {'user': u, 'er': er, 'tags': tags})
        elif request.method == 'POST':
            id = models.User.objects.filter(username=u)[0].id
            name = request.POST.get('d_name', '')
            content = request.POST.get('content', '')
            tag = request.POST.get('tag', '')
            if content:
                # 不允许内容为空，允许日记名为空，内容不为空，插入数据库，并提示
                er = '''alert('添加成功！！！！');'''
                tags = models.Tags.objects.filter(user__username=u)
                models.Blogs.objects.create(content=content, title=name, author_id=id, tag_id=tag)
                return render(request, 'add.html', {'user': u, 'er': er, 'tags': tags})
            else:
                # 内容为空则返回er到前端提示不能为空
                er = '''alert('博客内容不能为空！！！');'''
                return render(request, 'add.html', {'user': u, 'er': er, 'tags': tags})
    else:
        obj = User()
        return render(request, 'login.html', {'obj': obj})


def show(request):
    # f和u均为session验证，为登录成功放在服务器端的字段，有f这个字段且正确才能访问该界面，即登录成功才能访问
    f = request.session.get('is_login', None)
    u = request.session.get('user', None)
    er = ''
    if f:
        if request.method == 'GET':
            er = '''alert('还未选择要查看的博客！！！')'''
            return render(request, 'show.html', {'er': er, 'user': u})
        elif request.method == 'POST':
            id = request.POST.get('d_id')
            obj = models.Blogs.objects.filter(id=id).first()
            return render(request, 'show.html', {'obj': obj, 'er': er, 'user': u})
    else:
        obj = User()
        return render(request, 'login.html', {'obj': obj})


def edit(request):
    # f和u均为session验证，为登录成功放在服务器端的字段，有f这个字段且正确才能访问该界面，即登录成功才能访问

    f = request.session.get('is_login', None)
    u = request.session.get('user', None)
    er = ''
    if f:
        if request.method == 'GET':
            id = request.GET.get('id')
            if id:
                er = ''
                obj = models.Blogs.objects.filter(id=id).first()
                tags = models.Tags.objects.filter(user__username=u)
                if obj:
                    return render(request, 'edit.html', {'er': er, 'user': u, 'obj': obj, 'tags': tags})
                else:
                    return redirect('/blogs/')
            else:
                obj = ''
                return redirect('/blogs/')
        elif request.method == 'POST':
            # 跳转到编辑页面，并展现已经写好了的旧内容
            id = request.POST.get('id')
            title = request.POST.get('title', '')
            content = request.POST.get('content', '')
            tag = request.POST.get('tag', '')
            er = '''alert('修改成功！！！');location.href='/blogs';'''
            obj = models.Blogs.objects.filter(id=id).first()
            obj.title = title
            obj.content = content
            obj.tag_id = tag
            obj.save()
            return render(request, 'edit.html', {'obj': obj, 'er': er, 'user': u})

    else:
        obj = User()
        return render(request, 'login.html', {'obj': obj})


def change(request):
    # f为session验证，为登录成功放在服务器端的字段，有f这个字段且正确才能访问该界面，即登录成功才能访问
    f = request.session.get('is_login', None)
    # 定义字典，便于处理
    ret = {'status': True, 'error': None, 'data': None}
    id = request.POST.get('d_id')
    title = request.POST.get('name')
    content = request.POST.get('content')
    if f:
        if content:
            obj = models.Blogs.objects.filter(id=id)[0]
            obj.content = content
            obj.title = title
            obj.save()
            return HttpResponse(json.dumps(ret))
        else:
            ret['status'] = False
            ret['error'] = '内容不能为空！！！'
            return HttpResponse(json.dumps(ret))
    else:
        ret['status'] = False
        ret['error'] = '请先登录！！！'
        return HttpResponse(json.dumps(ret))


def index(request):
    u = request.session.get('user', None)
    tag = request.GET.get('tag', '')
    id = request.GET.get('id', '')
    if tag in ['Python', 'Linux', 'PHP', 'Scrapy', 'Java']:
        all_titles = models.Blogs.objects.filter(tag__tag=tag)
    else:
        all_titles = models.Blogs.objects.all()
    tuxue_tui = models.Blogs.objects.all()[:16:2]
    ping = models.Blogs.objects.all()[:24:3]
    return render(request, 'index.html', {'all_titles': all_titles, 'tuxue_tui': tuxue_tui,
                                          'ping': ping, 'user': u, 'tag': tag})


def tag(request):
    f = request.session.get('is_login', None)
    u = request.session.get('user', None)
    ret = {'status': True, 'error': None, 'data': None}
    if f:
        if request.method == "GET":
            tags = models.Tags.objects.filter(user__username=u)
            return render(request, 'backend_tag.html', {'user': u, 'tags': tags})
        elif request.method == 'POST':
            d_id = request.POST.get('d_id', '')
            if d_id:
                models.Tags.objects.filter(id=d_id).delete()
                return HttpResponse(json.dumps(ret))
            else:
                ret['status'] = False
                ret['error'] = "未找到"
                return HttpResponse(json.dumps(ret))

    else:
        ret['status'] = False
        ret['error'] = '请先登录！！！'
        return HttpResponse(json.dumps(ret))


def add_tag(request):
    f = request.session.get('is_login', None)
    u = request.session.get('user', None)
    ret = {'status': True, 'error': None, 'data': None}
    if request.method == 'POST':
        tag = request.POST.get('tag', '')
        if tag and not models.Tags.objects.filter(tag=tag):
            user_id = models.User.objects.filter(username=u).first().id
            models.Tags.objects.create(user_id=user_id, tag=tag)
        return HttpResponse(json.dumps(ret))
    else:
        ret['status'] = False
        ret['error'] = '请先登录！！！'
        return HttpResponse(json.dumps(ret))
