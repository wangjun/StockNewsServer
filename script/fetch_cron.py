#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Lian Tian'
__email__ = "liantian@188.com"
__status__ = "Dev"

import os
import sys
import datetime
import re

import feedparser
import pytz
import django
from dateutil import parser



# Django Setting
sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../..//'))
sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../..//'))
sys.path.append('/home/stocknews/web')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()
from entry.models import Feed, EntryCollect, FetchLog

# from concurrent.futures import ThreadPoolExecutor
# fetch_pool = ThreadPoolExecutor(max_workers=1)

# Script Setting
COLLECT_DAYS = 0
COLLECT_HOURS = 1

# import blueware.agent


def clean_html(html):
    return re.sub('<[^<]+?>', '', html)


# @blueware.agent.background_task(name='Fetch Feed', group='StockNews')
def execute_task():
    fs = Feed.objects.all()
    for f in fs:
        # try:
        d = feedparser.parse(f.url)
        for e in d['entries']:
            text = e["title"] + clean_html(e["summary"])
            dt = parser.parse(e["published"])
            dy = (datetime.datetime.utcnow() - datetime.timedelta(days=COLLECT_DAYS, seconds=COLLECT_HOURS*3600)).replace(tzinfo=pytz.utc)
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
        # log = FetchLog()
        #     log.feed = f
        #     log.result = "error"
        #     log.save()
        #     print("error")
        # time.sleep(1)
    return True


if __name__ == "__main__":

    # if sys.platform == 'win32':
    #     blueware.agent.initialize('e:/StockNewsServer/script/blueware.ini')
    # else:
    #     blueware.agent.initialize('/home/stocknews/web/blueware.ini', 'fetch')
    #
    # blueware.agent.register_application(timeout=10.0)
    # application = newrelic.agent.application()
    #
    # with newrelic.agent.BackgroundTask(application):
    # if sys.platform == 'win32':
    # pass
    # else:
    #     import blueware.agent
    #     blueware.agent.initialize('/home/stocknews/web/blueware.ini', 'fetch')
    execute_task()




