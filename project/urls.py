"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth.views import login, logout

from cacheops import cached_view


# from entry.views import Index, SetEntry
from entry.views import *
from public.views import Login

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', Index.as_view(), name='index'),
    url(r'^filter$', Filter.as_view(), name='filter'),
    url(r'^keyword$', EditKeyWord.as_view(), name='keyword'),
    # url(r'^accounts/login/$',  login, {'template_name': 'admin/login.html'}),
    url(r'^accounts/logout/$', logout),
    # url(r'^accounts/', include("registration.backends.default.urls")),
    url(r'^accounts/login/$', Login.as_view(), name='login'),
    url(r'^accounts/reguser/$', RegUser.as_view(), name='reguser'),
    # url(r'^set$', SetEntry.as_view(), name="SetEntry"),
    # url(r'^fetch/', include('fetch.urls')),
]
              # + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
