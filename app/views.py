from django.shortcuts import HttpResponse
from django.shortcuts import render,redirect
from django import forms
from django.forms import fields
from django.forms import widgets
from app import models
import datetime
import json
# Create your views here.
class User(forms.Form):
    #登录界面的用户名框，error_messages为fields包的参数，输入为空时的提示，widget为该input标签的属性
    username = fields.CharField(error_messages={'required': '用户名不能为空'},
                                widget=widgets.Input(attrs={'type': "text", 'class': "form-control", 'name': "username",
                                                            'id': "username", 'placeholder': "请输入用户名"}))
   #密码框的定制
    password = fields.CharField(error_messages={'required': '密码不能为空.'},
                                widget=widgets.Input(
                                    attrs={'type': "password", 'class': "form-control", 'name': "password",
                                           'id': "password",
                                           'placeholder': "请输入密码"}))
class Newuser(forms.Form):
    #注册界面用户名框最长长度不能超过9，最小不能小于3，且不能为空
    username=fields.CharField(max_length=9,min_length=3,error_messages={'required':'用户名不能为空','max_length':'用户名长度不能大于9','min_length':'用户名长度不能小于3'},
                              widget=widgets.Input(attrs={'type':"text",'class':"form-control",'name':"username",'id':"username",'placeholder':"请输入用户名"}))
    # 注册界面密码框最长长度不能超过12，最小不能小于6，且不能为空
    password=fields.CharField(max_length=12, min_length=6,
                               error_messages={'required': '密码不能为空.', 'max_length': '密码长度不能大于12',
                                               'min_length': '密码长度不能小于6'},
                              widget=widgets.Input(
                                  attrs={'type': "password", 'class': "form-control", 'name': "password", 'id': "password",
                                         'placeholder': "请输入密码"})
                              )
    # 注册界面再次输入密码框最长长度不能超过9，并与前一个密码框内容比较，两次不一致提示“两次密码不一致”，最小不能小于3，且不能为空
    confirm_password=fields.CharField(max_length=12, min_length=6,
                               error_messages={'required': '不能为空.', 'max_length': '两次密码不一致',
                                               'min_length': '两次密码不一致'},
                                      widget=widgets.Input(
                                          attrs={'type': "password", 'class': "form-control", 'name': "confirm_password",
                                                 'id': "confirm_password",
                                                 'placeholder': "请重新输入密码"})
                                      )
def login(request):
    """
        登陆
        :param request:
        :return:
        """
    #定义空字符串，以便向前端页面提示错误
    s = ''
    #Get请求，返回login.html界面，输入框规则参照制定的User()并实列化
    if request.method == 'GET':
        obj = User()
        return render(request, 'login.html', {'obj': obj})
    #POST请求，通过实例化User()表单验证输入是否符合要求，并把用户名和密码提交到后端验证，
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
                    return redirect('/diaries/')
                else:
                    s = '''
                      <script>alert('密码错误!!!请重新输入!!!');</script>
                  '''
        #输入的用户名不存在
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
    #如果是GET请求，实例化类Newuser(),即进行注册的表单验证
    if request.method == 'GET':
        obj = Newuser()
        return render(request, 'register.html', {'obj': obj, 'er': er})
    if request.method == 'POST':
           #form表单验证
            obj = Newuser(request.POST)
           #该方法表示输入框的值是否都符合定制的规范，是则返回True，否则False
            r = obj.is_valid()
            if r:
                    #获取用户名框中内容并与数据库比较，若存在该用户，向像前端返回s，提示用户已经存在，不存在则继续验证
                    user = request.POST.get('username')
                    u = models.User.objects.filter(username=user)
                    if u:
                        s = '''
                       <script>alert('用户名已经存在，请从新输入用户名！');
                   </script>
                       '''
                    else:
                        #验证输入框两次密码是否相同，不相同则提示不一致
                        pwd1 = request.POST.get('password')
                        pwd2 = request.POST.get('confirm_password')
                        if pwd1 != pwd2:
                            s = '''
                           <script>alert('两次密码不一致，请核对重新输入！');</script>'''
                        #两次密码相同且用户不存在，注册成功，向前端提示成功
                        else:
                            models.User.objects.create(username=user, pwd=pwd1)
                            s = '''
                           <script>alert('注册成功！');
                           </script>'''
                    return render(request, 'register.html', {'obj': obj, 'er': er, 's': s})
           #输入不符合定制的form表单验证，提示格式不正确
            else:
                s = '''
               <script>alert('信息格式不正确,注册失败！');
                   </script>'''
                return render(request, 'register.html', {'obj': obj, 'er': er, 's': s})
