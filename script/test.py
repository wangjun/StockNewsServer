#!/usr/bin/env python3
# -*- coding: utf-8 -*- 

__author__ = 'Lian Tian'
__email__ = "liantian@188.com"
__status__ = "Dev"

import os
import sys
import django


# Django Setting
sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../..//'))
sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../'))
sys.path.append('/home/stocknews/web')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()

# import jieba
# import jieba.analyse
#
# s = """财信网(记者 赵琦薇)今年以来，
# 沪指涨幅只有43.99%，
# 却已有100多只主动偏股型基金取得了翻番以上的涨幅，
# 一些抱团个股的基金净值大幅上涨的现象更是让人叹为观止。 　
# 　数据显示，截至5月22日，有两只基金的净值增长率超200%，分别是易方达新兴成长和汇添富移动互联，涨幅...."""
# # for x, w in jieba.analyse.extract_tags(s, withWeight=True):
# #     print('%s %s' % (x, w))
#
# print('-'*40)
# print(' TextRank')
# print('-'*40)
#
# for x, w in jieba.analyse.textrank(s, topK=20, withWeight=True):
#     print('%s %s' % (x, w))
#
# print('-'*40)
# print(' TextRank')
# print('-'*40)
#
# words = jieba.posseg.cut(s)
# for w in words:
#     print('%s %s' % (w.word, w.flag))
#
# print('-'*40)
# print(' TextRank')
# print('-'*40)
#
# for x, w in jieba.analyse.textrank(s, withWeight=True, topK=20, allowPOS=('ns', 'n', 'vn', 'v', 'nr')):
#     print('%s %s' % (x, w))






# import http.client, urllib
#
# conn = http.client.HTTPSConnection("api.pushover.net:443")
# conn.request("POST", "/1/messages.json",
#   urllib.parse.urlencode({
#     "token": "atHi9r6xV93dPbuYdgyLSekvyquJBp",
#     "user": "uirrBnWoS3wGv9oDQMFA6D4WGHYG3E",
#     "message": "hello world",
#   }), { "Content-type": "application/x-www-form-urlencoded" })
# conn.getresponse()

from pushover import Pushover
#
# po = Pushover("atHi9r6xV93dPbuYdgyLSekvyquJBp")
# po.user("uirrBnWoS3wGv9oDQMFA6D4WGHYG3E")
#
# msg = po.msg("Hello, World!")
#
# msg.set("title", "Best title ever!!!")
#
# q = po.send(msg)

# print(type(q))

from entry.models import *

from concurrent.futures import ThreadPoolExecutor
push_pool = ThreadPoolExecutor(max_workers=4)


import urllib
import http.client


def push_msg(msg_dict):
    conn = http.client.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
      urllib.parse.urlencode({
        "token": msg_dict["pushover_app_token"],
        "user": msg_dict["pushover_user_token"],
        # "message": msg_dict["message"],
        "message": msg_dict["summary"],
        "url": msg_dict["url"],
        "url_title": msg_dict["title"],
        "title": msg_dict["title"],
        "html ": 1,
      }), {"Content-type": "application/x-www-form-urlencoded"})
    return conn.getresponse()


    # po = Pushover()
    # po.user()
    # msg = po.msg()
    # msg.set("title", )
    # return po.send(msg)
    # # return True


templates = """<b>%(title)s</b>
%(summary)s

<a href="%(url)s">原始链接</a>"""

if __name__ == "__main__":
    es = EntryCollect.objects.filter(need_notice=True).all()
    for e in es:
        print(e.title)
        sus = SubscriptionUser.objects.filter(pushover_notice=True).filter(key_word__in=e.key_word.all()).all().distinct()
        for su in sus:
            msg = dict()
            msg["pushover_app_token"] = su.pushover_app_token
            msg["pushover_user_token"] = su.pushover_user_token
            msg["title"] = e.title
            msg["url"] = e.url
            msg["summary"] = e.summary
            msg["message"] = templates % {'title': e.title, "summary": e.summary, "url": e.url}
            # print(push_msg(msg))
            push_pool.submit(push_msg, msg)
        e.need_notice = False
        e.save()