# encoding=utf-8
import sys

reload(sys)
sys.setdefaultencoding('utf8')


class wxCofing(object):
    """微信开发--基础配置"""

    AppID = ""
    AppSecret = ""

    # 微信网页开发域名
    AppHost = ""

    # 获取access_tokenc的url
    config_get_access_token_url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s" % (
    AppID, AppSecret)

    # 获取Token的url
    token_url = "https://api.weixin.qq.com/cgi-bin/qrcode/create?access_token="

    # 获取二维码图片Url,
    qrcode_getUrl = "https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket="

    # 自定义菜单创建接口
    menu_create_url = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token="

    # 自定义菜单查询接口
    menu_get_url = "https://api.weixin.qq.com/cgi-bin/menu/get?access_token="

    # 自定义菜单删除接口
    menu_delete_url = "https://api.weixin.qq.com/cgi-bin/menu/delete?access_token="