def diary(request):
    '''
    日记主页
    :param request: 
    :return: 
    '''
    #f和u均为session验证，为登录成功放在服务器端的字段，有f这个字段且正确才能访问该界面，即登录成功才能访问
    f=request.session.get('is_login',None)
    u=request.session.get('user',None)
    er=''
    if f:
        #取出用户id
      id=models.User.objects.filter(username=u)[0].id
      if request.method=='GET':
          #若为get请求，则把是用户写的日记从日记表取出，返回给前端处理
          obj=models.Diaries.objects.filter(author_id=id)
          return render(request,'diary.html',{'obj':obj,'er':er,'user':u})
      elif request.method=='POST':
          #前端发送删除的POST请求，在这处理，从日记表删除对应id的日记，并向前端返回处理结果
          d_id=request.POST.get('d_id')
          models.Diaries.objects.filter(id=d_id).delete()
          obj = models.Diaries.objects.filter(author_id=id)
          er='''alert('删除成功！！！！');'''
          return render(request,'diary.html',{'obj':obj,'er':er,'user':u})
    #未登录则返回登录界面，无法访问该界面
    else:
        obj=User()
        return render(request,'login.html',{'obj':obj})
def add(request):
    '''
    添加日记
    :param request: 
    :return: 
    '''
    #f和u均为session验证，为登录成功放在服务器端的字段，有f这个字段且正确才能访问该界面，即登录成功才能访问
    f = request.session.get('is_login', None)
    u = request.session.get('user', None)
    er = ''
    if f:
       if request.method=='GET':
           #跳转到添加日记的页面
         return render(request,'add.html',{'user':u,'er':er})
       elif request.method=='POST':
           #提交写好的日记，找到用户id，书写的日记名和内容，时间为现在时间，并插入到日记表中
             id=models.User.objects.filter(username=u)[0].id
             name=request.POST.get('d_name')
             content=request.POST.get('content')
             time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
             # print(name,content,time)
             if content:
                 #不允许内容为空，允许日记名为空，内容不为空，插入数据库，并提示
                 er='''alert('添加成功！！！！');'''
                 models.Diaries.objects.create(content=content,title=name,author_id=id,time=time)
                 return render(request,'add.html',{'user':u,'er':er})
             else:
                 #内容为空则返回er到前端提示不能为空
                 er='''alert('日记内容不能为空！！！');'''
                 return render(request, 'add.html',{'user':u,'er':er})
    else:
        obj = User()
        return render(request, 'login.html', {'obj': obj})
def show(request):
    #f和u均为session验证，为登录成功放在服务器端的字段，有f这个字段且正确才能访问该界面，即登录成功才能访问
    f = request.session.get('is_login', None)
    u = request.session.get('user', None)
    er = ''
    if f:
        if request.method=='GET':
            #未选择日记，提示选择
                er='''alert('还未选择要查看的日记！！！')'''
                return render(request,'show.html',{'er':er,'user':u})
        elif request.method=='POST':
                #选择日记，查看内容
                id=request.POST.get('d_id')
                obj=models.Diaries.objects.filter(id=id).first()
                return render(request,'show.html',{'obj':obj,'er':er,'user':u})
    else:
        obj=User()
        return render(request,'login.html',{'obj':obj})
def edit(request):
    #f和u均为session验证，为登录成功放在服务器端的字段，有f这个字段且正确才能访问该界面，即登录成功才能访问

    f = request.session.get('is_login', None)
    u = request.session.get('user', None)
    er = ''
    if f:
        # 未选择日记，提示选择
        if request.method == 'GET':
            er = '''alert('请从新选择要修改的日记！！！')'''
            return render(request, 'edit.html', { 'er': er, 'user': u})
        elif request.method == 'POST':
            #跳转到编辑页面，并展现已经写好了的旧内容
            id = request.POST.get('d_id')
            obj = models.Diaries.objects.filter(id=id).first()
            return render(request, 'edit.html', {'obj': obj, 'er': er, 'user': u})

    else:
        obj = User()
        return render(request, 'login.html', {'obj': obj})
def change(request):
    #f为session验证，为登录成功放在服务器端的字段，有f这个字段且正确才能访问该界面，即登录成功才能访问
    f=request.session.get('is_login',None)
    #定义字典，便于处理
    ret={'status':True,'error':None,'data':None}
    #获取日记id，修改后的日记名，内容
    id=request.POST.get('d_id')
    title=request.POST.get('name')
    content=request.POST.get('content')
    if f:
        if content:
            #到日记表中找到相应日记id，并修改内容和日记名
            obj=models.Diaries.objects.filter(id=id)[0]
            obj.content=content
            obj.title=title
            obj.save()
            return HttpResponse(json.dumps(ret))
        else:
            #日记为空，提示不能为空，不能修改
            ret['status']=False
            ret['error']='内容不能为空！！！'
            return HttpResponse(json.dumps(ret))
    else:
        #未登录，跳转到登录界面
        ret['status'] = False
        ret['error'] = '请先登录！！！'
        return HttpResponse(json.dumps(ret))
