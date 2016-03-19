#!/usr/bin/env python3
# -*- coding: utf-8 -*- 

__author__ = 'Lian Tian'
__email__ = "liantian@188.com"
__status__ = "Dev"

import os
import sys

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../..//'))
sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../'))

import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()

from django.db.models import F
from django.db import transaction
import feedparser
import json
from dateutil import parser, tz
import datetime
import pytz

from entry.models import *

# for k in d:
#     print(k)
# print(d)



if __name__ == "__main__":
    obj = EntryCollect.objects.all().update(need_collect_word=True)
    # obj = EntryCollect.objects.all()
    # obj.delete()
    # obj = FetchLog.objects.all()
    # obj.delete()
    # obj = HamWord.objects.all()
    # obj.delete()
    # obj = SpamWord.objects.all()
    # obj.delete()