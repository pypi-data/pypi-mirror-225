import socket
import select

import threading
import time
import uuid
from AndTools import pack_u, pack_b

clients = []

client_info = {}


def repackage(data, client):
    """重组包体"""
    global client_info
    _uuid = client_info[client]['uuid']
    client_info[client]['data'] = client_info[client]['data'] + data

    pack_ = pack_u(client_info[client]['data'])

    while True:

        if pack_.get_len() <= 4:
            """小于4个字节直接跳出"""
            break
        _len = pack_.get_int()

        if _len <= pack_.get_len() + 4:
            _bin = pack_.get_bin(_len - 4)
            _func = client_info[client]['func']
            _func(_bin)
            client_info[client]['data'] = pack_.get_all()
            pack_ = pack_u(client_info[client]['data'])
        else:
            pack = pack_b()
            pack.add_int(_len)
            pack.add_bin(pack_.get_all())
            pack_ = pack_u(pack.get_bytes())
            break


def disconnect_client(client):
    """断开客户端连接"""
    clients.remove(client)
    client.close()
    client_info.pop(client)


def receive_data_all():
    """接收全部连接的数据"""

    while True:
        time.sleep(0.1)
        if not clients:
            continue
        readable, _, _ = select.select(clients, [], [], 0)
        for client in readable:
            try:
                data = client.recv(1024)
                if not data:
                    disconnect_client(client)
                    print('断开连接')
                else:
                    repackage(data, client)
            except (ConnectionResetError, socket.error):
                print("连接已被客户端重置。")
                disconnect_client(client)


# def receive_data(sock):
#     while True:
#         data = sock.recv(1024)
#         if not data:
#             break
#         print(f"从服务器收到的数据: {data.hex()}")


def start_client(hostname, port, _func=None):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip_address = socket.gethostbyname(hostname)
    client.connect((ip_address, port))
    # 生成一个UUID作为客户端的唯一标识符
    client_uuid = str(uuid.uuid4())
    client_info[client] = client_uuid
    client_info[client] = {
        'uuid': client_uuid,
        'data': b'',
        'func': _func
    }
    clients.append(client)

    return client


def start_tcp_service():
    """启动接收线程"""

    receive_thread = threading.Thread(target=receive_data_all, daemon=True)
    receive_thread.start()
    print('启动接收线程')


start_tcp_service()

if __name__ == "__main__":
    pass
