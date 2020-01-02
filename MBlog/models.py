from django.db import models


# Create your models here.
class MicroBlogUser(models.Model):
    name = models.CharField(max_length=50, verbose_name='作者')
    personal_head = models.URLField(verbose_name='头像')
    attention_num = models.IntegerField(verbose_name='关注数')
    fans_num = models.IntegerField(verbose_name='粉丝数')
    micro_blog_num = models.IntegerField(verbose_name='微博数')
    profile = models.CharField(max_length=100, verbose_name='简介')
    address = models.CharField(max_length=50, verbose_name='地址')
    label = models.CharField(max_length=50, verbose_name='标签')
    category = models.CharField(max_length=10, verbose_name='分类')

    class Meta:
        ordering = ['-id']


class MicroBlog(models.Model):
    name = models.ForeignKey(to=MicroBlogUser, on_delete=models.CASCADE, verbose_name='作者')
    time = models.DateTimeField(verbose_name='发布时间')
    content = models.TextField('微博内容')
    forward_num = models.IntegerField(verbose_name='转发数')
    comment_num = models.IntegerField(verbose_name='评论数')
    like_num = models.IntegerField(verbose_name='点赞数')
    forward_content = models.TextField('转发微博内容', default='无')
    mid = models.CharField(max_length=20, verbose_name='当前这条微博的id')

    class Meta:
        ordering = ['-time']
