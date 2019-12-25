# Generated by Django 2.2.5 on 2019-12-17 01:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MicroBlogUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='作者')),
                ('personal_head', models.URLField(verbose_name='头像')),
                ('attention_num', models.CharField(max_length=10, verbose_name='关注数')),
                ('fans_num', models.CharField(max_length=12, verbose_name='粉丝数')),
                ('micro_blog_num', models.CharField(max_length=10, verbose_name='微博数')),
                ('profile', models.CharField(max_length=100, verbose_name='简介')),
                ('address', models.CharField(max_length=50, verbose_name='地址')),
                ('label', models.CharField(max_length=50, verbose_name='标签')),

            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='MicroBlog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(verbose_name='发布时间')),
                ('content', models.TextField(verbose_name='微博内容')),
                ('forward_num', models.CharField(max_length=10, verbose_name='转发数')),
                ('comment_num', models.CharField(max_length=10, verbose_name='评论数')),
                ('like_num', models.CharField(max_length=10, verbose_name='点赞数')),
                ('forward_content', models.TextField(default='无', verbose_name='转发微博内容')),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MBlog.MicroBlogUser', verbose_name='作者')),
            ],
            options={
                'ordering': ['-time'],
            },
        ),
    ]