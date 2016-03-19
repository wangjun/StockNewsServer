#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Create your views here.

from django.contrib.auth.decorators import login_required

from public.views import BaseView
from public.views import class_view_decorator

from django.contrib.auth import logout

from .models import *

DEFAULT_SIZE = 50


@class_view_decorator(login_required)
class Index(BaseView):
    def get(self, request):
        ecs = EntryCollect.objects.filter(active=True).prefetch_related("feed").prefetch_related("key_word")
        ecs = ecs.all()[0:DEFAULT_SIZE]
        self.response_dict["ecs"] = ecs
        return self.response(template_file="index.html")


@class_view_decorator(login_required)
class Filter(BaseView):
    def get(self, request):
        all_key_word = request.user.subscription.key_word.all()

        ecs = EntryCollect.objects.filter(active=True).filter(key_word__in=all_key_word).prefetch_related("feed")
        ecs = ecs.prefetch_related("key_word").distinct().all()[0:DEFAULT_SIZE]
        self.response_dict["ecs"] = ecs
        self.response_dict["user_words"] = all_key_word
        return self.response(template_file="index.html")


@class_view_decorator(login_required)
class EditKeyWord(BaseView):
    def get(self, request):
        all_key_word = request.user.subscription.key_word.all()
        self.response_dict["user_words"] = all_key_word
        return self.response(template_file="keyword.html")

    def post(self, request):
        errors = []
        if not request.POST.get('InputEmail'):
            errors.append('Enter a Email.')
        if '@' not in request.POST['InputEmail']:
            errors.append('Enter a Email.')
        if len(request.POST.get('InputPassword1', '')) > 8:
            if request.POST.get('InputPassword1', '') != request.POST.get('InputPassword2', ''):
                errors.append('Password not match ')
        if 0 < len(request.POST.get('InputPassword1', '')) < 8:
            errors.append('Password to short ')
        if not errors:
            cur_user = request.user

            sub_user = cur_user.subscription
            #
            sub_user.email = request.POST.get('InputEmail')
            sub_user.email_notice = request.POST.get('email_notice', False)
            #
            print(request.POST)
            sub_user.pushover_user_token = request.POST.get('pushover_user_token', "")
            sub_user.pushover_app_token = request.POST.get('pushover_app_token', "")
            sub_user.pushover_notice = request.POST.get('pushover_notice', False)
            #
            sub_user.key_word.clear()
            for x in request.POST.get('InputKeyword', '').replace(' ', '').replace('\n', '').replace('\t', '').split(
                    ','):
                word, created = KeyWord.objects.get_or_create(title=x)
                sub_user.key_word.add(word)
            sub_user.save()

            if len(request.POST.get('InputPassword1', '')) > 8:
                cur_user.set_password(request.POST.get('InputPassword1', ''))
            cur_user.save()
            return self.go(urlname="index", args={})

        self.response_dict["errors"] = errors
        all_key_word = request.user.subscription.key_word.all()
        self.response_dict["user_words"] = all_key_word
        return self.response(template_file="keyword.html")


# class SetEntry(BaseView):
# """
#     预约
#     """
#     def get(self, request):
#         json_data = dict()
#         e = EntryCollect.objects.get(id=request.GET['entry_id'])
#         mod = request.GET['mod']
#
#         if mod == "up":
#             e.human_score = 1
#             e.save()
#             json_data['status'] = True
#             json_data["text"] = "有效信息确认"
#
#         elif mod == "down":
#             e.human_score = -1
#             e.save()
#             json_data['status'] = True
#             json_data["text"] = "无效信息确认"
#         else:
#             json_data['status'] = False
#             json_data["text"] = "错误"
#
#         return self.response_json(data=json_data)


class RegUser(BaseView):
    def get(self, request):
        logout(request)
        return self.response(template_file="reguser.html")

    def post(self, request):
        errors = []
        if not request.POST.get('InputName'):
            errors.append('Enter a Username.')
        if not request.POST.get('InputEmail'):
            errors.append('Enter a Email.')
        if '@' not in request.POST['InputEmail']:
            errors.append('Enter a Email.')
        if len(request.POST.get('InputPassword1', '')) > 8:
            if request.POST.get('InputPassword1', '') != request.POST.get('InputPassword2', ''):
                errors.append('Password not match ')
        if 0 < len(request.POST.get('InputPassword1', '')) < 8:
            errors.append('Password to short ')
        if not errors:
            user = User.objects.create_user(username=request.POST.get('InputName'),
                                            email=request.POST.get('InputEmail'),
                                            password=request.POST.get('InputPassword1'))
            user.save()

            su = SubscriptionUser()
            su.user = user
            su.save()

            return self.go(urlname="index", args={})
        self.response_dict["errors"] = errors
        return self.response(template_file="reguser.html")