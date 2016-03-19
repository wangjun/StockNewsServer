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

from entry.models import *

from concurrent.futures import ThreadPoolExecutor

push_pool = ThreadPoolExecutor(max_workers=4)

import urllib
import http.client
# import blueware.agent


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


templates = """<b>%(title)s</b>
%(summary)s

<a href="%(url)s">原始链接</a>"""


# @blueware.agent.background_task(name='Push Msg', group='StockNews')
def execute_task():
    es = EntryCollect.objects.filter(need_notice=True).all()
    for e in es:
        print(e.title)
        sus = SubscriptionUser.objects.filter(pushover_notice=True).filter(
            key_word__in=e.key_word.all()).all().distinct()
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
    return True


if __name__ == "__main__":

    # if sys.platform == 'win32':
    #     blueware.agent.initialize('e:/StockNewsServer/script/blueware.ini')
    # else:
    #     blueware.agent.initialize('/home/stocknews/web/blueware.ini', "msg")
    #
    # blueware.agent.register_application(timeout=10.0)
    #
    # application = newrelic.agent.application()
    #
    # with newrelic.agent.BackgroundTask(application, name="Push Msg", group='Cron'):
    # if sys.platform == 'win32':
    # pass
    # else:
    #     import blueware.agent
    #     blueware.agent.initialize('/home/stocknews/web/blueware.ini', 'fetch')
    execute_task()