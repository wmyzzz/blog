# _author: 17393
# date: 2020/7/17
from django import forms

from web import models
from web.forms.bootstrap import BootstrapForm


class BlogModelForm(BootstrapForm, forms.ModelForm):

    class Meta:
        model = models.Blog
        fields = ['title', 'content', 'category', 'tag']


class BlogListModelForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = models.Blog
        fields = ['title', 'category', 'tag']


class CommentReplyModelForm(BlogModelForm, forms.Form):
    class Meta:
        model = models.Comment
        fields = ['content', 'comment']