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

import jieba.posseg as pseg

# en_punctuation = set(string.punctuation)
# ch_en_punctuation = set(['\r\n', '：', '。', ' ', '，', '\n'])
# # black_list =
# black_list = en_punctuation | ch_en_punctuation


def learn_now():
    es = EntryCollect.objects.filter(be_learn=False).filter(~Q(human_score=0)).all()
    for e in es:
        text = e.title + "\n" + e.summary
        print(text)
        print(
            "#########################################################################################################")

        # seg_list = jieba.cut(text, cut_all=True)
        # print("Full Mode: " + "/ ".join(seg_list))  # 全模式

        # seg_list = tags = jieba.analyse.extract_tags(text, topK=20)
        # print("Default Mode: " + "/".join(seg_list))  # 精确模式
        # print(seg_list)
        # z = Counter(seg_list)
        # print(z)
        # print('='*40)
        # print('1. 分词')
        # print('-'*40)
        # seg_list = jieba.cut(text, cut_all=False)
        # print("Default Mode: " + "/ ".join(seg_list))  # 默认模式

        # print('='*40)
        # print('3. 关键词提取')
        # print('-'*40)
        # print(' TF-IDF')
        # print('-'*40)
        #
        # for x, w in jieba.analyse.extract_tags(text, withWeight=True):
        # print('%s %s' % (x, w))
        # words = pseg.cut(text)
        # for w in words:
        #     print('%s %s' % (w.word, w.flag))
        #
        # print('-' * 40)
        # print(' TextRank')
        # print('-' * 40)

        for x in jieba.analyse.textrank(text, withWeight=False, topK=10):
            print('%s' % x)
            if e.human_score > 0:
                obj, created = HamWord.objects.get_or_create(word=x)
                obj.count = obj.count + 1
                obj.save()
            elif e.human_score < 0:
                obj, created = SpamWord.objects.get_or_create(word=x)
                obj.count = obj.count + 1
                obj.save()
        e.be_learn = True
        e.save()
        print(
            "#########################################################################################################")
        print(
            "#########################################################################################################")
        # exclude = set(string.punctuation)
        # print(black_list)
        # pass

if __name__ == "__main__":
    while True:
        learn_now()
        time.sleep(3600)