from AndTools import pack_u
from pydantic import BaseModel


class Un_Tlv:

    def __init__(self, data, info):
        self.info = info
        self.pack = pack_u(data)
        self.auth_info = {}
        self.handler_map = {
            '011a': lambda _data: setattr(self.info, 'uin_name', _data[5:].decode('utf-8')),
            '0120': lambda _data: setattr(self.info.cookies, 'skey', _data.decode('utf-8')),
            '0103': lambda _data: setattr(self.info.cookies, 'client_key', _data.hex()),
            '0004': lambda _data: setattr(self.info, 'uin', _data[4:].decode('utf-8')),
            '001e': lambda _data: setattr(self.info, 'key_rand', _data),  # 手表扫码返回的时候必须
            '0018': lambda _data: setattr(self.info.UN_Tlv_list, 'T018', _data),
            '0019': lambda _data: setattr(self.info.UN_Tlv_list, 'T019', _data),
            '0065': lambda _data: setattr(self.info.UN_Tlv_list, 'T065', _data),
            '0108': lambda _data: setattr(self.info.UN_Tlv_list, 'T108', _data),
            '010e': lambda _data: setattr(self.info.UN_Tlv_list, 'T10E', _data),
            '0134': lambda _data: setattr(self.info.UN_Tlv_list, 'T134', _data),
            '0114': lambda _data: setattr(self.info.UN_Tlv_list, 'T114', _data),
            '0133': lambda _data: setattr(self.info.UN_Tlv_list, 'T133', _data),
            '0143': lambda _data: setattr(self.info.UN_Tlv_list, 'T143_token_A2', _data),
            '010a': lambda _data: setattr(self.info.UN_Tlv_list, 'T10A_token_A4', _data),
            '0003': lambda _data: self.auth_info.__setitem__('0003', _data.decode('utf-8')),
            '0005': lambda _data: self.auth_info.__setitem__('0005', _data.decode('utf-8')),
            '0036': lambda _data: self.auth_info.__setitem__('0036', _data.decode('utf-8')),
            '0305': lambda _data: setattr(self.info, 'share_key', _data)
        }

    def _content(self, head, data):
        handler = self.handler_map.get(head)
        if handler:
            handler(data)
        else:
            print('tlv未解析', head, data.hex())

    def get_auth_result(self):
        return self.auth_info

    def return_specified_content(self):
        data = {
            'uin_name': self.info.uin_name,
            'guid': self.info.Guid.hex(),
            'token_A2': self.info.UN_Tlv_list.T143_token_A2,
            'token_A4': self.info.UN_Tlv_list.T10A_token_A4,
            'client_key': self.info.cookies.client_key,
        }
        return data

    def unpack(self):
        count = self.pack.get_short()
        for _ in range(count):
            head = self.pack.get_bin(2).hex()
            _len = self.pack.get_short()
            _data = self.pack.get_bin(_len)
            self._content(head, _data)

        return self.info
