import socket as skt
import time

#binding => ip:porta => localhost:8080
# MAX_BUFF => tam max msg (bytes)

class UDPClient():
    def __init__(self, sckt_family, sckt_type, sckt_binding, MAX_BUFF):
        self.sckt = skt.socket(sckt_family, sckt_type)
        self.sckt.bind(sckt_binding)
        self.sckt.settimeout(0.1)

        if self.sckt is None:
            raise "Socket not available."
    
        self.MAX_BUFF = MAX_BUFF

    def listen(self, server_addr: tuple[str, str]):
        while True:
            try:
                data, origin = self.sckt.recvfrom(self.MAX_BUFF)
                if str(data) == "STOP": #
                    self.send(server_addr, "To saindo".encode())
                    self.sckt.close()
                    break
            except:
                continue # Avoid timeout errors
        
    def send(self, server_addr: tuple[str, str], msg: bytes):
        # server_addr: (localhost, 8081)
        self.sckt.sendto(msg, server_addr)
        time.sleep(0.0001)

MAX_BUFF_SIZE = 1024 # Bytes (1KB)

addr_bind = ('localhost', 8080) # porta que o cliente será vinculado
addr_target = ('127.0.0.1', 7070) # porta que o cliente irá enviar dados (servidor)

client = UDPClient(skt.AF_INET, skt.SOCK_DGRAM, addr_bind, MAX_BUFF_SIZE)
client.send(addr_target, "STOP".encode())
client.listen()