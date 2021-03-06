# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2020-07-18 14:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0003_blog_creator'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=300, verbose_name='内容')),
                ('create_datetime', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Blog', verbose_name='博客')),
                ('comment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reply_comment', to='web.Comment', verbose_name='评论')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='create_comment', to='web.UserInfo', verbose_name='创建者')),
            ],
            options={
                'verbose_name': '博客评论',
                'verbose_name_plural': '博客评论',
            },
        ),
    ]
