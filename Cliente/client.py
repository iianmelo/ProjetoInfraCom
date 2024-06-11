import socket as skt
import time
import os

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
        
    def listen(self):
        print("Listening (client)...")
        while True:
            try:
                nome, end = self.sckt.recvfrom(self.MAX_BUFF)
                #os.rename(nome.decode(), 'Funcionou_'+nome.decode())
                if nome: 
                    break
            except:
                continue
        with open(nome.decode(), 'wb') as file: 
            while True:
                try: 
                    data, addr = self.sckt.recvfrom(self.MAX_BUFF)
                    if data == self.EOF_MARKER:
                        print("EOF marker received. File transfer complete.")
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




def main():
    client = UDPClient(skt.AF_INET, skt.SOCK_DGRAM, addr_bind, MAX_BUFF_SIZE)
    print("Client started.")
    client.send(addr_target, 'Imagem.png'.encode())
    client.send_file('Imagem.png', addr_target)
    client.listen()

main()