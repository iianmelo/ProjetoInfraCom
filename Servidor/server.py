import socket as skt
import time
import os

#binding => ip:porta => localhost:7070
# MAX_BUFF => tam max msg (bytes)

class UDPServer():
    def __init__(self, sckt_family, sckt_type, sckt_binding, MAX_BUFF):
        self.sckt = skt.socket(sckt_family, sckt_type)
        self.sckt.bind(sckt_binding)
        self.sckt.settimeout(5.0)

        if self.sckt is None:
            raise "Socket not available."
    
        self.MAX_BUFF = MAX_BUFF
        self.EOF_MARKER = b"EOF"

    def listen2(self, client_addr: tuple[str, str]):
        print("Listening (server)...")
        while True:
            try:
                data, origin = self.sckt.recvfrom(self.MAX_BUFF)
            except:
                continue

    def send(self, client_addr: tuple[str, str], msg: bytes):
        # client_addr: (localhost, 8080)
        self.sckt.sendto(msg, client_addr)
        time.sleep(0.0001)

    def send_file(self, file_path, client_addr: tuple[str, str]):
        #new_file_path = 'Modified_' + file_path
        #os.rename(file_path, new_file_path)
        with open(file_path, 'rb') as file:
            while True:
                data = file.read(self.MAX_BUFF)
                if not data:
                    break
                self.send(client_addr, data)
        self.send(client_addr, self.EOF_MARKER)

    def listen(self):
        print("Listening (server)...")
        while True:
            try:
                nome, end = self.sckt.recvfrom(self.MAX_BUFF)
                if nome: 
                    break
            except:
                continue
        with open('Server_'+nome.decode(), 'wb') as file: 
            while True:
                try: 
                    data, addr = self.sckt.recvfrom(self.MAX_BUFF)
                    if data == self.EOF_MARKER:
                        print("EOF marker received. File transfer complete.")
                        #os.rename(nome.decode(), 'Funcionou_'+nome.decode())
                        self.send(addr, ('Modified_'+nome.decode()).encode())
                        break
                    if data:
                        file.write(data)
                        #print(f"{data.decode()}")
                        print(f"Received data from {addr}")
                    else:
                        break
                except skt.timeout:
                    continue
                except Exception as e:
                    print(f"An error occurred: {e}")
                    break
        self.send_file('Server_'+nome.decode(), addr)

MAX_BUFF_SIZE = 1024 # Bytes (1KB)

addr_bind = ('127.0.0.1', 7070) # porta que o servidor será vinculado
addr_target = ('localhost', 8080) # porta que o servidor irá enviar dados (cliente)


def main():
    server = UDPServer(skt.AF_INET, skt.SOCK_DGRAM, addr_bind, MAX_BUFF_SIZE)
    print("Server started.")
    server.listen()

main()
