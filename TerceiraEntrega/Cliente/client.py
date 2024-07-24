import socket as skt


MAX_BUFF_SIZE = 1024 # Bytes (1KB)

addr_bind = ('localhost', 8080) # porta que o cliente será vinculado / cada cliente deve ter uma porta diferente
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
        x=0

        while x<1:
            ##COMANDOS
            #command = input("Digite o comando: ")
            if msg.decode().startswith("login"):
                command = seq_num_bytes + msg
                self.sckt.sendto(command, server_addr) #
                response, _ = self.sckt.recvfrom(self.MAX_BUFF)
                print(response.decode())
            elif msg.decode() == "logout":
                command = seq_num_bytes + msg
                self.sckt.sendto(command, server_addr)
                response, _ = self.sckt.recvfrom(self.MAX_BUFF)
                print(response.decode())
            else:
                command = seq_num_bytes + msg
                self.sckt.sendto(command, server_addr)
                response, _ = self.sckt.recvfrom(self.MAX_BUFF)
                print(response.decode())
            #####################
            try:
                ack, _ = self.sckt.recvfrom(self.MAX_BUFF)
                if ack == seq_num_bytes:
                    x=10
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

        #self.send(server_addr, self.EOF_MARKER, seq_num) # Envia sinal de que a mensagem acabou.
        
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
    #command = input("Digite o comando: ")
    #client.send(addr_target, "Imagem.png".encode(), 0)      #Envia o nome do arquivo para o servidor.
    #print("Finzalizou")
    client.send_file(addr_target)          #Envia o arquivo para o servidor.

    #client.send() #Envia o comando para o servidor.

main()
