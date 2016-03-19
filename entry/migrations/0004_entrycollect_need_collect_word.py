# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entry', '0003_auto_20150522_2110'),
    ]

    operations = [
        migrations.AddField(
            model_name='entrycollect',
            name='need_collect_word',
            field=models.BooleanField(default=True, verbose_name='需要收集关键词'),
        ),
    ]
