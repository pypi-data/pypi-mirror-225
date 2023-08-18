import time

from AndTools import pack_b, get_random_bin, get_md5, TEA

from AndroidQQ.proto import DeviceReport


def Tlv_head(head, data):
    pack = pack_b()
    pack.add_Hex(head)
    pack.add_int(len(data), 2)
    pack.add_bin(data)
    return pack.get_bytes()


class TLV:
    def __init__(self, info):
        self.pack = pack_b()
        self.info = info

    def T018(self):
        self.pack.empty()
        self.pack.add_Hex('00 01 00 00 06 00 00 00 00 10 00 00 00 00')
        self.pack.add_int(int(self.info.uin))
        self.pack.add_Hex('00 00 00 00')
        return Tlv_head('00 18', self.pack.get_bytes())

    def T001(self):
        self.pack.empty()
        self.pack.add_Hex('00 01')
        self.pack.add_bin(get_random_bin(4))
        self.pack.add_int(int(self.info.uin))
        self.pack.add_int(int(time.time()))
        self.pack.add_Hex('00 00 00 00 00 00')
        return Tlv_head('00 01', self.pack.get_bytes())

    def T142(self):
        self.pack.empty()
        self.pack.add_body(self.info.device.package_name, 4)
        return Tlv_head('01 42', self.pack.get_bytes())

    def T016(self):
        self.pack.empty()
        self.pack.add_Hex('00 00 00 05')
        self.pack.add_Hex('00 00 00 10')  # len
        self.pack.add_Hex('20 04 1E EE 9B 6B E0 65 3A 35 6F 4F AC 89 92 6F 3F 1C EB 7E')
        self.pack.add_body('com.tencent.qqlite', 2)
        self.pack.add_body('2.1.7', 2)
        self.pack.add_Hex('00 10')  # len
        self.pack.add_Hex('A6 B7 45 BF 24 A2 C2 77 52 77 16 F6 F3 6E B6 8D')
        return Tlv_head('00 16', self.pack.get_bytes())

    def T01B(self):
        self.pack.empty()
        self.pack.add_Hex('00 00 00 00 00 00 00 00 00 00 00 08 00 00 00 04 00 00 00 48 00 00 00 02 00 00 00 02 00 00 ')
        return Tlv_head('00 1B', self.pack.get_bytes())

    def T01D(self):
        self.pack.empty()
        self.pack.add_Hex('01 00 F7 FF 7C 00 00 00 00 00 00 00 00 00')
        return Tlv_head('00 1D', self.pack.get_bytes())

    def T01F(self):
        self.pack.empty()
        self.pack.add_Hex('01')
        self.pack.add_Hex('00 07')  # android len
        self.pack.add_Hex('61 6E 64 72 6F 69 64')  # android
        self.pack.add_Hex('00 01')
        self.pack.add_Hex('39')
        self.pack.add_Hex('00 02')
        self.pack.add_Hex('00 10')  # len
        self.pack.add_Hex('43 68 69 6E 61 20 4D 6F 62 69 6C 65 20 47 53 4D')  # China Mobile GSM
        self.pack.add_Hex('00 00 00 04')
        self.pack.add_Hex('77 69 66 69')  # wifi
        return Tlv_head('00 1F', self.pack.get_bytes())

    def T033(self):
        self.pack.empty()
        self.pack.add_bin(get_random_bin(16))
        return Tlv_head('00 33', self.pack.get_bytes())

    def T035(self):
        self.pack.empty()
        self.pack.add_Hex('00 00 00 73')
        return Tlv_head('00 35', self.pack.get_bytes())

    def T106(self):
        self.pack.empty()
        if self.info.device.client_type == 'Watch':
            self.pack.add_bin(self.info.UN_Tlv_list.T018)
            # Token0106
        else:
            password_md5 = get_md5(self.info.password.encode('utf-8'))
            self.pack.add_Hex('00 04')
            self.pack.add_bin(get_random_bin(4))
            self.pack.add_Hex('00 00 00 13 00 00 00 10 00 00 00 00 00 00 00 00')
            self.pack.add_int(int(self.info.uin))
            self.pack.add_int(self.info.login_time)
            self.pack.add_Hex('00 00 00 00 01')
            self.pack.add_bin(bytes.fromhex(password_md5))
            self.pack.add_bin(self.info.key_rand)
            self.pack.add_bin(self.info.Guid)
            self.pack.add_int(self.info.device.app_id)
            self.pack.add_Hex('00 00 00 01')
            self.pack.add_body(self.info.uin, 2)
            self.pack.add_Hex('00 00')
            _data = self.pack.get_bytes()
            _key = get_md5(bytes.fromhex(password_md5) + bytes.fromhex('00 00 00 00') + self.info.key_rand)
            _data = TEA.encrypt(_data, _key)

        return Tlv_head('01 06', self.pack.get_bytes())

    def T116(self):
        self.pack.empty()
        if self.info.device.client_type == 'Watch':
            self.pack.add_Hex('00 00 F7 FF 7C 00 01 04 00 00')
        else:
            self.pack.add_Hex('00 0A F7 FF 7C 00 01 04 00 01 5F 5E 10 E2')
        return Tlv_head('01 16', self.pack.get_bytes())

    def T100(self):
        client_type_map = {
            'Watch': ('00 00 00 05', '02 04 10 C0'),
            'Other': ('00 00 00 13', '02 14 10 E0')
        }

        _H = client_type_map.get(self.info.device.client_type, client_type_map['Other'])

        self.pack.empty()
        self.pack.add_Hex('00 01')
        self.pack.add_Hex(_H[0])
        self.pack.add_Hex('00 00 00 10')
        self.pack.add_int(self.info.device.app_id)
        self.pack.add_Hex('00 00 00 00')
        self.pack.add_Hex(_H[1])
        return Tlv_head('01 00', self.pack.get_bytes())

    def T107(self):
        self.pack.empty()
        self.pack.add_Hex('00 00 00 00 00 01 ')
        return Tlv_head('01 07', self.pack.get_bytes())

    def T109(self):

        self.pack.empty()
        self.pack.add_Hex(get_md5(self.info.device.android_id))
        # todo 还不确定
        return Tlv_head('01 09', self.pack.get_bytes())

    def T124(self):
        self.pack.empty()
        temp = '39'  # todo 不确定是什么,后面和普通安卓进行对比再确认
        self.pack.add_body(self.info.device.name, 2)
        self.pack.add_body(temp, 2, True)
        self.pack.add_int(2, 2)
        self.pack.add_body(self.info.device.internet, 2)
        self.pack.add_body(self.info.device.internet_type, 4)
        print(self.pack.get_bytes().hex())
        return Tlv_head('01 24', self.pack.get_bytes())

    def T128(self):
        self.pack.empty()
        self.pack.add_Hex('00 00 01 01 00 11 00 00 00')
        self.pack.add_body(self.info.device.model, 2)
        self.pack.add_body(self.info.Guid, 2)
        self.pack.add_body(self.info.device.brand, 2)
        return Tlv_head('01 28', self.pack.get_bytes())

    def T16E(self):
        self.pack.empty()
        self.pack.add_body(self.info.device.model, 2)
        return Tlv_head('01 6E', self.pack.get_bytes())

    def T52D(self):
        device_info = DeviceReport(
            bootloader='unknown',
            proc_version='Linux version 4.4.146 (build@ubuntu) (gcc version 4.8 (GCC) ) #1 SMP PREEMPT Thu Sep 1 '
                         '18:26:33 CST 2022',
            codename='REL',
            incremental='G9650ZHU2ARC6',
            fingerprint='samsung/star2qltezh/star2qltechn:9/PQ3B.190801.002/G9650ZHU2ARC6:user/release-keys',
            boot_id=self.info.device.boot_id,
            android_id=self.info.device.android_id.hex(),
            base_band='',
            inner_version='G9650ZHU2ARC6',
        )
        return Tlv_head('05 2D', device_info.SerializeToString())

    def T144(self):
        pack = pack_b()

        if self.info.device.client_type == 'Watch':
            methods = {
                self.T109,
                self.T124,
                self.T128,
                self.T16E,
            }
        else:
            methods = {
                self.T109,
                self.T52D,
                self.T124,
                self.T128,
                self.T16E,
            }

        pack.add_int(len(methods), 2)  # 数量
        # 循环调用每一个方法，并将结果添加到包中
        for method in methods:
            pack.add_bin(method())
        _data = pack.get_bytes()
        _data = TEA.encrypt(_data, self.info.key_rand)
        return Tlv_head('01 44', _data)

    def T145(self):
        """GUid"""
        self.pack.empty()
        self.pack.add_bin(self.info.Guid)
        _data = self.pack.get_bytes()
        return Tlv_head('01 45', _data)

    def T147(self):
        self.pack.empty()
        self.pack.add_Hex('00 00 00 10')
        self.pack.add_body(self.info.device.version, 2)
        self.pack.add_body(self.info.device.Sig, 2)
        return Tlv_head('01 47', self.pack.get_bytes())

    def T511(self):
        """
            office.qq.com
            qun.qq.comgamecenter.qq.comdocs.qq.commail.qq.com	ti.qq.com
            vip.qq.com
            tenpay.comqqweb.qq.comqzone.qq.com
            mma.qq.comgame.qq.comopenmobile.qq.comconnect.qq.com"""
        self.pack.empty()
        self.pack.add_Hex(
            '00 0E 01 00 0D 6F 66 66 69 63 65 2E 71 71 2E 63 6F 6D 01 00 0A 71 75 6E 2E 71 71 2E 63 6F 6D 01 00 11 67 61 6D 65 63 65 6E 74 65 72 2E 71 71 2E 63 6F 6D 01 00 0B 64 6F 63 73 2E 71 71 2E 63 6F 6D 01 00 0B 6D 61 69 6C 2E 71 71 2E 63 6F 6D 01 00 09 74 69 2E 71 71 2E 63 6F 6D 01 00 0A 76 69 70 2E 71 71 2E 63 6F 6D 01 00 0A 74 65 6E 70 61 79 2E 63 6F 6D 01 00 0C 71 71 77 65 62 2E 71 71 2E 63 6F 6D 01 00 0C 71 7A 6F 6E 65 2E 71 71 2E 63 6F 6D 01 00 0A 6D 6D 61 2E 71 71 2E 63 6F 6D 01 00 0B 67 61 6D 65 2E 71 71 2E 63 6F 6D 01 00 11 6F 70 65 6E 6D 6F 62 69 6C 65 2E 71 71 2E 63 6F 6D 01 00 0E 63 6F 6E 6E 65 63 74 2E 71 71 2E 63 6F 6D')
        return Tlv_head('05 11', self.pack.get_bytes())

    def T16A(self):
        self.pack.empty()
        self.pack.add_bin(self.info.UN_Tlv_list.T019)
        return Tlv_head('01 6A', self.pack.get_bytes())

    def T154(self):
        self.pack.empty()
        self.pack.add_int(self.info.seq)
        return Tlv_head('01 54', self.pack.get_bytes())

    def T141(self):
        self.pack.empty()
        self.pack.add_Hex('00 01')
        self.pack.add_body(self.info.device.internet, 2)
        self.pack.add_Hex('00 02')
        self.pack.add_body(self.info.device.internet_type, 2)
        return Tlv_head('01 41', self.pack.get_bytes())

    def T008(self):
        self.pack.empty()
        self.pack.add_Hex('00 00 00 00 08 04 00 00')
        return Tlv_head('00 08', self.pack.get_bytes())

    def T187(self):
        self.pack.empty()
        self.pack.add_body(self.info.device.Mac_bytes, 2)
        return Tlv_head('01 87', self.pack.get_bytes())

    def T188(self):
        _app_id = get_md5(str(self.info.device.app_id).encode())

        self.pack.empty()

        self.pack.add_body(_app_id, 2)
        return Tlv_head('01 88', self.pack.get_bytes())

    def T194(self):
        _IMEI = get_md5(self.info.device.IMEI)
        self.pack.empty()
        self.pack.add_body(_IMEI, 2)
        return Tlv_head('01 94', self.pack.get_bytes())

    def T191(self):
        self.pack.empty()
        self.pack.add_Hex('00')
        return Tlv_head('01 91', self.pack.get_bytes())

    def T202(self):
        self.pack.empty()
        self.pack.add_body(self.info.device.Bssid_bytes, 2)
        self.pack.add_body('<unknown ssid>', 2)
        return Tlv_head('02 02', self.pack.get_bytes())

    def T177(self):
        self.pack.empty()
        self.pack.add_Hex('01')
        self.pack.add_int(self.info.device.build_time)
        self.pack.add_body(self.info.device.sdk_version)
        return Tlv_head('01 77', self.pack.get_bytes())

    def T516(self):
        self.pack.empty()
        self.pack.add_Hex('00 00 00 00')
        return Tlv_head('05 16', self.pack.get_bytes())

    def T521(self):
        self.pack.empty()
        self.pack.add_Hex('00 00 00 73 00 00 ')
        return Tlv_head('05 21', self.pack.get_bytes())

    def T525(self):
        self.pack.empty()
        self.pack.add_Hex('00 00 00 00 00 00')
        return Tlv_head('05 25', self.pack.get_bytes())

    def T318(self):
        self.pack.empty()
        self.pack.add_bin(self.info.UN_Tlv_list.T065)
        return Tlv_head('03 18', self.pack.get_bytes())

    def T544(self):
        self.pack.empty()
        self.pack.add_Hex(
            '686568610000000101000000000000000101000504000000005d7f198100000002000000a60001000800000189c2162c3b0002000a333871733d453974467a00030004010000010005000401000001000400040000000000060004000000010007000401000005000800040100000600090020f88af80ad1b5201c476268acf5a4fce85e17fb856ebb833de816e013f32eb89c000a00105579f2d9bd726b85e21fda3ae5c7688d000b0010478ebf77c7c1cd7bfc78055dd5d0b092000c000401000001000d000400000002')
        return Tlv_head('05 44', self.pack.get_bytes())
