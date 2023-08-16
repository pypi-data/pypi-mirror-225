#!/usr/bin/env python3
# coding = utf8
"""
@ Author : ZeroSeeker
@ e-mail : zeroseeker@foxmail.com
@ GitHub : https://github.com/ZeroSeeker
@ Gitee : https://gitee.com/ZeroSeeker
"""
import requests
import json


def get_public_ip():
    """
    获取当前网络公网ip地址
    """
    request_url = "http://httpbin.org/ip"
    response = requests.get(url=request_url)
    origin_ip = json.loads(response.text).get("origin")
    return origin_ip
