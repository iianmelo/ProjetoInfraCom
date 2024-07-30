import socket as skt
import threading


MAX_BUFF_SIZE = 1024 # Bytes (1KB)

addr_bind = ('localhost', 5500) # porta que o cliente será vinculado / cada cliente deve ter uma porta diferente
addr_target = ('127.0.0.1', 7070) # porta que o client irá enviar dados (servidor)
clients = {}
accomodations = {}

event = threading.Event()

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
            ##
            response, _ = self.sckt.recvfrom(self.MAX_BUFF)
            print(response.decode())
            try:
                ack, _ = self.sckt.recvfrom(self.MAX_BUFF)
                if ack == seq_num_bytes:
                    ##
                    break  # ACK correto recebido, sair do loop
            except skt.timeout:
                continue  # Timeout, reenviar pacote

    def send_file(self, server_addr: tuple[str, int]): # Assume-se que server_addr é uma tupla de string (IP) e int (porta)
        seq_num = 1 # Inicializa o número de sequência como 1. O nome do arquivo não é mais relevante aqui.
        while True:
            command = (input("")).encode()
            # Verifica se a mensagem não excede o tamanho máximo do buffer.
            if len(command) <= self.MAX_BUFF - 1:
                seq_num_bytes = seq_num.to_bytes(1, byteorder='big')  # Convertendo o número de sequência para 1 byte

                while True:
                    print("--------------------------------------")
                    event.clear()
                    command = seq_num_bytes + command
                    self.sckt.sendto(command, server_addr)
                    try:
                        ack, _ = self.sckt.recvfrom(self.MAX_BUFF)
                        if ack == seq_num_bytes:
                            event.set()
                            break  # ACK correto recebido, sair do loop
                    except skt.timeout:
                        continue  # Timeout, reenviar pacote
                seq_num = 1 if seq_num == 0 else 0 # Alterna o número de sequência.
            else:
                # Se a mensagem for maior que o buffer, divide e envia em partes.
                for i in range(0, len(command), self.MAX_BUFF - 1):
                    part = command[i:i+self.MAX_BUFF - 1]
                    self.send(server_addr, part.encode(), seq_num)
                    seq_num = 1 if seq_num == 0 else 0 # Alterna o número de sequência.

    def listen(self):
        event.set()
        while True:
            event.wait()
            try:
                response, _ = self.sckt.recvfrom(self.MAX_BUFF)
                if response:
                    print(response.decode())
                    print("--------------------------------------")
                    
            except skt.timeout:
                continue
            except:
                continue
       
    

def main():
    client = UDPClient(skt.AF_INET, skt.SOCK_DGRAM, addr_bind, MAX_BUFF_SIZE)
    print("Client started |port: 5500|.")
    send_thread = threading.Thread(target=client.send_file, args=(addr_target,))
    listen_thread = threading.Thread(target=client.listen)
    send_thread.start()
    listen_thread.start()

    send_thread.join()
    listen_thread.join()

main()

