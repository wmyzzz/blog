

from django.db import models


# Create your models here.
from django.utils import timezone


class UserInfo(models.Model):
    """用户信息"""
    username = models.CharField(verbose_name="用户名", max_length=32)
    email = models.EmailField(verbose_name="邮箱", max_length=32)
    password = models.CharField(verbose_name="密码", max_length=32)
    mobile_phone = models.CharField(verbose_name="手机号", max_length=32)

    def __str__(self):
        return self.username


class Category(models.Model):
    """文章分类"""
    name = models.CharField(verbose_name='文章类别', max_length=20)

    class Meta:
        verbose_name = '文章类别'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Tag(models.Model):
    """文章标签"""
    name = models.CharField(verbose_name='文章标签', max_length=20)

    class Meta:
        verbose_name = '文章标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Blog(models.Model):
    """博客"""
    title = models.CharField(verbose_name='标题', max_length=100)
    content = models.TextField(verbose_name='正文', default='')
    creator = models.ForeignKey(verbose_name='创建者', to="UserInfo")
    create_time = models.DateTimeField(verbose_name='创建时间', default=timezone.now)
    modify_time = models.DateTimeField(verbose_name='修改时间', auto_now=True)
    click_nums = models.IntegerField(verbose_name='点击量', default=0)
    category = models.ForeignKey(Category, verbose_name='文章类别')
    tag = models.ManyToManyField(Tag, verbose_name='文章标签')

    class Meta:
        verbose_name = '我的博客'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Comment(models.Model):
    creator = models.ForeignKey(verbose_name='创建者', to='UserInfo', related_name='create_comment')
    # name = models.CharField(verbose_name='姓名', max_length=20, default='佚名')
    content = models.CharField(verbose_name='内容', max_length=300)
    create_datetime = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    blog = models.ForeignKey(to='Blog', verbose_name='博客')

    comment = models.ForeignKey(verbose_name='评论', to='self', related_name='reply_comment', null=True, blank=True)

    class Meta:
        verbose_name = '博客评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.content
