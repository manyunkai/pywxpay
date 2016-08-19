# pywxpay
WeChat Pay development based on Python.

### 说明
---
初期开发，支持统一下单、查询订单、关闭订单及下单对账单。

### 依赖的第三方库
---
* BeautifulSoup4：用于 XML 解析
* requests：用于发送请求

### 示例
---
```
>>> from wxpay import *

>>> import random
>>> p = Payload()
>>> p.out_trade_no = random.randrange(1000000000, 9999999999)
>>> p.openid = 'o54WPt8_gLU71cKgj_8Sq8wTsCyI'
>>> p.device_info = 'WEB'
>>> p.body = 'WXPay Test'
>>> p.total_fee = 1
>>> import datetime
>>> p.time_start = datetime.datetime.now()
>>> p.time_expire = datetime.datetime.now() + datetime.timedelta(seconds=600)
>>> p.spbill_create_ip = '180.175.214.202'
>>> p.trade_type = 'JSAPI'

>>> p.put_detail_item(goods_id='1000201', goods_name='Apple', goods_num=1, price=1, wxpay_goods_id='1000201', body='')
>>> p.to_dict()
{u'body': 'WXPay Test', u'openid': 'o54WPt8_gLU71cKgj_8Sq8wTsCyI', u'trade_type': 'JSAPI', u'time_start': '20160819110722', u'detail': '{"goods_detail": [{"wxpay_goods_id": "1000201", "price": 1, "goods_num": 1, "goods_name": "Apple", "goods_id": "1000201"}]}', u'device_info': 'WEB', u'out_trade_no': 2357175218L, u'total_fee': 1, u'time_expire': '20160819111743', u'spbill_create_ip': '180.175.214.202'}

>>> pay = WXPay('you app_id', 'your app_secret', 'your mch_id', 'your api_key', 'https://weixin.iengine.cc/pay/unifiedorder')

>>> pay.send_order(p)
{'trade_type': u'JSAPI', 'prepay_id': u'wx2016081911103872b3f6efe30805011525', 'nonce_str': u'DXq6j4of1yGFTju6', 'device_info': u'WEB', 'return_msg': u'OK', 'return_code': u'SUCCESS', 'mch_id': u'1348794101', 'appid': u'wx42555c938abd6289', 'sign': u'8D87DF825518C797710708000C2C87A3', 'result_code': u'SUCCESS'}

>>> pay.query(out_trade_no='2357175218')
{'trade_state': u'NOTPAY', 'nonce_str': u'zKfpcjaslJVO7DD7', 'return_code': u'SUCCESS', 'return_msg': u'OK', 'sign': u'12EFA6DAACDB29D65DB3112ED5E7B2E1', 'mch_id': u'1348794101', 'out_trade_no': u'2357175218', 'trade_state_desc': u'\u8ba2\u5355\u672a\u652f\u4ed8', 'appid': u'wx42555c938abd6289', 'result_code': u'SUCCESS'}

>>> pay.close(out_trade_no='2357175218')
{'sub_mch_id': u' ', 'nonce_str': u'DJIMR5RAAOAb4MZT', 'return_code': u'SUCCESS', 'return_msg': u'OK', 'sign': u'33D112314AB927479994398FC17C63E0', 'mch_id': u'1348794101', 'appid': u'wx42555c938abd6289', 'result_code': u'SUCCESS'}
>>> pay.query('2357175218')
{'trade_state': u'CLOSED', 'nonce_str': u'vtmfZ5M8IaEckkTU', 'return_code': u'SUCCESS', 'return_msg': u'OK', 'sign': u'9D5699673288BAA1E0D520EEDDA55BE2', 'mch_id': u'1348794101', 'out_trade_no': u'2357175218', 'trade_state_desc': u'\u8ba2\u5355\u5df2\u5173\u95ed', 'appid': u'wx42555c938abd6289', 'result_code': u'SUCCESS'}

>>> pay.download_bill(bill_date=datetime.date(2016, 8, 17), bill_type='ALL')
u'\u4ea4\u6613\u65f6\u95f4,\u516c\u4f17\u8d26\u53f7ID,\u5546\u6237\u53f7,\u5b50\u5546\u6237\u53f7,\u8bbe\u5907\u53f7,\u5fae\u4fe1\u8ba2\u5355\u53f7,\u5546\u6237\u8ba2\u5355\u53f7,\u7528\u6237\u6807\u8bc6,\u4ea4\u6613\u7c7b\u578b,\u4ea4\u6613\u72b6\u6001,\u4ed8\u6b3e\u94f6\u884c,\u8d27\u5e01\u79cd\u7c7b,\u603b\u91d1\u989d,\u4f01\u4e1a\u7ea2\u5305\u91d1\u989d,\u5fae\u4fe1\u9000\u6b3e\u5355\u53f7,\u5546\u6237\u9000\u6b3e\u5355\u53f7,\u9000\u6b3e\u91d1\u989d,\u4f01\u4e1a\u7ea2\u5305\u9000\u6b3e\u91d1\u989d,\u9000\u6b3e\u7c7b\u578b,\u9000\u6b3e\u72b6\u6001,\u5546\u54c1\u540d\u79f0,\u5546\u6237\u6570\u636e\u5305,\u624b\u7eed\u8d39,\u8d39\u7387\r\n...'
```
