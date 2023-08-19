import socket

def check_port_open(ip, port):
    tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_result = tcp_sock.connect_ex((ip, port))
    tcp_sock.close()
    #print(tcp_result)

    if tcp_result == 0:
        return True
    else:
        return False
