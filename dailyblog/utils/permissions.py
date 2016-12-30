#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
permissions.py

 provide one decorator for View Function

 :copyright: (c) 2016 by Haibo Wang.

"""

from django.core.exceptions import PermissionDenied
from functools import wraps
from django.http import HttpResponse,HttpResponseRedirect,HttpResponseNotFound



def permission_forbidden(http_exception=403,next_url='/account/login/'):
    """
    Usage:
    @permission_forbidden(403)
    def test(request):
        return HttpResposne('hello world')

    when decorated by permission_forbidden,if the user is not staff,
    it will raise one PerissionDenied exception

    :param http_exception:
    :return:the return value of decorated function
    """
    def decorator(func):
        @wraps(func)
        def wrapper(request,**kwargs):
            if http_exception == 403:
                if request.user.is_staff:
                    rv = func(request,**kwargs)
                    return rv
                else:
                    raise PermissionDenied
            elif http_exception == 401:
                if not request.user.is_authenticated():
                    return HttpResponseRedirect(next_url)
            rv = func(request,**kwargs)
            return rv

        return wrapper
    return decorator










