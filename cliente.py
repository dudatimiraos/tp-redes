import socket  # Importa o módulo socket para comunicação em rede

def iniciar_cliente():
    # Cria um socket TCP (AF_INET para IPv4 e SOCK_STREAM para TCP)
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Conecta o cliente ao servidor local ('localhost') na porta 2002
    cliente.connect(('localhost', 2002))  # Conectando ao servidor

    apelido = input("Digite o seu apelido: ")  # Solicita o apelido do jogador

    # Envia o nome do jogador para o servidor, codificando a string para bytes
    cliente.send(apelido.encode())

    # Loop contínuo para manter a comunicação com o servidor
    while True:
        # Recebe uma mensagem do servidor, com um buffer de 1024 bytes
        mensagem = cliente.recv(1024).decode()  # Recebe uma mensagem do servidor e decodifica para string
        print(mensagem)  # Exibe a mensagem recebida

        # Verifica se a mensagem recebida contém a palavra "Escolha"
        if "Escolha" in mensagem:
            escolha = input()  # O jogador escolhe Pedra, Papel ou Tesoura

            # Envia a escolha ao servidor, codificando-a para bytes
            cliente.send(escolha.encode())

# Inicia o cliente
iniciar_cliente()
