from django.db import models
from django.core import serializers
import json
from datetime import datetime

def djmodel2dict(obj):
    """
    the func is used to convert django model into one dict format
    however,it only take two level into consideration.
    For example:
     Model:
       title = models.CharField()
       author = models.ForeignKey(User,....)

    :param obj:
    :return:
    """
    if not isinstance(obj,models.Model):
        return
    result = {}
    for field in obj._meta.fields:
        value = getattr(obj,field.name)
        if isinstance(value,models.Model):
            value = serializers.serialize('python',[value])[0]
        if isinstance(value,datetime):
            value = value.strftime("%Y-%m-%d %H:%M:%S")
        try:
            json.dumps(value)
        except:
            value = str(value)
        result.setdefault(field.name,value)
    return result
    #return json.dumps(result)






