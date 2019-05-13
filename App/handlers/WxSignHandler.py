# coding:utf-8
import hashlib

from BaseHandler import BaseHandler
import logging
import xml.etree.cElementTree as ET
import time
import re

from utils.db_utils import db_util
from utils.utils import api_log_start


class WxSignatureHandler(BaseHandler):
    """微信服务器签名验证"""

    def get(self):
        api_log_start("WxSignatureHandler_verification")
        try:
            signature = self.get_argument('signature')
            timestamp = self.get_argument('timestamp')
            nonce = self.get_argument('nonce')
            echostr = self.get_argument('echostr')
            logging.debug('[微信sign验证],signature' + signature, '&timestamp=' + timestamp, '&nonce=' + nonce,
                          '&echostr=' + echostr)
            result = self.check_signature(signature, timestamp, nonce)
            if result:
                logging.debug('[微信sign验证]，返回echostr=' + echostr)
                self.write(echostr)
            else:
                logging.error('微信sign校验，--校验失败')
        except Exception as e:
            logging.error('微信sign校验，--Exception' + str(e))

    def post(self):
        body = self.request.body
        logging.debug('微信消息回复中心--收到用户消息' + str(body.decode('utf-8')))
        data = ET.fromstring(body)
        ToUserName = data.find('ToUserName').text
        FromUserName = data.find('FromUserName').text
        MsgType = data.find('MsgType').text
        if MsgType == 'text' or MsgType == 'voice':
            '''文本消息 or 语音消息'''
            try:
                MsgId = data.find("MsgId").text
                if MsgType == 'text':
                    Content = data.find('Content').text  # 文本消息内容
                elif MsgType == 'voice':
                    Content = data.find('Recognition').text  # 语音识别结果，UTF8编码
                if Content == u'你好':
                    reply_content = '您好,请问有什么可以帮助您的吗?'
                else:
                    # 查找不到关键字,默认回复
                    reply_content = "抱歉没有找到，客服小儿智商不够用啦~"
                if reply_content:
                    CreateTime = int(time.time())
                    out = self.reply_text(FromUserName, ToUserName, CreateTime, reply_content)
                    self.write(out)
            except:
                pass

        elif MsgType == 'event':
            '''接收事件推送'''
            try:
                Event = data.find('Event').text
                if Event == 'subscribe' or Event == "SCAN":
                    # subscribe 用户未关注时,进行关注后的事件推送 / SCAN 用户已关注的事件推送
                    create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    rfid = data.find('EventKey').text
                    if not rfid:
                        reply_content = '欢迎来到远望谷智慧旅游，在这里将带给你不一样的旅游体验~'
                        out = self.reply_text(FromUserName, ToUserName, create_time, reply_content)
                        self.write(out)
                    else:
                        if rfid.startswith('qrscene'):
                            rfid = rfid.split("_")[1]
                        DbInit = db_util()
                        _sql = ""
                        DbRsIns = DbInit.executeSQL(_sql, (FromUserName, rfid, create_time, create_time))
                        if DbRsIns:
                            DbInit.commit()
                            reply_content = '恭喜您！感谢使用~'
                            out = self.reply_text(FromUserName, ToUserName, create_time, reply_content)
                            self.write(out)
                        else:
                            logging.error(u'未绑定数据保存失败')

                if Event == "unsubscribe":
                    # 取消关注事件
                    pass

                if Event == "CLICK":
                    # 点击菜单拉取消息时的事件推送
                    pass

                if Event == "VIEW":
                    # 点击菜单跳转链接时的事件推送
                    pass

            except Exception as e:
                logging.error(e)

    def check_signature(self, signature, timestamp, nonce):
        """校验token是否正确"""
        token = 'invengosh'
        L = [timestamp, nonce, token]
        L.sort()
        s = L[0] + L[1] + L[2]
        sha1 = hashlib.sha1(s.encode('utf-8')).hexdigest()
        logging.debug('sha1=' + sha1 + '&signature=' + signature)
        return sha1 == signature

    def reply_text(self, FromUserName, ToUserName, CreateTime, Content):
        """回复文本消息模板"""
        textTpl = """<xml> <ToUserName><![CDATA[%s]]></ToUserName> <FromUserName><![CDATA[%s]]></FromUserName> <CreateTime>%s</CreateTime> <MsgType><![CDATA[%s]]></MsgType> <Content><![CDATA[%s]]></Content></xml>"""
        out = textTpl % (FromUserName, ToUserName, CreateTime, 'text', Content)
        return out
