import socket
import threading

def ouvir_servidor(cliente_socket):
    while True:
        try:
            # Recebe e exibe as mensagens do servidor
            mensagem = cliente_socket.recv(1024).decode()
            print(mensagem)
        except:
            print("Conexão perdida com o servidor.")
            cliente_socket.close()
            break

def iniciar_cliente():
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect(('localhost', 2002))

    # Envia o apelido do jogador e espera uma confirmação antes de continuar
    apelido = input("Digite o seu apelido: ")
    cliente.send(apelido.encode())

    # Thread para ouvir as mensagens do servidor
    thread_ouvir = threading.Thread(target=ouvir_servidor, args=(cliente,))
    thread_ouvir.daemon = True
    thread_ouvir.start()

    # Enviar escolhas do jogador
    while True:
        escolha = input()  # Aqui, o jogador faz suas escolhas após mensagens do servidor
        cliente.send(escolha.encode())
        if escolha == '0':
            break

iniciar_cliente()
