# encoding=utf-8
import datetime
import json
import urllib

from App.Server.WechatConfig import wxCofing


class AccessToken(object):
    _access_token = {
        'token': '',
        'updatetime': datetime.datetime.now(),
        'expires_in': ''
    }

    @classmethod
    def get_access_token(cls):
        # 如果access_token不存在，或是有效期已过，调用update_access_token方法，生成access_token
        if not cls._access_token['token'] or (
                    datetime.datetime.now() - cls._access_token['updatetime']).seconds >= 6800:
            return cls._update_access_token()
        else:
            return cls._access_token['token']

    @classmethod
    def _update_access_token(cls):
        # 构造请求的url，把appid和appsecret添加到url
        url = wxCofing.config_get_access_token_url
        # 获取响应数据
        resp = urllib.urlopen(url).read()
        resp_data = json.loads(resp)
        cls._access_token['token'] = resp_data.get('access_token')
        return cls._access_token['token']
