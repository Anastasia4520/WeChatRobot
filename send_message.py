# -*-coding:utf-8-*-
import falcon
from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException
from wechatpy import parse_message
from wechatpy.replies import TextReply, ImageReply
from pymongo import MongoClient
import random
'''
遇到不懂的问题？Python学习交流群：821460695满足你的需求，资料都已经上传群文件，可以自行下载！
'''
client = MongoClient('localhost')
db = client['test']
table = db['joke']

class Connect(object):

    def on_get(self, req, resp):
        query_string = req.query_string
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

    def on_post(self, req, resp):
        xml = req.stream.read()
        msg = parse_message(xml)
        if msg.type == 'text':
            if msg.content=='笑话':
                cursor = table.find({'id':random.randint(1,6)})
                for i in cursor:
                    content = i["joke"]
                    print(content)
                reply = TextReply(content=content, message=msg)
                xml = reply.render()
            else:
                print(msg, msg.content)
                reply = TextReply(content=msg.content, message=msg)
            xml = reply.render()
            resp.body = (xml)
            resp.status = falcon.HTTP_200
        elif msg.type == 'image':
            reply = ImageReply(media_id=msg.media_id, message=msg)
            xml = reply.render()
            resp.body = (xml)
            resp.status = falcon.HTTP_200

app = falcon.API()
connect = Connect()
app.add_route('/connect', connect)