#!/usr/bin/env python3
# -*- coding: utf-8 -*- 

__author__ = 'Lian Tian'
__email__ = "liantian@188.com"
__status__ = "Dev"



import os
import sys
# import datetime
import time
# import json
# import re
#
# import feedparser
# import pytz
import django
from django.db.models import Q
# from django.db import transaction
# from dateutil import parser
# from concurrent.futures import ThreadPoolExecutor

# Django Setting
sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../..//'))
sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../..//'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()
from entry.models import Feed, EntryCollect, FetchLog
from entry.models import SpamWord, HamWord

# from collections import Counter
import jieba
import jieba.analyse
# import string

MIN_WORD_COUNT = 5
RARE_WORD_PROB = 0.5
EXCLUSIVE_WORD_PROB = 0.99


def text_to_list(text):
    words = jieba.analyse.textrank(text, withWeight=False, topK=15)
    if not len(words):
        raise ValueError('Text did not contain any valid words')
    return words


def get_word_hum(word):
    obj, created = HamWord.objects.get_or_create(word=word)
    if created:
        return 1 - RARE_WORD_PROB
    else:
        return

if __name__ == "__main__":
    es = EntryCollect.objects.all()[:2]
    for e in es:
        text = e.title + "\n" + e.summary
        print(text)
        words = text_to_list(text)
        total_word_count = len(words)
        for word in words:
            word_hum =a