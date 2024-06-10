import os
import socket as skt

class UDPClient():
    def __init__(self, sckt_family, sckt_type, client_addr, MAX_BUFF):
        self.sckt = skt.socket(sckt_family, sckt_type)
        self.server_addr = client_addr
        self.MAX_BUFF = MAX_BUFF

    def send_file(self, file_path):
        with open(file_path, 'rb') as file:
            while True:
                data = file.read(self.MAX_BUFF)
                if not data:
                    break
                self.sckt.sendto(data, self.server_addr)

    def receive_file(self, file_path):
        with open(file_path, 'wb') as file:
            while True:
                data, addr = self.sckt.recvfrom(self.MAX_BUFF)
                if not data:
                    break
                file.write(data)

class UDPServer():
    def __init__(self, sckt_family, sckt_type, server_addr, MAX_BUFF):
        self.sckt = skt.socket(sckt_family, sckt_type)
        self.server_addr = server_addr
        self.MAX_BUFF = MAX_BUFF

    def receive_file(self, file_path):
        with open(file_path, 'wb') as file:
            while True:
                data, addr = self.sckt.recvfrom(self.MAX_BUFF)
                if not data:
                    break
                file.write(data)

    def send_file(self, file_path):
        with open(file_path, 'rb') as file:
            while True:
                data = file.read(self.MAX_BUFF)
                if not data:
                    break
                self.sckt.sendto(data, addr_target)

# ... código existente ...

MAX_BUFF_SIZE = 1024 # Bytes (1KB)
addr_bind = ('127.0.0.1', 7070) # porta que o servidor será vinculado
addr_target = ('localhost', 8080) # pprta que o cliente será vinculado

client = UDPClient(skt.AF_INET, skt.SOCK_DGRAM, addr_target, MAX_BUFF_SIZE)
server = UDPServer(skt.AF_INET, skt.SOCK_DGRAM, addr_bind, MAX_BUFF_SIZE)

client.send_file('ProjetoInfraCom/hello.txt')
server.receive_file('ProjetoInfraCom/received.txt')