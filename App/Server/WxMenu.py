# encoding=utf-8

import json
import sys

import requests

from App.Server.TokenCache import AccessToken
from App.Server.WechatConfig import wxCofing
from App.handlers.BaseHandler import BaseHandler

reload(sys)
sys.setdefaultencoding('utf8')


class WxCreateMenu(BaseHandler):
    def post(self):
        wxmenu = WxMenuServer()
        data = wxmenu.create_menu()
        if data == 0:
            return self.write(dict(code=20000, msg=u"菜单创建成功"))
        else:
            return self.write(dict(code=40001, msg=u"菜单创建失败"))


class WxDeleteMenu(BaseHandler):
    def get(self):
        delete_menu = WxMenuServer()
        data = delete_menu.delete_menu()
        if data == 0:
            return self.write(dict(code=20000, msg=u"菜单删掉成功"))
        else:
            return self.write(dict(code=40001, msg=u"菜单创建失败"))


class WxMenuServer(object):
    """
    微信自定义菜单服务
    """

    def create_menu(self):
        """自定义菜单创建接口"""
        access_token = AccessToken.get_access_token()
        if access_token:
            url = wxCofing.menu_create_url + access_token
            data = self.create_menu_data()
            r = requests.post(url, data.encode("utf-8"))
            if r.status_code == 200:
                res = r.text
                json_res = json.loads(res)
                if 'errcode' in json_res.keys():
                    errcode = json_res['errcode']
                    return errcode
        else:
            return u'获取不得access_token'

    def create_menu_data(self):
        """创建菜单数据"""
        menu_data = {
            "button": [
                {
                    "type": "view",
                    "name": "关于我们",
                    "url": "http://www.invengo.cn/"
                },
                {
                    "name": "智慧旅游",
                    "sub_button": [
                        {
                            "type": "view",
                            "name": "护照兑换系统",
                            "url": "http://www.rfidtour.com"
                        },
                        {
                            "type": "view",
                            "name": "景区签到系统",
                            "url": "http://www.wx2.rfidtour.com/"
                        }
                    ]
                }
            ]
        }
        menu_data = json.dumps(menu_data, ensure_ascii=False)
        return menu_data

    def delete_menu(self):
        access_token = AccessToken.get_access_token()
        if access_token:
            url = wxCofing.menu_delete_url + access_token
            req = requests.get(url)
            if req.status_code == 200:
                res = req.text
                json_res = json.loads(res)
                if 'errcode' in json_res.keys():
                    errcode = json_res['errcode']
                    return errcode
        else:
            return u'删除菜单失败'
