import socket
import select

import threading
import time
import uuid
from AndTools import pack_u, pack_b

clients = []

client_info = {}
receive_thread = None


def repackage(data, client, _func):
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
            _func(_bin)
            client_info[client]['data'] = pack_.get_all()
            pack_ = pack_u(client_info[client]['data'])
        else:
            pack = pack_b()
            pack.add_int(_len)
            pack.add_bin(pack_.get_all())

            pack_ = pack_u(pack.get_bytes())
            break


def receive_data_all(clients):
    """接收全部连接的数据"""
    global client_info

    while True:
        time.sleep(0.1)
        # todo 下面代码存在问题
        if len(clients) == 0:
            continue
        # 从元组列表中提取客户端套接字
        client_sockets = [client for client, _ in clients]
        readable, _, _ = select.select(client_sockets, [], [])
        for client in readable:
            # 查找当前客户端对应的函数 (_func)
            _func = next(func for cli, func in clients if cli == client)
            data = client.recv(1024)
            if not data:
                clients.remove((client, _func))
                client.close()
                client_info.pop(client)
                print('断开连接')
            else:
                # print(f"从客户端收到的数据: {data.hex()}")
                if _func is not None:
                    repackage(data, client, _func)


# def receive_data(sock):
#     while True:
#         data = sock.recv(1024)
#         if not data:
#             break
#         print(f"从服务器收到的数据: {data.hex()}")


def start_client(host, port, _func=None):
    global receive_thread
    if not receive_thread.is_alive():
        start_tcp_service()

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    # 生成一个UUID作为客户端的唯一标识符
    client_uuid = str(uuid.uuid4())
    client_info[client] = client_uuid
    client_info[client] = {
        'uuid': client_uuid,
        'data': b''
    }
    clients.append((client, _func))

    return client


def start_tcp_service():
    """启动接收线程"""

    global receive_thread
    receive_thread = threading.Thread(target=receive_data_all, args=(clients,), daemon=True)
    receive_thread.start()
    print('启动接收线程')


start_tcp_service()

if __name__ == "__main__":
    pass
