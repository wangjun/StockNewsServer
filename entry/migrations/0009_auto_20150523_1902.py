# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entry', '0008_remove_subscriptionuser_api'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriptionuser',
            name='pushover_app_token',
            field=models.CharField(verbose_name='PushOver App  Token', max_length=100, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='subscriptionuser',
            name='pushover_notice',
            field=models.BooleanField(verbose_name='是否使用PushOver通知', default=False),
        ),
        migrations.AddField(
            model_name='subscriptionuser',
            name='pushover_user_token',
            field=models.CharField(verbose_name='PushOver User Token', max_length=100, null=True, blank=True),
        ),
    ]
