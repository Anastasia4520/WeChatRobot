# -*-coding:utf-8-*-
'''
这个程序主要用来接通订阅号的URL，如果接通，url就会添加成功，并可以启用
在终端输入如下命令，即可运行程序
waitress-serve --port=80 connect:app
'''
import falcon
from falcon import uri
from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException

class Connect(object):

    def on_get(self, req, resp):
        query_string = req.query_string
        # 调试时查看一下返回的内容
        print(query_string)
        query_list = query_string.split('&')
        b = {}
        for i in query_list:
            b[i.split('=')[0]] = i.split('=')[1]

        try:
            check_signature(token='Anastasia', signature=b['signature'], timestamp=b['timestamp'], nonce=b['nonce'])
            resp.body = (b['echostr'])
        except InvalidSignatureException:
            pass
        resp.status = falcon.HTTP_200


app = falcon.API()
connect = Connect()
app.add_route('/connect', connect)


