# -*- coding: utf-8 -*-
"""
permissions.py

 provide one decorator for View Function
 It can provide several different permissions.such as 401,403 etc.

 In Additions,you can set permission for different Model. such as

 ArticlePerimission,UserPermisson.

 of course ,They(permisson class) are mainly used in djangorestframwork



 :copyright: (c) 2016 by Haibo Wang.

"""

from django.core.exceptions import PermissionDenied
from functools import wraps
from django.http import HttpResponse,HttpResponseRedirect,HttpResponseNotFound
from rest_framework.permissions import BasePermission,SAFE_METHODS


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



class UserPermisson(BasePermission):
    """
    define one permission,which can limit the user operation
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            #only the authorised user can get data
            return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        only the creater can delete,put or post
        :param request:
        :param view:
        :param obj:
        :return:
        """

        return obj == request.user or request.user.is_staff




class ArticlePermisson(BasePermission):

    def has_object_permission(self, request, view, obj):
        """
        only the creater can delete,put or post
        :param request:
        :param view:
        :param obj:
        :return:
        """
        if request.method in SAFE_METHODS:
            #only the authorised user can get data
            return request.user.is_authenticated

        return request.user == obj.author or request.user.is_staff







