# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entry', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entrycollect',
            name='url',
            field=models.URLField(verbose_name='地址'),
        ),
    ]
