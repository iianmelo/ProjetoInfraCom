import socket as skt


MAX_BUFF_SIZE = 1024 # Bytes (1KB)

addr_bind = ('localhost', 5000) # porta que o cliente será vinculado / cada cliente deve ter uma porta diferente
addr_target = ('127.0.0.1', 7070) # porta que o client irá enviar dados (servidor)
clients = {}
accomodations = {}

class UDPClient():
    def __init__(self, sckt_family, sckt_type, sckt_binding, MAX_BUFF):
        self.sckt = skt.socket(sckt_family, sckt_type)
        self.sckt.bind(sckt_binding)
        self.sckt.settimeout(0.1)


        if self.sckt is None:
            raise "Socket not available."
    
        self.MAX_BUFF = MAX_BUFF #Tamanho máximo do buffer;

    def send(self, server_addr: tuple[str, str], msg: bytes, seq_num: int): # envia pacotes do arquivo para o servidor
        seq_num_bytes = seq_num.to_bytes(1, byteorder='big')  # Convertendo o número de sequência para 1 byte

        while True:
            command = seq_num_bytes + msg
            self.sckt.sendto(command, server_addr)
            response, _ = self.sckt.recvfrom(self.MAX_BUFF)
            print(response.decode())
            try:
                ack, _ = self.sckt.recvfrom(self.MAX_BUFF)
                if ack == seq_num_bytes:
                    break  # ACK correto recebido, sair do loop
            except skt.timeout:
                continue  # Timeout, reenviar pacote

    def send_file(self, server_addr: tuple[str, int]): # Assume-se que server_addr é uma tupla de string (IP) e int (porta)
        seq_num = 1 # Inicializa o número de sequência como 1. O nome do arquivo não é mais relevante aqui.
        while True:
            command = input("Digite o comando: ")
            # Verifica se a mensagem não excede o tamanho máximo do buffer.
            if len(command) <= self.MAX_BUFF - 1:
                self.send(server_addr, command.encode(), seq_num) # Envia a mensagem.
                seq_num = 1 if seq_num == 0 else 0 # Alterna o número de sequência.
            else:
                # Se a mensagem for maior que o buffer, divide e envia em partes.
                for i in range(0, len(command), self.MAX_BUFF - 1):
                    part = command[i:i+self.MAX_BUFF - 1]
                    self.send(server_addr, part.encode(), seq_num)
                    seq_num = 1 if seq_num == 0 else 0 # Alterna o número de sequência.

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
    print("Client started |port: 5000|.")
    client.send_file(addr_target)          #Envia o comando para o servidor.

main()
