
"""
    基本视图：
    ~~~~~~~~~~~~~

    这里保存着基本视图。不要轻易修改。

    最后更新日期：2015-05-16

"""

from django.views.generic.base import View
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate
from django.contrib.auth import login


from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from django.utils.decorators import method_decorator
import time
from django.contrib.auth.models import User
from django.contrib.auth import logout

class BaseView(View):
    __doc__ = """修改了系统自带的View，加入一个setup（）的初始化函数"""
    def setup(self, request):
        self.response_dict = {}
        self.request = request

    def dispatch(self, request, *args, **kwargs):
        self.setup(request)
        return View.dispatch(self, request, *args, **kwargs)

    def in_group(self, group_full_name):
        """判断当前用户时候在组"""
        return self.request.user.groups.filter(name=group_full_name).exists()

    @staticmethod
    def response_json(data):
        from .utils.DjangoJSONEncoder import dumps
        return HttpResponse(dumps(data), content_type="application/json")

    @staticmethod
    def http_response(data, content_type="application/json"):
        return HttpResponse(data, content_type=content_type)

    def response(self, mimetype="text/html", template_file=None):
        return render_to_response(template_file,
            self.response_dict,
            content_type=mimetype,
            context_instance=RequestContext(self.request, processors=[]))

    @staticmethod
    def go(urlname, args):
        """用法 return self.go(urlname="wiki-view-page",args=(page_id,))"""
        return HttpResponseRedirect(reverse(urlname, args=args))

    @staticmethod
    def null_good():
        # 服务器成功处理了请求，但未返回任何内容。
        return HttpResponse(status=204)

    def go_to_referer(self):
        return HttpResponseRedirect(self.request.META['HTTP_REFERER'])


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


def class_view_decorator(function_decorator):
    """
    适用于类的权限判定
    使用方法：
    @class_view_decorator(login_required)
    class MyView(View):
    """

    def simple_decorator(view):
        view.dispatch = method_decorator(function_decorator)(view.dispatch)
        return view

    return simple_decorator


class Login(BaseView):
    def get(self,request):
        from .forms import SingInForm
        self.response_dict['sif'] = SingInForm
        return self.response(template_file="login.html")

    def post(self, request):
        from .forms import SingInForm
        form = SingInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            login(request, user)
            return self.go(urlname="index", args={})
        return self.go(urlname="login", args={})


