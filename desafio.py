#Inserção de bibliotecas
import socket
import threading
import Rpi.GPIO as gpio

host = '192.168.0.110' # Endereço IP do servidor
port =  # Porta que o servidor está

# Envio
def send(interface):
    while True:
        try:
            #mensagem: leitura do botão
            message = gpio.input(18)
            interface.sendall(message.encode("utf-8"))
        except socket.error:
            break
    print("Envio de mensagens encerrado!")

# Recebimento
def receive(interface):
    while True:
        message = interface.recv(1024)
        if not(len(message)):
            break
        # Se a mensagem recebida for que o botão foi pressionado o led acende
        elif message == 1:
            gpio.output(13, gpio.HIGH)
        # Se a mensagem recebida for que o botão não está pressionado o led permanece apagado
        elif message == 0:
            gpio.output(13, gpio.LOW)
        else:
            gpio.output(13, gpio.LOW)
        print("Conexão com o servidor encerrada!")

def main():
    # Configurações iniciais
    gpio.setmode(gpio.BOARD)
    gpio.setup(13, gpio.OUT)
    gpio.setput(18, gpio.IN)

    # Criar um socket TCP    
    interface = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Habilitar a reutilização do endereço/porta
    interface.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Conectando o socket no servidor
    server_adress = (host, port)
    interface.connect(server_adress)
    
    send_thread = threading.Thread(target = send, args = (interface,))
    receive_thread = threading.Thread(target = receive, args = (interface,))
