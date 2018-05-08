#encoding=utf-8

import json
import sys

import requests

from App.Server.WechatConfig import wxCofing

reload(sys)
sys.setdefaultencoding('utf8')


class WxMenuServer(object):
    """
    微信自定义菜单服务
    """
    def create_menu(self):
        """自定义菜单创建接口"""
        access_token = self._token_cache.get_cache(self._token_cache.KEY_ACESS_TOKEN)
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
                        "name": "梦想护照",
                        "url": "http://www.rfidtour.com"
                    },
                    {
                        "name": "智慧旅游",
                        "sub_button": [
                            {
                                "type": "click",
                                "name": "交互游戏",
                                "key": "V1001_GAME"
                            },
                            {
                                "type": "view",
                                "name": "关于我们",
                                "url": "http://www.invengo.cn/"
                            }
                        ]
                    }
                ]
            }
        menu_data = json.dumps(menu_data, ensure_ascii=False)
        return menu_data

# if __name__ == '__main__':
#     wx_menu_server = WxMenuServer()
#     '''自定义菜单创建接口'''
#     wx_menu_server.create_menu()
