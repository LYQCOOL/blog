from django.db import models
from DjangoUeditor.models import UEditorField
from DjangoUeditor.models import UEditorWidget

from datetime import datetime


# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=32, verbose_name="用户名")
    pwd = models.CharField(max_length=32, verbose_name="密码")
    email=models.EmailField(verbose_name="邮箱",max_length=30,null=True,default=True)
    nick_name=models.CharField(verbose_name="昵称",max_length=32,default='haha')

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class Tags(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    tag = models.CharField(max_length=20, verbose_name="标签")

    class Meta:
        verbose_name = "标签"
        verbose_name_plural = verbose_name


class Blogs(models.Model):
    title = models.CharField(max_length=32, verbose_name="标题")
    content = UEditorField(verbose_name="内容", width=600, height=300, imagePath="blog/ueditor/",
                           filePath="blog/ueditor/", default='')
    author = models.ForeignKey(User, on_delete=True, verbose_name="用户")
    tag = models.ForeignKey(Tags, on_delete=models.CASCADE, verbose_name="标签",null=True,blank=True)
    add_time=models.DateTimeField(default=datetime.now,verbose_name="时间")

    class Meta:
        verbose_name = "博客"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
