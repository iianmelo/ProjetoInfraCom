import socket as skt
import datetime
import time
import os

MAX_BUFF_SIZE = 1024 # Bytes (1KB)
addr_bind = ('127.0.0.1', 7070) # porta que o servidor será vinculado.
addr_target = ('localhost', 8080) # porta que o servidor irá enviar dados (cliente).
clients = {}
accomodations = {}

#Definindo a faixa de datas disponíveis
data_inicio = datetime.date(2024, 7, 17)
data_fim = datetime.date(2024, 7, 22)
delta = datetime.timedelta(days=1)
available_dates = {}

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
        expected_seq_num = 1 # Inicializa o número de sequência esperado como 1.
        while True:
            try:
                data, end = self.sckt.recvfrom(self.MAX_BUFF) #Recebe o input e o ack referente ao input.
                seq_num , data = data[0], data[1:] #Separa o número de sequência do conteudo do input

                #verifica se o número de sequência é o esperado(garantindo a ordem dos pacotes)
                if seq_num == expected_seq_num:
                    command = data.decode()
                    #LOGIN
                    if command.startswith("login"): #Verifica se o comando é um login
                        _, userName = command.split() #Separa o comando do nome do usuário
                        if userName in clients:
                            self.send(end, b"Ja existe um usuario logado com esse nome.")
                        else:
                            clients[userName] = end #Adiciona o nome do usuário com o endereço ao dicionário de clientes online.
                            self.send(end, b"Voce esta online!") 
                            print(f"Usuario {userName}/{end} logado com sucesso!")
                    #LOGOUT
                    elif command == "logout":
                        userName = None
                        for name, addr in clients.items():
                            if addr == end:
                                userName = name #Remove o usuário do dicionário de clientes online.
                                break
                        if userName:
                            del clients[userName]
                            self.send(end, b"Logout realizado com sucesso.")
                            print(f"Usuario {userName} deslogado com sucesso.")
                    #CREATE
                    elif command.startswith("create"):
                        _, name_accommodation, location = command.split(maxsplit=2)
                        if end not in clients.values(): #Verifica se o usuário está logado
                            self.send(end, b"Voce nao esta logado.")
                        else:
                            if (name_accommodation, location) in accomodations:
                                self.send(end, b"Acomodacao ja existente.")
                            else:
                                while data_inicio <= data_fim: #Percorre as datas disponíveis
                                    available_dates[data_inicio.strftime("%Y-%m-%d")] = True  # Marca como disponível
                                    start_date += delta

                                # Adiciona a acomodação com os dias disponíveis    
                                accomodations[(name_accommodation, location)] = { #Adiciona a acomodação ao dicionário de acomodações
                                    "owner": end,
                                    "bookings": {} #Dicionário para armazenar as reservas
                                }
                                self.send(end, f"Acomodacao {name_accommodation} criada com sucesso.")
                                for _, client_addr in clients.items():
                                    if client_addr != end:
                                        self.send(client_addr, f"[{name}/{end} Adicionou uma nova acomodação!]")
                                        #talvez seja necessario enviar ACK para cada cliente
                    #BOOK
                    elif command.startswith("book"):
                        _, owner, name_accommodation, location, day, room = command.split(maxsplit=5)
                        if end not in clients.values(): #Verifica se o usuário está logado
                            self.send(end, b"Voce nao esta logado.")
                        else:
                            if(name_accommodation, location) not in accomodations:
                                self.send(end, b"Acomodacao nao encontrada.")
                            else:
                                accomodation = accomodations[(name_accommodation, location)]
                                if end == accomodation["owner"]:
                                    self.send(end, b"Voce nao pode reservar sua propria acomodacao.")
                                elif day not in accomodation["bookings"]:
                                    self.send(end, b"Data nao disponivel.")
                                else:
                                    accomodation["bookings"][day] = end
                                    self.send(end, f"Reserva realizada com sucesso.")
                                    self.send(accomodation["owner"], f"Reserva realizada por {name}/{end} na acomodacao {name_accommodation}.")
                    #CANCEL
                    elif command.startswith("cancel"):
                        _, owner, name, location, day = command.split(maxsplit=4)
                        if end not in clients.values(): #Verifica se o usuário está logado
                            self.send(end, b"Voce nao esta logado.")
                        else:
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
                    
                    self.send(addr, seq_num.to_bytes(1, 'big')) # Envia um ACK para o cliente.  
                    expected_seq_num = 1 if expected_seq_num == 0 else 0 # Alterna o número de sequência esperado entre 0 e 1.
                else:
                    self.send(end, ((expected_seq_num + 1) % 2).to_bytes(1, 'big')) # Envia um ACK para o cliente.       
            except skt.timeout:
                continue
            except:
                continue
                
            
def main():

    server = UDPServer(skt.AF_INET, skt.SOCK_DGRAM, addr_bind, MAX_BUFF_SIZE)
    print("Server started.")
    server.listen()     #O servidor começa a escutar.

main()
