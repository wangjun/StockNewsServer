#!/usr/bin/env python3
# -*- coding: utf-8 -*- 

__author__ = 'Lian Tian'
__email__ = "liantian@188.com"
__status__ = "Dev"


import json
import requests

payload =  {'text':"卫星新闻莫斯科6月13日电 俄罗斯总统新闻秘书佩斯科夫表示，普京与土耳其总统埃尔多安重申，双333边贸易额突破1000亿美元是两国的战略目标。 　　佩斯科夫说：“双方几乎就所有双边关系问题交换了意见，包括经贸合作等具体问2题", 'mode':'DF'}

r = requests.post("http://w.liantian.me/analyse", data=payload)

q = json.loads(r.text)

print(q)