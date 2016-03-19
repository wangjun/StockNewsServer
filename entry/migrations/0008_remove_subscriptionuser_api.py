# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entry', '0007_auto_20150523_1806'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscriptionuser',
            name='api',
        ),
    ]
