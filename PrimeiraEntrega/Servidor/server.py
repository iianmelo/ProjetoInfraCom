import socket as skt
import time
import os

#Criando a classe do servidor
class UDPServer():
    def __init__(self, sckt_family, sckt_type, sckt_binding, MAX_BUFF):
        self.sckt = skt.socket(sckt_family, sckt_type)
        self.sckt.bind(sckt_binding)
        self.sckt.settimeout(5.0)
        #Verifica se o socket foi criado.
        if self.sckt is None:
            raise "Socket not available."
        
        #Define o tamanho máximo do buffer.
        self.MAX_BUFF = MAX_BUFF
        #Variável criada para marcar o final do arquivo enviado.
        self.EOF_MARKER = b"EOF"

    def send(self, client_addr: tuple[str, str], msg: bytes):
        self.sckt.sendto(msg, client_addr)
        time.sleep(0.0001)

    def send_file(self, file_path, client_addr: tuple[str, str]):
        with open(file_path, 'rb') as file:
            while True:
                data = file.read(self.MAX_BUFF)
                if not data:
                    break
                self.send(client_addr, data)
        self.send(client_addr, self.EOF_MARKER) #envia o marcador, indicando o final do arquivo.

    def listen(self):
        print("Listening (server)...")
        while True:
            try:
                nome, end = self.sckt.recvfrom(self.MAX_BUFF) #Recebe o nome do arquivo enviado pelo cliente.
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
                        self.send(addr, ('Modified_'+nome.decode()).encode()) #envia o nome do arquivo que foi recebido com o nome alterado.
                        break
                    if data:
                        file.write(data)
                        print(f"Received data from {addr}")
                    else:
                        break
                except skt.timeout:
                    continue
                except Exception as e:
                    print(f"An error occurred: {e}")
                    break
        self.send_file('Server_'+nome.decode(), addr) #envia o arquivo que foi recebido de volta para o cliente.

MAX_BUFF_SIZE = 1024 # Bytes (1KB)

addr_bind = ('127.0.0.1', 7070) # porta que o servidor será vinculado.
addr_target = ('localhost', 8080) # porta que o servidor irá enviar dados (cliente).


def main():

    server = UDPServer(skt.AF_INET, skt.SOCK_DGRAM, addr_bind, MAX_BUFF_SIZE)
    print("Server started.")
    server.listen()     #O servidor começa a escutar.

main()
