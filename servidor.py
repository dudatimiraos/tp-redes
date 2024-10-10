import socket
import threading

jogadores = []
escolhas = {}
jogadores_conexoes = {}

def determinar_vencedor():
    jogador1, jogador2 = list(escolhas.keys())
    escolha1, escolha2 = escolhas[jogador1].capitalize(), escolhas[jogador2].capitalize()

    if escolha1 == escolha2:
        return "Empate!"
    elif (escolha1 == "Pedra" and escolha2 == "Tesoura") or \
         (escolha1 == "Tesoura" and escolha2 == "Papel") or \
         (escolha1 == "Papel" and escolha2 == "Pedra"):
        return f"{jogador1} venceu!"
    else:
        return f"{jogador2} venceu!"

def comunicacao_cliente(conexao, endereco, apelido):
    print(f"{apelido} conectado.")
    jogadores.append(apelido)

    # Envia a mensagem de aguardando outro jogador, se for o primeiro
    if len(jogadores) == 1:
        conexao.send("Aguardando jogador 2...\n".encode())

    # Espera até que o segundo jogador se conecte
    while len(jogadores) < 2:
        pass  # Aguarda até que o segundo jogador entre

    # Agora que ambos estão conectados, libera as escolhas
    conexao.send("Ambos jogadores conectados! \nEscolha: Pedra, Papel ou Tesoura (ou 0 para sair): ".encode())

    # Flag para controle do envio de mensagens de espera
    aguardando = False

    while True:
        try:
            if len(escolhas) < 2:
                if apelido not in escolhas:
                    escolha = conexao.recv(1024).decode()

                    if escolha == '0':
                        conexao.send("Você se desconectou.".encode())
                        conexao.close()
                        jogadores.remove(apelido)
                        for jogador, jogador_conexao in jogadores_conexoes.items():
                            if jogador != apelido:
                                jogador_conexao.send(f"{apelido} se desconectou.".encode())
                        return

                    escolhas[apelido] = escolha
                    print(f"{apelido} escolheu {escolha}")

                    if len(escolhas) == 2:
                        resultado = determinar_vencedor()
                        for jogador, jogador_conexao in jogadores_conexoes.items():
                            jogador_conexao.send(f"Resultado: {resultado}\n".encode())
                            jogador_conexao.send("Novo jogo!".encode())
                            jogador_conexao.send("Escolha: Pedra, Papel ou Tesoura (ou 0 para sair): ".encode())
                        print(f"Resultado: {resultado}")
                        escolhas.clear()
                elif not aguardando:
                    conexao.send("Aguardando o outro jogador...\n".encode())
                    aguardando = True
            else:
                aguardando = False
        except:
            conexao.close()
            jogadores.remove(apelido)
            for jogador, jogador_conexao in jogadores_conexoes.items():
                if jogador != apelido:
                    jogador_conexao.send(f"{apelido} se desconectou.".encode())
            break

def iniciar_servidor():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind(('localhost', 2002))
    servidor.listen(2)
    print("Servidor aguardando jogadores...")

    while len(jogadores) < 2:
        conexao, endereco = servidor.accept()
        apelido = conexao.recv(1024).decode()
        jogadores_conexoes[apelido] = conexao
        thread = threading.Thread(target=comunicacao_cliente, args=(conexao, endereco, apelido))
        thread.start()

iniciar_servidor()
