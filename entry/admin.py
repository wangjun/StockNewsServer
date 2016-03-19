from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# Register your models here.
from django.utils.translation import ugettext_lazy as _
from .models import *


class EntryCollectAdmin(admin.ModelAdmin):
    list_display = ["title", "published", "active"]
    list_filter = ['feed', "key_word"]
    filter_horizontal = ["key_word"]


class FeedAdmin(admin.ModelAdmin):
    list_display = ["title", "url", "isp", "delay"]


class FetchLogAdmin(admin.ModelAdmin):
    list_display = ["time", "feed", "result"]
    list_filter = ['feed']


class KeyWordAdmin(admin.ModelAdmin):
    list_display = ["title"]


class SubscriptionUserInline(admin.StackedInline):
    model = SubscriptionUser
    can_delete = False
    verbose_name_plural = 'SubscriptionUser'
    filter_horizontal = ["key_word"]

class UserAdmin(UserAdmin):
    inlines = (SubscriptionUserInline, )

admin.site.register(EntryCollect, EntryCollectAdmin)
admin.site.register(Feed, FeedAdmin)
admin.site.register(KeyWord, KeyWordAdmin)
# admin.site.register(HamWord, WordAdmin)
# admin.site.register(SpamWord, WordAdmin)
admin.site.register(FetchLog, FetchLogAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)