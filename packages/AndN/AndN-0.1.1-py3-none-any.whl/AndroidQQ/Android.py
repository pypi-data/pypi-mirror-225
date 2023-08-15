import json

from AndTools import get_md5
from pydantic import BaseModel

from AndroidQQ.proto import *

from AndroidQQ.Tcp import *

import AndroidQQ.package.OidbSvc as OidbSvc
import AndroidQQ.package.StatSvc as StatSvc
import AndroidQQ.package.wtlogin as wt_login
import AndroidQQ.package.MQUpdateSvc_com_qq_ti as MQUpdateSvc
from AndroidQQ.package.head import *


class cookies(BaseModel):
    skey: str = None
    client_key: str = None


class device(BaseModel):
    # 软件信息
    version: str = None
    package_name: str = None  # com.tencent.qqlite
    Sig: bytes = None  # A6 B7 45 BF 24 A2 C2 77 52 77 16 F6 F3 6E B6 8D
    build_time: int = None  # 软件构建时间 1654570540
    sdk_version: str = None  # #6.0.0.2366
    client_type: str = None  # android
    app_id: int = None
    var: bytes = None

    # 设备信息
    name: str = 'android'
    internet: str = 'China Mobile GSM'
    internet_type: str = 'wifi'
    model: str = 'V1916A'
    brand: str = 'vivo'
    Mac_bytes: bytes = None  # '02:00:00:00:00:00'
    Bssid_bytes: bytes = None  # '00:14:bf:3a:8a:50'
    android_id: bytes = None  # 4cba299189224ca5 Android 操作系统中设备的一个唯一ID。每个设备在首次启动时都会生成一个随机的64位数字作为其
    boot_id: str = '65714910-7454-4d01-a148-6bdf337a3812'  # Linux系统中用来唯一标识系统自上次启动以来的运行时期的标识符
    IMEI: bytes = None


class UN_Tlv_list(BaseModel):
    T10A_token_A4: bytes = b''
    T143_token_A2: bytes = b''
    T100_qr_code_mark: bytes = b''  # watch
    T018: bytes = b''  # watch
    T019: bytes = b''  # watch
    T065: bytes = b''  # watch
    T108: bytes = b''
    T10E: bytes = b''
    T134: bytes = b''
    T114: bytes = b''
    T133: bytes = b''


#


class info_model(BaseModel):
    uin: str = '0'
    uin_name: str = None
    password: str = None
    seq: int = 5267
    share_key: bytes = None
    key_rand: bytes = get_random_bin(16)
    key_tg: bytes = None
    key_Pubkey: bytes = None  # 公钥
    Guid: bytes = get_random_bin(16)
    login_time: int = int(time.time())

    UN_Tlv_list: UN_Tlv_list = UN_Tlv_list()
    device: device = device()
    cookies: cookies = cookies()


