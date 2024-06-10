import socket as skt
import time

#binding => ip:porta => localhost:7070
# MAX_BUFF => tam max msg (bytes)

MAX_BUFF_SIZE = 1024 # Bytes (1KB)

addr_bind = ('localhost', 8080) # porta que o cliente será vinculado
addr_target = ('127.0.0.1', 7070) # porta que o client irá enviar dados (servidor)

class UDPClient():
    def __init__(self, sckt_family, sckt_type, sckt_binding, MAX_BUFF):
        self.sckt = skt.socket(sckt_family, sckt_type)
        self.sckt.bind(sckt_binding)
        self.sckt.settimeout(0.1)
        self.EOF_MARKER = b"EOF"

        if self.sckt is None:
            raise "Socket not available."
    
        self.MAX_BUFF = MAX_BUFF

    def listen(self, server_addr: tuple[str, str]):
        while True:
            print("Listening... (client)")
            try:
                data, origin = self.sckt.recvfrom(self.MAX_BUFF)
                print(data.decode())
                if data.decode() == "STOP":
                    print("Server stopped the connection.")
                    self.sckt.close()
                    break
            except:
                continue

    def send(self, server_addr: tuple[str, str], msg: bytes):
        # client_addr: (localhost, 8080)
        self.sckt.sendto(msg, server_addr)
        time.sleep(0.0001)

    def send_file(self, file_path, server_addr: tuple[str, str]):
        with open(file_path, 'rb') as file:
            while True:
                data = file.read(self.MAX_BUFF)
                if not data:
                    print("File sent.")
                    break
                self.send(server_addr, data)
        self.send(server_addr, self.EOF_MARKER)

    def receive_file(self, file_path):
        with open(file_path, 'wb') as file:
            while True:
                data, addr = self.sckt.recvfrom(self.MAX_BUFF)
                if not data:
                    break
                file.write(data)

client = UDPClient(skt.AF_INET, skt.SOCK_DGRAM, addr_bind, MAX_BUFF_SIZE)
print("Client started.")

client.send_file('hello.txt', addr_target)