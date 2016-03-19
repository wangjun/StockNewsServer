# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entry', '0006_entrycollect_need_notice'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriptionuser',
            name='email',
            field=models.EmailField(max_length=254, null=True, verbose_name='邮件地址', blank=True),
        ),
        migrations.AddField(
            model_name='subscriptionuser',
            name='email_notice',
            field=models.BooleanField(default=False, verbose_name='是否邮件通知'),
        ),
    ]
