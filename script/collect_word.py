#!/usr/bin/env python3
# -*- coding: utf-8 -*- 

__author__ = 'Lian Tian'
__email__ = "liantian@188.com"
__status__ = "Dev"

import os
import sys

import django
import jieba.analyse
# import blueware.agent


# Django Setting
sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../..//'))
sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../'))
sys.path.append('/home/stocknews/web')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()
from entry.models import EntryCollect, KeyWord

# Script Setting
TOP_WORD = 20

jieba.initialize()


# @blueware.agent.background_task(name='Collect Word', group='StockNews')
def execute_task():
    es = EntryCollect.objects.filter(need_collect_word=True).all()[0:25]
    for e in es:
        e.key_word.clear()
        all_text = e.title + e.summary
        # print(all_text)
        for x in jieba.analyse.textrank(all_text, withWeight=False, topK=TOP_WORD):
            # print(x)
            obj, created = KeyWord.objects.get_or_create(title=x)
            e.key_word.add(obj)
        e.need_collect_word = False
        e.save()
    return True


if __name__ == "__main__":

    # if sys.platform == 'win32':
    #     blueware.agent.initialize('e:/StockNewsServer/script/blueware.ini')
    # else:
    #     blueware.agent.initialize('/home/stocknews/web/blueware.ini', 'word')
    #
    # blueware.agent.register_application(timeout=10.0)
    #
    # # application = newrelic.agent.application()
    # #
    # # with newrelic.agent.BackgroundTask(application):
    # # if sys.platform == 'win32':
    # # pass
    # # else:
    # #     import blueware.agent
    # #     blueware.agent.initialize('/home/stocknews/web/blueware.ini', 'fetch')
    execute_task()

