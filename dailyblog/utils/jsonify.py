#-*-coding:utf-8-*-
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





