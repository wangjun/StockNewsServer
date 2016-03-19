# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class Feed(models.Model):
    __doc__ = """
    一个源...
    """
    title = models.CharField(max_length=255, verbose_name=_("标题"))
    url = models.URLField(verbose_name=_("地址"))
    isp = models.CharField(max_length=127, verbose_name=_("提供商"))
    delay = models.IntegerField(default=900, verbose_name=_("扫描延时"))

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("RSS源")
        verbose_name_plural = verbose_name
        ordering = ['id']


class KeyWord(models.Model):
    __doc__ = """
    关键词.
    """
    title = models.CharField(max_length=255, verbose_name=_("主键"), unique=True)

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("关键词")
        verbose_name_plural = verbose_name


class EntryCollect(models.Model):
    __doc__ = """
    一条又一条的信息...
    """
    url_id = models.TextField(verbose_name=_("主键"), unique=True)
    published = models.DateTimeField(verbose_name=_("发布日期"))
    title = models.TextField(verbose_name=_("标题"))
    url = models.TextField(verbose_name=_("地址"))
    summary = models.TextField(verbose_name=_("简讯"))
    active = models.BooleanField(default=True, verbose_name=_("是否被显示"))

    feed = models.ForeignKey(Feed, verbose_name=_("源"), related_name="entrys")

    raw = models.TextField(verbose_name=_("原始内容"))

    key_word = models.ManyToManyField(KeyWord, verbose_name=_("关键词"), blank=True)
    # key_word_str = models.TextField(verbose_name=_("关键词串"), blank=True)

    # human_score = models.IntegerField(verbose_name=_("人类评分"), default=0)
    # ai_score = models.FloatField(verbose_name=_("机器评分"), default=0.00)
    # be_learn = models.BooleanField(verbose_name=_("已被机器学习"), default=False)

    need_collect_word = models.BooleanField(verbose_name=_("需要收集关键词"), default=True)

    need_notice = models.BooleanField(verbose_name=_("需要通知邮件"), default=True)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _("消息归集")
        verbose_name_plural = verbose_name
        ordering = ['-published']
        index_together = ["url_id"]


class FetchLog(models.Model):
    __doc__ = """
    抓取日志...
    """

    time = models.DateTimeField(auto_now_add=True, verbose_name=_("时间"))
    feed = models.ForeignKey(Feed, verbose_name=_("源"), related_name="logs")
    result = models.TextField(verbose_name=_("结果"))

    def __unicode__(self):
        return self.time.strftime("%Y-%m-%d %H:%M")

    class Meta:
        verbose_name = _("抓取日志")
        verbose_name_plural = verbose_name
        ordering = ['-time']


# class SpamWord(models.Model):
#     word = models.CharField(max_length=63, verbose_name=_("字段"))
#     count = models.IntegerField(verbose_name=_("计数"), default=0)
#
#     def __unicode__(self):
#         return self.word
#
#     class Meta:
#         verbose_name = _("无价值字段")
#         verbose_name_plural = verbose_name
#         ordering = ['-count']
#
#
# class HamWord(models.Model):
#     word = models.CharField(max_length=63, verbose_name=_("字段"))
#     count = models.IntegerField(verbose_name=_("计数"), default=0)
#
#     def __unicode__(self):
#         return self.word
#
#     class Meta:
#         verbose_name = _("有价值字段")
#         verbose_name_plural = verbose_name
#         ordering = ['-count']

class SubscriptionUser(models.Model):
    user = models.OneToOneField(User, verbose_name=_("对应用户"), related_name="subscription")
    # api = models.CharField(max_length=100, verbose_name=_("API KEY"), null=True, blank=True)
    key_word = models.ManyToManyField(KeyWord, verbose_name=_("订阅的关键词"), blank=True)
    email_notice = models.BooleanField(verbose_name=_("是否邮件通知"), default=False)
    email = models.EmailField(verbose_name=_("邮件地址"), blank=True, null=True)

    pushover_notice = models.BooleanField(verbose_name=_("是否使用PushOver通知"), default=False)
    pushover_user_token = models.CharField(max_length=100, verbose_name=_("PushOver User Token"), null=True, blank=True)
    pushover_app_token = models.CharField(max_length=100, verbose_name=_("PushOver App  Token"), null=True, blank=True)

    def __unicode__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = _("订阅用户")
        verbose_name_plural = verbose_name