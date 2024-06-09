import socket as skt
import time

#binding => ip:porta => localhost:7070
# MAX_BUFF => tam max msg (bytes)

class UDPServer():
    def __init__(self, sckt_family, sckt_type, sckt_binding, MAX_BUFF):
        self.sckt = skt.socket(sckt_family, sckt_type)
        self.sckt.bind(sckt_binding)
        self.sckt.settimeout(0.1)

        if self.sckt is None:
            raise "Socket not available."
    
        self.MAX_BUFF = MAX_BUFF

    def listen(self, client_addr: tuple[str, str]):
        while True:
            try:
                data, origin = self.sckt.recvfrom(self.MAX_BUFF)
            except:
                continue

    def send(self, client_addr: tuple[str, str], msg: bytes):
        # client_addr: (localhost, 8080)
        self.sckt.sendto(msg, client_addr)
        time.sleep(0.0001)

MAX_BUFF_SIZE = 1024 # Bytes (1KB)

addr_bind = ('127.0.0.1', 7070) # porta que o servidor será vinculado
addr_target = ('localhost', 8080) # porta que o servidor irá enviar dados (cliente)

server = UDPServer(skt.AF_INET, skt.SOCK_DGRAM, addr_bind, MAX_BUFF_SIZE)
server.listen()