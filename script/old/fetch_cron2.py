#!/usr/bin/env python3
# -*- coding: utf-8 -*- 

__author__ = 'Lian Tian'
__email__ = "liantian@188.com"
__status__ = "Dev"


import os
import sys
import datetime
import time
import re

import feedparser
import pytz
import django

from dateutil import parser




# Django Setting
sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../..//'))
sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../'))
sys.path.append('/home/stocknews/web')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()
from entry.models import Feed, EntryCollect, FetchLog

from concurrent.futures import ThreadPoolExecutor
fetch_pool = ThreadPoolExecutor(max_workers=10)

# Script Setting
COLLECT_DAYS = 1

import concurrent.futures
# fetch_pool = ThreadPoolExecutor(max_workers=5)


def clean_html(html):
    return re.sub('<[^<]+?>', '', html)

def execute_task():
    fs = Feed.objects.all()
    for f in fs:
        # try:
        d = feedparser.parse(f.url)
        for e in d['entries']:
            text = e["title"] + clean_html(e["summary"])
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
                        obj.feed = f
                        obj.raw = "none"
                        obj.active = True
                        obj.need_collect_word = True
                        obj.save()
                except EntryCollect.DoesNotExist:
                    obj = EntryCollect()
                    obj.url_id = e["id"]
                    obj.published = dt
                    obj.title = e["title"]
                    obj.url = e["link"]
                    obj.summary = clean_html(e["summary"])
                    obj.feed = f
                    # obj.raw = json.dumps(e, sort_keys=True, indent=4)
                    obj.raw = "none"
                    obj.save()
                except:
                    print("error")

        log = FetchLog()
        log.feed = f
        log.result = "done"
        log.save()
        print(f.id)
        print("ok")
        # except:
        #     log = FetchLog()
        #     log.feed = f
        #     log.result = "error"
        #     log.save()
        #     print("error")
        time.sleep(5)
    return True


def fetch_one_feed(feed):
    d = feedparser.parse(feed.url)
    for e in d['entries']:
        # text = e["title"] + clean_html(e["summary"])
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
                    obj.feed = feed
                    obj.raw = "none"
                    obj.active = True
                    obj.need_collect_word = True
                    obj.save()
                    print("update %s" % obj.id)
                    # print("update one %s" % feed_id)
            except EntryCollect.DoesNotExist:
                obj = EntryCollect()
                obj.url_id = e["id"]
                obj.published = dt
                obj.title = e["title"]
                obj.url = e["link"]
                obj.summary = clean_html(e["summary"])
                obj.feed = feed
                # obj.raw = json.dumps(e, sort_keys=True, indent=4)
                obj.raw = "none"
                obj.save()
                print("new %s" % obj.id)
                # print("add one %s" % feed_id)
            except:
                pass
        # else:
            # print("older  %s" % feed_id)
    # print("ok%s" % feed_id)
    log = FetchLog()
    log.feed = feed
    log.result = "done"
    log.save()
    return True



if __name__ == "__main__":
    # e = concurrent.futures.ThreadPoolExecutor(5)

    fetch_list = []
    fs = Feed.objects.all()
    for f in fs:
        fetch_list.append(fetch_pool.submit(fetch_one_feed,f))

    for fetch_result in fetch_list:
        try:
            data = fetch_result.result(timeout=30)
        except:
            print("timeout")




    # with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    #     future_to_fetch = {executor.submit(fetch_one_feed, feed): feed for feed in fs}
    #     for future in concurrent.futures.as_completed(future_to_fetch):
    #         feed = future_to_fetch[future]
    #         try:
    #             data = future.result(timeout=30)
    #             print(data)
    #         except Exception as exc:
    #             print("eror")
    #         else:
    #             print("eror")







    # import newrelic.agent
    # if sys.platform == 'win32':
    #     newrelic.agent.initialize('e:/StockNewsServer/script/newrelic.ini')
    # else:
    #     newrelic.agent.initialize('/home/stocknews/web/script/newrelic.ini')
    #
    # newrelic.agent.register_application(timeout=10.0)
    #
    # application = newrelic.agent.application()
    #
    # with newrelic.agent.BackgroundTask(application, name="Fetch Seed", group='Cron'):
    # execute_task()




