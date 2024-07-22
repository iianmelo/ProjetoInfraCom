import socket as skt
import random
import time
import os

MAX_BUFF_SIZE = 1024 # Bytes (1KB)

addr_bind = ('localhost', 8080) # porta que o cliente será vinculado
addr_target = ('127.0.0.1', 7070) # porta que o client irá enviar dados (servidor)
clients = {}
accomodations = {}

class UDPClient():
    def __init__(self, sckt_family, sckt_type, sckt_binding, MAX_BUFF):
        self.sckt = skt.socket(sckt_family, sckt_type)
        self.sckt.bind(sckt_binding)
        self.sckt.settimeout(0.1)
        self.EOF_MARKER = b"EOF" #Variável criada para marcar o final do arquivo

        if self.sckt is None:
            raise "Socket not available."
    
        self.MAX_BUFF = MAX_BUFF #Tamanho máximo do buffer;

    def send(self, server_addr: tuple[str, str], msg: bytes, seq_num: int): # envia pacotes do arquivo para o servidor
        # client_addr: (localhost, 8080)
        seq_num_bytes = seq_num.to_bytes(1, byteorder='big')  # Convertendo o número de sequência para 1 byte
        msg_with_seq = seq_num_bytes + msg  # Concatenando o número de sequência com a mensagem

        while True:
            self.sckt.sendto(msg_with_seq, server_addr)
            print(f'Client sent data with seq_num {seq_num}')
            try:
                ack, _ = self.sckt.recvfrom(self.MAX_BUFF)
                if ack == seq_num_bytes:
                    break  # ACK correto recebido, sair do loop
            except skt.timeout:
                print(f"Timeout for data with seq_num {int.from_bytes(seq_num_bytes, byteorder='big')}")
                continue  # Timeout, reenviar pacote
            ##NOVO BLOCO DE CÓDIGO
            command = input("Digite o comando: ")
            if command.startswith("login"):
                #rdt_send(data)
                self.sckt.sendto(command.encode(), server_addr)
                response, _ = self.sckt.recvfrom(self.MAX_BUFF)
                print(response.decode())
            elif command == "logout":
                #rdt_send(data)
                self.sckt.sendto(command.encode(), server_addr)
                response, _ = self.sckt.recvfrom(self.MAX_BUFF)
                print(response.decode())
                break
            #elif command.startswith("create"):
            #    #Escrever código
            #    continue
            #elif command.startswith("book"):
            #    #Escrever código
            #    continue
            #elif command.startswith("cancel"):
            #    #Escrever código
            #    continue
            else:
                self.sckt.sendto(command.encode(), server_addr)
                response, _ = self.sckt.recvfrom(self.MAX_BUFF)
                print(response.decode())
            #####################

    def send_file(self, file_path, server_addr: tuple[str, str]): # envia o arquivo para o servidor
        seq_num = 1 # Inicializa o número de sequência como 1 já que o nome do aruivo é enviado com o número de sequência 0. 
        with open(file_path, 'rb') as file:
            while True:
                data = file.read(self.MAX_BUFF - 1) # Lê o arquivo em partes iguais ao MAX_BUFF, e continua de onde parou até o final do arquivo.
                if not data:
                    break
                self.send(server_addr, data, seq_num)    # Envia os dados do arquivo.
                seq_num = 1 if seq_num == 0 else 0 # Alterna o numero de seq dos pacotes entre 0 e 1.
        self.send(server_addr, self.EOF_MARKER, seq_num) # Envia para o servidor um sinal de que o arquivo acabou.
        print("File sent.")
        
    def listen(self):
        print("Listening (client)...")
        while True:
            try:
                nome, end = self.sckt.recvfrom(self.MAX_BUFF) # Recebe o nome do arquivo do servidor, já alterado.
                if nome: 
                    break
            except:
                continue
        with open(nome.decode(), 'wb') as file:           # Recebe a devolução do arquivo pelo servidor.
            while True:
                try: 
                    data, addr = self.sckt.recvfrom(self.MAX_BUFF)
                    if data == self.EOF_MARKER:
                        print("EOF marker received. File transfer complete.") 
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
    


def main():
    client = UDPClient(skt.AF_INET, skt.SOCK_DGRAM, addr_bind, MAX_BUFF_SIZE)
    print("Client started.")
    client.send(addr_target, 'Imagem.png'.encode(), 0)      #Envia o nome do arquivo para o servidor.
    print("Name sent")
    client.send_file('Imagem.png', addr_target)          #Envia o arquivo para o servidor.

    client.send() #Envia o comando para o servidor.

main()