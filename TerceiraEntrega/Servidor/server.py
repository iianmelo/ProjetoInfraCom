import socket as skt
import random
import time
import os


#Criando a classe do servidor
class UDPServer():
    def __init__(self, sckt_family, sckt_type, sckt_binding, MAX_BUFF):
        self.sckt = skt.socket(sckt_family, sckt_type)
        self.sckt.bind(sckt_binding)
        self.sckt.settimeout(5.0)
        self.EOF_MARKER = b"EOF"  #Variável criada para marcar o final do arquivo enviado.
        self.MAX_BUFF = MAX_BUFF #Define o tamanho máximo do buffer.
        #Verifica se o socket foi criado.
        
        if self.sckt is None:
            raise "Socket not available."
        
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
                seq_num , nome = nome[0], nome[1:] #Separa o número de sequência do nome do arquivo.[]
                data = nome[1:]
                if random.random() < 0.1:
                    print(f"Simulated packet loss for file name with seq_num: {seq_num}")
                    continue  # Simula a perda do pacote ignorando o restante do código no loop
                if nome:
                    self.send(end, seq_num.to_bytes(1, 'big')) #Envia o nome do arquivo para o cliente.
                    print(f'Server sent ACK to data with seq_num: {seq_num}')
                    break
            except:
                continue
            ##NOVO BLOCO DE CÓDIGO
            command = data.decode()
            if command.startswith("login"):
                _, userName = command.split()
                if userName in clients:
                    self.send(end, b"Nome de usuario ja existe.")
                else:
                    clients[userName] = end
                    self.send(end, b"Login realizado com sucesso.") 
                    print(f"Usuario {userName} logado com sucesso ao endereço {end}.")
            elif command == "logout":
                userName = None
                for name, addr in clients.items():
                    if addr == end:
                        userName = name
                        break
                if userName:
                    del clients[userName]
                    self.send(end, b"Logout realizado com sucesso.")
                    print(f"Usuario {userName} deslogado com sucesso.")
            elif command.startswith("create"):
                _, name, location, description = command.split(maxsplit=3)
                if (name, location) in accomodations:
                    self.send(end, b"Acomodacao ja existente.")
                else:
                    accomodations[(name, location)] = {
                        "description": description,
                        "owner": end,
                        "bookings": {}
                    }
                    self.send(end, f"Acomodacao {nome} criada com sucesso.")
                    for client_name, client_addr in clients.items():
                        if client_addr != end:
                            self.send(client_addr, f"Acomodacao {nome} criada por {name}.")
            elif command.startswith("book"):
                _, owner, nome, location, day, room = command.split(maxsplit=5)
                if(name, location) not in accomodations:
                    self.send(end, b"Acomodacao nao encontrada.")
                else:
                    accomodation = accomodations[(name, location)]
                    if end == accomodation["owner"]:
                        self.send(end, b"Voce nao pode reservar sua propria acomodacao.")
                    elif day not in accomodation["bookings"]:
                        self.send(end, b"Data nao disponivel.")
                    else:
                        accomodation["bookings"][day] = end
                        self.send(end, f"Reserva realizada com sucesso.")
                        self.send(accomodation["owner"], f"Reserva realizada por na acomodacao {name}.")
            elif command.startswith("cancel"):
                _, owner, name, location, day = command.split(maxsplit=4)
                if(name, location) not in accomodations:
                    self.send(end, b"Acomodacao nao encontrada.")
                else:
                    accomodation = accomodations[(name, location)]
                    if day not in accomodation["bookings"] or accomodation["bookings"][day] != end:
                        self.send(end, b"Reserva nao encontrada.")
                    else:
                        del accomodation["bookings"][day]
                        self.send(end, b"Reserva cancelada com sucesso.")
                        self.send(accomodation["owner"], f"Reserva cancelada na acomodacao {name}.")
            elif command == "list:myacmd":
                userName = None
                for name, addr in clients.items():
                    if addr == end:
                        userName = name
                        break
                if userName:
                    my_accomodations = [f"{name}, {location}, descrição: {accomodation['description']}" for (name, location), accomodation in accomodations.items() if accomodation["owner"] == end]
                    self.send(end, "\n".join(my_accomodations).encode())
            elif command == "list:acmd":
                available_accomodations = [f"{name}, {location}, descrição: {accomodation['description']}" for (name, location), accomodation in accomodations.items()]
                self.send(end, "\n".join(available_accomodations).encode())
            elif command == "list:myrsv":
                userName = None
                for name, addr in clients.items():
                    if addr == end:
                        userName = name
                        break
                if userName:
                    my_reservations = [f"[{owner}/{addr[0]}:{addr[1]}] Reserva para {name} em {location} no dia {day}" for (name, location), accomodation in accomodations.items() for day, client in accomodation["bookings"].items() if client == addr]
                    self.send(end, "\n".join(my_reservations).encode())
            #####################
                                


        with open('Server_' + nome.decode(), 'wb') as file: 
            expected_seq_num = 1 # Inicializa o número de sequência esperado como 1.
            while True:
                try:
                    segment, addr = self.sckt.recvfrom(self.MAX_BUFF)
                    # Simula a perda de pacote com 10% de probabilidade
                    if random.random() < 0.1:
                        seq_num, data = segment[0], segment[1:] # Separa o número de sequência dos dados.
                        print(f"Simulated packet loss for data with seq_num: {seq_num}")
                        continue  # Simula a perda do pacote ignorando o restante do código no loop
                    seq_num, data = segment[0], segment[1:] # Separa o número de sequência dos dados.
                    if data == self.EOF_MARKER:
                        print("EOF marker received. File transfer complete.")
                        self.send(addr, seq_num.to_bytes(1, 'big')) # Envia o nome do arquivo que foi recebido com o nome alterado.
                        break
                    if seq_num == expected_seq_num:
                        file.write(data)
                        print(f"Received data from {addr} with seq_num: {seq_num}")
                        self.send(addr, seq_num.to_bytes(1, 'big')) # Envia um ACK para o cliente.
                        print(f'Server sent ACK to data with seq_num: {seq_num}')
                        expected_seq_num = 1 if expected_seq_num == 0 else 0 # Alterna o número de sequência esperado entre 0 e 1.
                    else:
                        # Se o número de sequência não for o esperado, reenvia o ACK do último pacote recebido corretamente
                        self.send(addr, ((expected_seq_num + 1) % 2).to_bytes(1, 'big'))
                except skt.timeout:
                    continue
                except Exception as e:
                    print(f"An error occurred: {e}")
                    break

MAX_BUFF_SIZE = 1024 # Bytes (1KB)

addr_bind = ('127.0.0.1', 7070) # porta que o servidor será vinculado.
addr_target = ('localhost', 8080) # porta que o servidor irá enviar dados (cliente).
clients = {}
accomodations = {}


def main():

    server = UDPServer(skt.AF_INET, skt.SOCK_DGRAM, addr_bind, MAX_BUFF_SIZE)
    print("Server started.")
    server.listen()     #O servidor começa a escutar.

main()
