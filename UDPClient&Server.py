import os
import socket as skt

class UDPClient():
    def __init__(self, sckt_family, sckt_type, server_addr, MAX_BUFF):
        self.sckt = skt.socket(sckt_family, sckt_type)
        self.server_addr = server_addr
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
                self.sckt.sendto(data, addr)

# ... código existente ...

client = UDPClient(skt.AF_INET, skt.SOCK_DGRAM, addr_target, MAX_BUFF_SIZE)
client.send_file('path_to_file')
server.receive_file('received_file')
os.rename('received_file', 'new_file_name')
server.send_file('new_file_name')
client.receive_file('new_file_name')