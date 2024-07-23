import socket as skt
import random
import time
import os

MAX_BUFF_SIZE = 1024 # Bytes (1KB)

addr_bind = ('192.168.100.100', 8080) # porta que o cliente será vinculado / cada cliente deve ter uma porta diferente
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
                continue  # Timeout, reenviar pacote
           
            ##COMANDOS
            command = input("Digite o comando: ")
            if command.startswith("login"):
                self.sckt.sendto(command.encode(), server_addr) #
                response, _ = self.sckt.recvfrom(self.MAX_BUFF)
                print(response.decode())
            elif command == "logout":
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

    def send_file(self, command: str, server_addr: tuple[str, int]): # Assume-se que server_addr é uma tupla de string (IP) e int (porta)
        seq_num = 1 # Inicializa o número de sequência como 1. O nome do arquivo não é mais relevante aqui.
        
        # Verifica se a mensagem não excede o tamanho máximo do buffer.
        if len(command) <= self.MAX_BUFF - 1:
            self.send(server_addr, command.encode(), seq_num) # Envia a mensagem.
        else:
            # Se a mensagem for maior que o buffer, divide e envia em partes.
            for i in range(0, len(command), self.MAX_BUFF - 1):
                part = command[i:i+self.MAX_BUFF - 1]
                self.send(server_addr, part.encode(), seq_num)
                seq_num = 1 if seq_num == 0 else 0 # Alterna o número de sequência.

        self.send(server_addr, self.EOF_MARKER, seq_num) # Envia sinal de que a mensagem acabou.
        print("Message sent.")
        
    def listen(self):
        print("Listening (client)...")
        while True:
            try:
                nome, end = self.sckt.recvfrom(self.MAX_BUFF) # Recebe o nome do arquivo do servidor, já alterado.
                if nome: 
                    break
            except:
                continue
       
    


def main():
    client = UDPClient(skt.AF_INET, skt.SOCK_DGRAM, addr_bind, MAX_BUFF_SIZE)
    print("Client started.")
    client.send(addr_target, 'Imagem.png'.encode(), 0)      #Envia o nome do arquivo para o servidor.
    print("Name sent")
    client.send_file('Imagem.png', addr_target)          #Envia o arquivo para o servidor.

    client.send() #Envia o comando para o servidor.

main()