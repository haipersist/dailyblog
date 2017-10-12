#!/usr/bin/env python
# -*- coding:utf-8 -*-


import requests


def get_cookie(url):
      resp = requests.get(url)
      return resp.cookies.items()