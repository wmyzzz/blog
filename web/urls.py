# _author: 17393
# date: 2020/7/17

from django.conf.urls import url

from web import views

urlpatterns = [
    url(r'^index/$', views.index, name="index"),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login, name='login'),
    url(r'^image/code/$', views.image_code, name='image_code'),
    url(r'^logout/$', views.logout, name='logout'),

    url(r'^blog/$', views.blog, name='blog'),
    url(r'^blog/list/$', views.blog_list, name='blog_list'),
    url(r'^blog/detail/(?P<blog_id>\d+)/$', views.blog_detail, name='blog_detail'),
    url(r'^blog/delete/(?P<blog_id>\d+)/$', views.blog_delete, name='blog_delete'),
    url(r'^blog/update/(?P<blog_id>\d+)/$', views.blog_update, name='blog_update'),
    url(r'^comment/record/(?P<blog_id>\d+)/$', views.comment_record, name='comment_record'),
]
