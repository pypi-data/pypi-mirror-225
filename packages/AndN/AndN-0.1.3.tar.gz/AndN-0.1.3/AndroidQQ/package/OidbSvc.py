import json
# 对象数据服务
from google.protobuf.json_format import MessageToJson, MessageToDict

from AndroidQQ.proto import *
from AndroidQQ.package.head import *
from pyproto import ProtoBuf


def P_0xeb8(info):
    _dict = {1: 3768, 2: 1, 4: {1: 1, 2: 2}}
    _data = ProtoBuf(_dict).toBuf()
    _data = PackHeadNoToken(info, _data, 'OidbSvc.0xeb8')
    _data = Pack_(info, _data, Types=11, encryption=1, sso_seq=info.seq)
    return _data


def P_0x88d_1(info):
    msg = OidbSvc0x88d1()
    msg.field1 = 2189
    msg.field2 = 1
    msg.field4.field1 = 537046294
    msg.field4.field2.field1 = 799854399
    msg.field4.field2.field2.field7 = 0
    msg.field4.field2.field2.field24 = b''  # Replace this with your intended byte array
    # 序列化消息
    bytes_temp = msg.SerializeToString()
    bytes_temp = Pack_Head(info, bytes_temp, 'OidbSvc.0x88d_1')
    bytes_temp = Pack_(info, bytes_temp, Types=8, encryption=1, token=True)
    return bytes_temp


def P_0x88d_1_res(data):
    """返回字典"""
    new_msg = OidbSvc0x88d1r()
    new_msg.ParseFromString(data)
    return MessageToDict(new_msg)
