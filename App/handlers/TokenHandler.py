# coding:utf-8
import logging

from App.Server.TokenCache import AccessToken
from BaseHandler import BaseHandler
from utils.utils import api_log_start, api_log_end, f_rsp

"""
    api给C#传递参数token
"""
class TokenHandler(BaseHandler):

    def post(self):
        api_log_start("tokenhandler__verification")
        try:
            # 获取access_token
            token = AccessToken.get_access_token()
            if not token:
                rsp = f_rsp("token error", "41000")
                self.write(rsp)
            rsp = f_rsp(token, "20000")
            self.write(rsp)
            api_log_end(rsp, "tokenhandler_sync")
        except Exception as e:
            logging.error('获取access_token失败', str(e))

