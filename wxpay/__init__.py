# -*-coding:utf-8 -*-
"""
Created on 2016-8-16

@author: Danny<manyunkai@hotmail.com>
DannyWork Project
"""

from __future__ import unicode_literals

import json
import datetime
import requests

from .utils import gen_nonce_str, gen_sign, trans_dict_to_xml, trans_xml_to_dict

WXPAY_UNIFIED_ORDER_URI = 'https://api.mch.weixin.qq.com/pay/unifiedorder'
WXPAY_QUERY_ORDER_URI = 'https://api.mch.weixin.qq.com/pay/orderquery'
WXPAY_CLOSE_ORDER_URI = 'https://api.mch.weixin.qq.com/pay/closeorder'
WXPAY_DOWNLOAD_BILL_URI = 'https://api.mch.weixin.qq.com/pay/downloadbill'


class Payload(object):
    """
    订单内容
    """

    __slots__ = ('device_info', 'body', '__detail', 'attach', 'out_trade_no', 'fee_type',
                 'total_fee', 'spbill_create_ip', 'time_start', 'time_expire',
                 'goods_tag', 'trade_type', 'product_id', 'limit_pay', 'openid')

    def __init__(self):
        self.__detail = []

    def to_dict(self):
        """
        将有效参数转换为字典返回

        :return: Python 字典
        """

        data = {}
        if self.__detail:
            data['detail'] = json.dumps({'goods_detail': self.__detail})

        for k in self.__slots__:
            v = getattr(self, k, None)
            if v:
                if k in ['time_start', 'time_expire'] and isinstance(v, (datetime.date, datetime.datetime)):
                    # 将 datetime 或 date 对象转换为所需字符串
                    v = v.strftime('%Y%m%d%H%M%S')
                data[k] = v
        return data

    def put_detail_item(self, goods_id, goods_name, goods_num, price,
                        wxpay_goods_id=None, goods_category=None, body=None):
        """
        添加商品详细信息

        :param goods_id: 商品的编号
        :param wxpay_goods_id: 微信支付定义的统一商品编号
        :param goods_name: 商品名称
        :param goods_num: 商品数量
        :param price: 商品单价，单位为分
        :param goods_category: 商品类目ID
        :param body: 商品描述信息
        :return: True
        """

        d = {
            'goods_id': goods_id,
            'goods_name': goods_name,
            'goods_num': goods_num,
            'price': price,
        }
        if wxpay_goods_id:
            d['wxpay_goods_id'] = wxpay_goods_id
        if goods_category:
            d['goods_category'] = goods_category
        if body:
            d['body'] = body

        self.__detail.append(d)


class WXPay(object):
    """
    微信支付

    init:
        app_id: 微信公众号应用ID
        app_secret：微信公众号应用密钥
        mch_id：微信支付商户号
        api_key：微信支付API密钥
        notify_url：微信支付异步通知回调地址
    """

    def __init__(self, app_id, app_secret, mch_id, api_key, notify_url):
        self.app_id = app_id
        self.app_secret = app_secret
        self.mch_id = mch_id
        self.api_key = api_key
        self.notify_url = notify_url

        self.payload = Payload()

    def send_order(self, payload):
        """
        向微信发起统一下单

        :param payload: Payload 实例化对象
        :return: 返回结果，字典形式
        """

        # 组装数据
        data = payload.to_dict()
        data.update({
            'appid': self.app_id,
            'mch_id': self.mch_id,
            'nonce_str': gen_nonce_str(),
            'notify_url': self.notify_url
        })
        data['sign'] = gen_sign(data, self.api_key)

        # 发送请求并返回结果
        return self._do_request(WXPAY_UNIFIED_ORDER_URI, data)

    def query(self, out_trade_no, transaction_id=None):
        """
        通过 商户订单号 或 微信订单号 查询订单状态

        :param out_trade_no: 商户订单号
        :param transaction_id: 微信订单号
        :return: 字典形式
        """

        # 组装数据
        data = {
            'appid': self.app_id,
            'mch_id': self.mch_id,
            'nonce_str': gen_nonce_str()
        }
        if transaction_id:
            data['transaction_id'] = transaction_id
        else:
            data['out_trade_no'] = out_trade_no
        data['sign'] = gen_sign(data, self.api_key)

        # 发送请求并返回结果
        return self._do_request(WXPAY_QUERY_ORDER_URI, data)

    def close(self, out_trade_no):
        """
        通过 商户订单号 关闭订单

        :param out_trade_no: 商户订单号
        :return: 字典形式
        """

        # 组装数据
        data = {
            'appid': self.app_id,
            'mch_id': self.mch_id,
            'nonce_str': gen_nonce_str(),
            'out_trade_no': out_trade_no
        }
        data['sign'] = gen_sign(data, self.api_key)

        # 发送请求并返回结果
        return self._do_request(WXPAY_CLOSE_ORDER_URI, data)

    def download_bill(self, bill_date, bill_type='ALL', device_info=None):
        """
        下载对账单

        :param bill_date: 对账单日期，datetime.date 类型
        :param bill_type: 账单类型，可以是 ALL、SUCCESS 和 REFUND，分别对应全部、当日成功支付的订单和当日退款订单
        :return: 字符串
        """

        data = {
            'appid': self.app_id,
            'mch_id': self.mch_id,
            'nonce_str': gen_nonce_str(),
            'bill_date': bill_date.strftime('%Y%m%d'),
            'bill_type': bill_type
        }
        if device_info:
            data['device_info'] = device_info
        data['sign'] = gen_sign(data, self.api_key)

        # 发送请求并返回结果
        return self._do_request(WXPAY_DOWNLOAD_BILL_URI, data, auto_trans=False)

    def _do_request(self, uri, data, auto_trans=True):
        """
        向微信接口发起请求

        :param uri: 接口地址
        :param data: 主体内容，字典
        :return: 字典形式
        """

        # 将数据转换为微信所需的 XML 格式数据
        xml = trans_dict_to_xml(data)

        req = requests.post(uri, data=xml.encode('utf8'))
        res = req.content.decode('utf8')

        if auto_trans:
            # 将 XML 数据转换为字典以便于处理
            return trans_xml_to_dict(res)
        return res
