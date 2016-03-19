#!/usr/bin/env python3
# -*- coding: utf-8 -*- 

__author__ = 'Lian Tian'
__email__ = "liantian@188.com"
__status__ = "Dev"


import os
import sys
import datetime
import time
import json
import re

import feedparser
import pytz
import django
import jieba.analyse

from django.db import transaction
from dateutil import parser
from concurrent.futures import ThreadPoolExecutor

# Django Setting
sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../..//'))
sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../..//'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()
from entry.models import Feed, EntryCollect, FetchLog, KeyWord


# Script Setting
COLLECT_DAYS = 2

seed_pool = ThreadPoolExecutor(max_workers=1024)
fetch_pool = ThreadPoolExecutor(max_workers=1)


def collect_word(entry_id):
        e = EntryCollect.objects.get(id=entry_id)
        e.key_word.clear()
        text = e.title + e.summary
        print(text)
        for x in jieba.analyse.textrank(text, withWeight=False, topK=15):
            print(x)
            obj, created = KeyWord.objects.get_or_create(title=x)
            e.key_word.add(obj)
        e.save()

def clean_html(text):
    return re.sub('<[^<]+?>', '', text)

@transaction.atomic
def fetch_feed(feed_id, feed_url):
    try:
        d = feedparser.parse(feed_url)
        for e in d['entries']:
            dt = parser.parse(e["published"])
            dy = (datetime.datetime.utcnow() - datetime.timedelta(days=COLLECT_DAYS)).replace(tzinfo=pytz.utc)
            if dt > dy:
                try:
                    obj = EntryCollect.objects.get(url_id=e["id"])
                    if obj.published < dt:
                        obj.published = dt
                        obj.url_id = e["id"]
                        obj.title = e["title"]
                        obj.url = e["link"]
                        obj.summary = clean_html(e["summary"])
                        obj.feed_id = feed_id
                        obj.raw = json.dumps(e, sort_keys=True, indent=4)
                        obj.active = True
                        obj.save()
                        collect_word(obj.id)
                    else:
                        pass
                except EntryCollect.DoesNotExist:
                    obj = EntryCollect()
                    obj.url_id = e["id"]
                    obj.published = dt
                    obj.title = e["title"]
                    obj.url = e["link"]
                    obj.summary = clean_html(e["summary"])
                    obj.feed_id = feed_id
                    obj.raw = json.dumps(e, sort_keys=True, indent=4)
                    obj.save()
                    collect_word(obj.id)
                except:
                    pass
        return "ok"
    except:
        return "Unexpected error:" + sys.exc_info()[0]


def feed_task(feed_id):
    f = Feed.objects.get(id=feed_id)
    url = f.url
    delay = f.delay
    # delay = 60
    while True:
        q = fetch_pool.submit(fetch_feed, feed_id, url)
        time.sleep(delay-3)
        try:
            result = q.result(timeout=2)
            print(result)
            log = FetchLog()
            log.feed = f
            log.result = result
            log.save()
        except TimeoutError as err:
            q.cancel()
            result = "OS error: {0}".format(err)
            print(result)
            log = FetchLog()
            log.feed = f
            log.result = result
            log.save()
        except :
            result = "Unexpected error:" + sys.exc_info()[0]
            print(result)
            log = FetchLog()
            log.feed = f
            log.result = result
            log.save()
        time.sleep(1)


def make_all_task():
    fs = Feed.objects.all()
    for f in fs:
        seed_pool.submit(feed_task, f.id)
        time.sleep(15)
    while True:
        time.sleep(60)


def test():
    make_all_task()
    # seed_pool.submit(feed_task, 1)
    # seed_pool.submit(feed_task, 2)

if __name__ == "__main__":
    test()
