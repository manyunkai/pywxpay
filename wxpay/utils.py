# -*-coding:utf-8 -*-
"""
Created on 2016-8-16

@author: Danny<manyunkai@hotmail.com>
DannyWork Project
"""

from __future__ import unicode_literals

import uuid
from hashlib import md5
from bs4 import BeautifulSoup


def gen_sign(params, key):
    """
    签名生成函数

    :param params: 参数，dict 对象
    :param key: API 密钥
    :return: sign string
    """

    param_list = []
    for k in sorted(params.keys()):
        v = params.get(k)
        if not v:
            # 参数的值为空不参与签名
            continue
        param_list.append('{0}={1}'.format(k, v))
    # 在最后拼接 key
    param_list.append('key={}'.format(key))
    # 用 & 连接各 k-v 对，然后对字符串进行 MD5 运算
    return md5('&'.join(param_list).encode('utf8')).hexdigest()


def gen_nonce_str():
    """
    生成随机字符串，有效字符a-zA-Z0-9

    :return: 随机字符串
    """

    return ''.join(str(uuid.uuid4()).split('-'))


def trans_xml_to_dict(xml):
    """
    将微信支付交互返回的 XML 格式数据转化为 Python Dict 对象

    :param xml: 原始 XML 格式数据
    :return: dict 对象
    """

    soup = BeautifulSoup(xml, features='xml')
    xml = soup.find('xml')
    if not xml:
        return {}

    # 将 XML 数据转化为 Dict
    data = dict([(item.name, item.text) for item in xml.find_all()])
    return data


def trans_dict_to_xml(data):
    """
    将 dict 对象转换成微信支付交互所需的 XML 格式数据

    :param data: dict 对象
    :return: xml 格式数据
    """

    xml = []
    for k in sorted(data.keys()):
        v = data.get(k)
        if k == 'detail' and not v.startswith('<![CDATA['):
            v = '<![CDATA[{}]]>'.format(v)
        xml.append('<{key}>{value}</{key}>'.format(key=k, value=v))
    return '<xml>{}</xml>'.format(''.join(xml))
