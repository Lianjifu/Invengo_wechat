# coding:utf-8

from tornado.web import RequestHandler

import json

class BaseHandler(RequestHandler):
    """"自定义基类"""

    def initialize(self):
        self.add_header("Access-Control-Allow-Origin", "*")
        print "\n"

    def prepare(self):
        """预解析json数据"""
        if self.request.headers.get("Content-Type", "").startswith("application/json"):
            self.json_args = json.loads(self.request.body)
        else:
            self.json_args = {}