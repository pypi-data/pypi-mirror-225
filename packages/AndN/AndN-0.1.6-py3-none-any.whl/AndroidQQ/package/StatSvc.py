import json
import zlib

from Jce import JceInputStream, JceStruct

from AndroidQQ.package.head import *


# 统计服务
def GetDevLoginInfo(info, **kwargs):
    jce = JceWriter()
    jce.write_bytes(info.Guid, 0)
    jce.write_string('com.tencent.mobileqq', 1)
    jce.write_int32(1, 2)
    jce.write_int32(0, 3)
    jce.write_int32(0, 4)
    jce.write_int32(20, 5)
    jce.write_int32(kwargs.get('type', 3), 6)
    _data = jce.bytes()

    jce = JceWriter()
    jce.write_jce_struct(_data, 0)
    _data = jce.bytes()

    jce = JceWriter()
    jce.write_map({'SvcReqGetDevLoginInfo': _data}, 0)
    _data = jce.bytes()
    _data = PackHeadNoToken(info, _data, 'StatSvc.GetDevLoginInfo', 'StatSvc', 'SvcReqGetDevLoginInfo')

    _data = Pack_(info, _data, Types=11, encryption=1, sso_seq=info.seq)
    return _data


def GetDevLoginInfo_res(data):
    if data[0] == 120:
        data = zlib.decompress(data)
    data = Un_jce_Head(data)
    data = Un_jce_Head_2(data)

    stream = JceInputStream(data)
    s = JceStruct()
    s.read_from(stream)
    return s.to_json()
