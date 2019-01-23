# Generated by Django 2.0.2 on 2018-12-02 09:47

import DjangoUeditor.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Blogs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='标题')),
                ('content', DjangoUeditor.models.UEditorField(default='', verbose_name='内容')),
                ('time', models.DateTimeField(verbose_name='创建时间')),
            ],
            options={
                'verbose_name': '博客',
                'verbose_name_plural': '博客',
            },
        ),
        migrations.RemoveField(
            model_name='diaries',
            name='author',
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': '用户', 'verbose_name_plural': '用户'},
        ),
        migrations.AlterField(
            model_name='user',
            name='pwd',
            field=models.CharField(max_length=32, verbose_name='密码'),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=32, verbose_name='用户名'),
        ),
        migrations.DeleteModel(
            name='Diaries',
        ),
        migrations.AddField(
            model_name='blogs',
            name='author',
            field=models.ForeignKey(on_delete=True, to='app.User', verbose_name='用户'),
        ),
    ]