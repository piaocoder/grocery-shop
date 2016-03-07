#coding:utf8
import datetime

from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse, Http404


def helloFamily(request, name):
    """helloFamily:对应http://../hello的业务逻辑代码

    :param request:
    """
    if name == "zheng":
        int("error")
    elif name == "404":
        raise Http404()

    rsp = '''Welcome to the page at {0}.<br>
    Hello world, your name is {1}.'''.format(
        request.path, name)
    return HttpResponse(rsp)


def currentDatetime(request):
    """currentDatetime:显示当前时间

    :param request:
    """
    now = datetime.datetime.now()
    templateTime = get_template("times.html")
    # Context渲染
    html = templateTime.render(
        Context({'current_date':now}))
    # html = "<html><body>Now time {0}."\
        # "</body></html>".format(now)
    return HttpResponse(html)
