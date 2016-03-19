# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entry', '0005_subscriptionuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='entrycollect',
            name='need_notice',
            field=models.BooleanField(verbose_name='需要通知邮件', default=True),
        ),
    ]
