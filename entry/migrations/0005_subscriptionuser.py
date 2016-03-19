# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('entry', '0004_entrycollect_need_collect_word'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubscriptionUser',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('api', models.CharField(blank=True, max_length=100, null=True, verbose_name='API KEY')),
                ('key_word', models.ManyToManyField(blank=True, to='entry.KeyWord', verbose_name='订阅的关键词')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, verbose_name='对应用户', related_name='subscription')),
            ],
            options={
                'verbose_name_plural': '订阅用户',
                'verbose_name': '订阅用户',
            },
        ),
    ]
