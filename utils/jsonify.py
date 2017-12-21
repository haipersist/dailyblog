#-*-coding:utf-8-*-
"""

the func is gotten from Flask,I can construct json data.

it's created by the time when I started to learn Django.
maybe ,it's my habbit.

In fact,Django also provides json format---JsonResponse


 :copyright: (c) 2016 by Haibo Wang.
"""
import json


def jsonify(**kwargs):
    """
    Example usage::
        def get_current_user():
            return jsonify(username=g.user.username,
                           email=g.user.email,
                           id=g.user.id)

    """
    return json.dumps(dict(**kwargs))


def json2py(json_data):
    return json.loads(json_data)





