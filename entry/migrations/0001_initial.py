# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EntryCollect',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('url_id', models.TextField(unique=True, verbose_name='主键')),
                ('published', models.DateTimeField(verbose_name='发布日期')),
                ('title', models.TextField(verbose_name='标题')),
                ('url', models.TextField(verbose_name='地址')),
                ('summary', models.TextField(verbose_name='简讯')),
                ('active', models.BooleanField(default=True, verbose_name='是否被显示')),
                ('raw', models.TextField(verbose_name='原始内容')),
            ],
            options={
                'ordering': ['-published'],
                'verbose_name': '消息归集',
                'verbose_name_plural': '消息归集',
            },
        ),
        migrations.CreateModel(
            name='Feed',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('title', models.CharField(max_length=255, verbose_name='标题')),
                ('url', models.URLField(verbose_name='地址')),
                ('isp', models.CharField(max_length=127, verbose_name='提供商')),
                ('delay', models.IntegerField(default=900, verbose_name='扫描延时')),
            ],
            options={
                'verbose_name': 'RSS源',
                'verbose_name_plural': 'RSS源',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='FetchLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('time', models.DateTimeField(auto_now_add=True, verbose_name='时间')),
                ('result', models.TextField(verbose_name='结果')),
                ('feed', models.ForeignKey(verbose_name='源', related_name='logs', to='entry.Feed')),
            ],
            options={
                'verbose_name': '抓取日志',
                'verbose_name_plural': '抓取日志',
                'ordering': ['-time'],
            },
        ),
        migrations.CreateModel(
            name='KeyWord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('title', models.CharField(max_length=255, unique=True, verbose_name='主键')),
            ],
            options={
                'verbose_name': '关键词',
                'verbose_name_plural': '关键词',
            },
        ),
        migrations.AddField(
            model_name='entrycollect',
            name='feed',
            field=models.ForeignKey(verbose_name='源', related_name='entrys', to='entry.Feed'),
        ),
        migrations.AddField(
            model_name='entrycollect',
            name='key_word',
            field=models.ManyToManyField(to='entry.KeyWord', blank=True, verbose_name='关键词'),
        ),
        migrations.AlterIndexTogether(
            name='entrycollect',
            index_together=set([('url_id',)]),
        ),
    ]
