# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entry', '0002_auto_20150522_2109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entrycollect',
            name='url',
            field=models.TextField(verbose_name='地址'),
        ),
    ]