class AndroidQQ:
    def __init__(self, **kwargs):
        """
        :param client_type: QQ or Watch
        :param kwargs:
        """
        self.info = info_model()
        self.info.device.Mac_bytes = bytes.fromhex(get_md5('02:00:00:00:00:00'.encode()))
        self.info.device.Bssid_bytes = bytes.fromhex(get_md5('00:14:bf:3a:8a:50'.encode()))
        client_type = kwargs.setdefault('client_type', 'QQ')
        self.info.device.client_type = client_type
        if client_type == 'QQ':
            self.info.device.app_id = 537170024
            self.info.device.android_id = bytes.fromhex('d018b704652f41f4')
            self.info.device.package_name = 'com.tencent.mobileqq'
            self.info.device.var = '||A8.9.71.9fd08ae5'.encode()
            self.info.device.IMEI = '498054355930458'.encode()
        elif client_type == 'Tim':
            self.info.device.app_id = 537162285
            self.info.device.package_name = 'com.tencent.tim'
            self.info.device.var = '||A3.5.2.3f4af297'.encode()
            self.info.device.IMEI = '877408608703263'.encode()



        elif client_type == 'Watch':
            self.info.device.app_id = 537140974
            self.info.device.android_id = bytes.fromhex('4cba299189224ca2')
            self.info.uin = '0'
            self.info.device.package_name = 'com.tencent.qqlite'
            self.info.device.version = '2.1.7'
            self.info.device.Sig = bytes.fromhex('A6 B7 45 BF 24 A2 C2 77 52 77 16 F6 F3 6E B6 8D')
            self.info.device.build_time = int('1654570540')  # 2022-06-07 10:55:40 软件构建时间
            self.info.device.sdk_version = '6.0.0.2366'
            self.info.key_Pubkey = bytes.fromhex(
                '04 04 6E 31 F8 59 79 DF 7F 3D F0 31 CD C6 EB D9 B9 8E E2 E2 F6 3E FB 6E 79 BC 54 BF EE FB 0F 60 24 07 DA 8C 41 4A 34 EF 46 10 A7 95 48 0E F8 3F 0E')  # 49 长度的
            self.info.share_key = bytes.fromhex('54 9F 5C 3A B4 8D B9 16 DA 96 5F 3B 1B C1 03 4B')
            self.info.key_rand = bytes.fromhex('70 3F 79 79 55 78 2E 55 63 64 3A 44 38 49 7A 53')
            self.info.Guid = bytes.fromhex('9b6be0653a356f4fac89926f3f1ceb7e')
            IMEI = '866174040000000'
            self.info.device.IMEI = bytes(IMEI, 'utf-8')
            self.info.device.var = bytes(IMEI, 'utf-8')

        self._tcp = start_client('36.155.187.71', 8080, self.UN_data)
        self.pack_list = {}

    def Set_TokenA(self, data):

        """
        appid
            537085851 小栗子二开
            537101242 小栗子



        """
        json_data = json.loads(data)
        uin = json_data['UIN']
        device_APPID = json_data.get('device_APPID')

        if device_APPID is not None:
            # 向下兼容
            appid = int.from_bytes(bytes.fromhex(device_APPID), 'big')
        else:
            # 获取appid
            appid = int(json_data.get('Appid', self.info.device.app_id))

        # appid = int('537085851')
        # print('appid', appid)
        self.info.uin = str(json_data['UIN'])
        self.info.UN_Tlv_list.T10A_token_A4 = bytes.fromhex(json_data['token_A4'])
        self.info.UN_Tlv_list.T143_token_A2 = bytes.fromhex(json_data['token_A2'])
        self.info.share_key = bytes.fromhex(json_data['Sharekey'].replace(' ', ''))
        self.info.Guid = bytes.fromhex(json_data['GUID_MD5'])
        self.info.device.app_id = appid  # 现在必须验证这个参数了
        self.info.UN_Tlv_list.T10E = bytes.fromhex(json_data['T10E'])
        self.info.UN_Tlv_list.T134 = bytes.fromhex(json_data['T134'])
        self.info.UN_Tlv_list.T114 = bytes.fromhex(json_data['T114'])
        self.info.UN_Tlv_list.T133 = bytes.fromhex(json_data['T133'])

    def UN_data(self, data):
        """解包"""
        pack = pack_u(data)
        pack.get_int()
        pack_way = pack.get_byte()

        pack.get_byte()  # 00
        _len = pack.get_int()
        pack.get_bin(_len - 4)  # Uin bin
        _data = pack.get_all()
        if pack_way == 2:
            # 登录相关
            _data = TEA.decrypt(_data, '00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00')
        elif pack_way == 1:
            _data = TEA.decrypt(_data, self.info.share_key)
        else:
            _data = b''
            print('未知的解密类型')

        if _data == b'':
            return
        else:
            pack = pack_u(_data)
            _len = pack.get_int()
            part1 = pack.get_bin(_len - 4)
            _len = pack.get_int()
            part2 = pack.get_bin(_len - 4)
            # part1
            pack = pack_u(part1)
            ssoseq = pack.get_int()
            pack.get_int()
            _len = pack.get_int()
            Tips = pack.get_bin(_len - 4).decode('utf-8')
            _len = pack.get_int()
            Cmd = pack.get_bin(_len - 4).decode('utf-8')
            if Tips != '':
                print('Tips', Tips)
            # part2
            if ssoseq > 0:
                # print('包序号', ssoseq, '包类型', Cmd, part2.hex())
                self.pack_list.update({ssoseq: part2})
            else:
                pass
                # print('推送包', '包类型', Cmd, part2.hex())

    def get_seq(self):
        """获取缓存测试"""
        # todo 详细测试完可以删除
        return len(self.pack_list)

    def Tcp_send(self, data):
        self._tcp.sendall(data)
        start_time = time.time()  # 获取当前时间
        ssoseq = self.info.seq
        while time.time() - start_time < 3:  # 检查是否已过去三秒
            data = self.pack_list.get(ssoseq)
            if data is not None:
                self.pack_list.pop(ssoseq)  # 删除已经取出的包
                break
            time.sleep(0.1)
        self.info.seq = ssoseq + 1

        return data

    def no_tail_login(self):
        """无尾登录包"""
        data = OidbSvc.P_0x88d_1(self.info)
        data = self.Tcp_send(data)
        data = OidbSvc.P_0x88d_1_res(data)
        return data

    def get_dev_login_info(self, **kwargs):
        """
           获取设备登录信息。
               **kwargs: 可变数量的关键字参数，包括：
                   type (int): 设备类型。1 表示在线设备，2 表示离线设备，3 表示全部设备。默认为 3。

           Returns:
               返回获取到的设备登录信息。
           """
        data = StatSvc.GetDevLoginInfo(self.info, **kwargs)
        data = self.Tcp_send(data)
        data = StatSvc.GetDevLoginInfo_res(data)
        return data

    def watch_scan_code(self, verify=False):
        """手表扫码"""

        data = wt_login.trans_emp(self.info, verify)

        data = self.Tcp_send(data)
        data = wt_login.trans_emp_res(data, self.info, verify)

        return data

    def scan_code_auth(self, **kwargs):
        """扫码授权"""
        data = wt_login.trans_emp_auth(self.info, **kwargs)

        data = self.Tcp_send(data)
        data = wt_login.trans_emp_auth_res(data, self.info, **kwargs)
        return data

    def login(self, **kwargs):
        """登录"""
        data = wt_login.login(self.info, **kwargs)
        data = self.Tcp_send(data)
        wt_login.login_res(data, self.info)

    def scan_Login(self, **kwargs):
        """扫码登录/辅助验证"""
        data = MQUpdateSvc.web_scan_login(self.info, **kwargs)
        data = self.Tcp_send(data)
        data = MQUpdateSvc.web_scan_login_res(data)
        return data

    def get_specified_info(self):
        """获取指定信息"""
        # 兼容其他源码
        data = {
            "UIN": self.info.uin,
            "GUID_MD5": self.info.Guid.hex(),
            "token_A4": self.info.UN_Tlv_list.T10A_token_A4.hex(),
            "token_A2": self.info.UN_Tlv_list.T143_token_A2.hex(),
            "Sharekey": self.info.share_key.hex(),
            "T134": self.info.UN_Tlv_list.T134.hex(),
            "T133": self.info.UN_Tlv_list.T133.hex(),
            "T10E": self.info.UN_Tlv_list.T10E.hex(),
            "T114": self.info.UN_Tlv_list.T114.hex(),
            "device_APPID": self.info.device.app_id.to_bytes(4, 'big').hex()
        }
        return json.dumps(data)

    def get_phone(self):
        """获取手机号"""
        data = OidbSvc.P_0xeb8(self.info)
        data = self.Tcp_send(data)
        print(data.hex())
