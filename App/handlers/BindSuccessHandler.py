# coding=utf-8
import tornado.websocket
import logging
from utils.db_utils import db_util
from utils.utils import f_rsp, verify_request_body
from BaseHandler import BaseHandler


class bindSucceedHandler(BaseHandler):
    def post(self):
        try:
            ExpectParams = ['RFID']
            RqstDt = verify_request_body(self, ExpectParams)
            if not RqstDt:
                rsp = f_rsp("Wrong Params: ", "40000")
                self.write(rsp)
            else:
                rfid = str(RqstDt.get('RFID'))
                DbInit = db_util()
                _sql = "SELECT * FROM wx_openid_rfid WHERE wx_rfid = '" + rfid + "'"
                DbRsIns = DbInit.selectSQL(_sql)
                if DbRsIns:
                    rsp = f_rsp("success", "20000")
                    self.write(rsp)
                else:
                    rsp = f_rsp("error", "41000")
                    self.write(rsp)
        except Exception as e:
            logging.error('获取绑定信息失败' + str(e))
            rsp = f_rsp("error", "50000")
            self.write(rsp)
