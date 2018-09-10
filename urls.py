# coding:utf8

'''web解析规则'''

from App.handlers import TokenHandler as tk
from App.handlers import WxSignHandler as wx
from App.handlers import BindSuccessHandler as bs
from App.Server import WxMenu as wm


urlpatterns = [

    (r'/api/wx/token', tk.TokenHandler),
    (r'/', wx.WxSignatureHandler),
    (r'/api/wx/bind_success', bs.bindSucceedHandler),
    (r"/api/wx/menu/create", wm.WxCreateMenu),
    (r"/api/wx/menu/delete", wm.WxDeleteMenu),
    # (r'', wm.wx_menu_server)
   ]