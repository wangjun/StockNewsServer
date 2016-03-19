#!/usr/bin/env python3
# -*- coding: utf-8 -*- 

__author__ = 'Lian Tian'
__email__ = "liantian@188.com"
__status__ = "Dev"

import os
import sys

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../../..//'))

import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()

from django.db import transaction
import feedparser
import json
from dateutil import parser, tz
import datetime
import pytz

from entry.models import Feed, EntryCollect

# for k in d:
#     print(k)
# print(d)


# @transaction.atomic
def test():

    # f = Feed.objects.get(id=1)
    url = "http://finance.qq.com/financenews/domestic/rss_domestic.xml"
    print(url)
    d = feedparser.parse(url)
    print(d['feed']['title'])
    print(d['feed']['link'])
    for e in d['entries']:
        for k in e:
            print(k)
        print(type(e))
        print(e["title"])
        print(e["id"])
        # print(e["published"])
        print(e["published"])
        print(e["link"])
        # print(e["published_parsed"])
        # print(type())
        # dt = parser.parse(e["published"])
        # dy = (datetime.datetime.utcnow() - datetime.timedelta(days=3)).replace(tzinfo=pytz.utc)
        #
        # if dt > dy:
        #     print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")



        # try:
        #     obj = EntryCollect.objects.get(url_id=e["id"])
        #     if obj.published < dt:
        #         # print(obj.published)
        #         # print(dt)
        #         # print(e["link"])
        #         # print(e["title"])
        #         obj.published = dt
        #         obj.url_id = e["id"]
        #         obj.title = e["title"]
        #         obj.url = e["link"]
        #         obj.summary = e["summary"]
        #         obj.feed_id = 1
        #         obj.raw = json.dumps(e, sort_keys=True, indent=4)
        #         obj.active = True
        #         obj.save()
        #     else:
        #         pass
        # except EntryCollect.DoesNotExist:
        #     obj = EntryCollect()
        #     obj.url_id = e["id"]
        #     obj.published = dt
        #     obj.title = e["title"]
        #     obj.url = e["link"]
        #     obj.summary = e["summary"]
        #     obj.feed_id = 1
        #     obj.raw=json.dumps(e, sort_keys=True, indent=4)
        #     print(dt)
        #     print(e["link"])
        #     print(e["title"])
        #     obj.save()


    # print(d.feed.subtitle)
    # print(len(d['entries']))
    # print( d['entries'][0]['title'] )
    # print( d['entries'][0])
    # print( d['entries'][0]['id'])
    # print(d.version)
    # print(d.headers)


        print("=============================")
if __name__ == "__main__":
    test()