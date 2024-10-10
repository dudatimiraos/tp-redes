import socket
import threading
import time
import signal
import sys

jogadores = []
escolhas = {}
jogadores_conexoes = {}

# Função para determinar o vencedor
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

# Função para enviar aviso e desconectar após o timeout
def desconectar_apos_timeout(conexao, apelido):
    time.sleep(90)  # 1:30 minutos
    if apelido not in escolhas:
        conexao.send("Escolha uma ação ou será desconectado em 30 segundos.".encode())
    
    time.sleep(30)  # Mais 30 segundos (totalizando 2 minutos)
    if apelido not in escolhas:  # Se ainda não fez escolha
        conexao.send("Você foi desconectado por inatividade.".encode())
        conexao.close()
        jogadores.remove(apelido)
        for jogador, jogador_conexao in jogadores_conexoes.items():
            if jogador != apelido:
                jogador_conexao.send(f"{apelido} foi desconectado por inatividade.".encode())
        return True
    return False

# Função de comunicação com o cliente
def comunicacao_cliente(conexao, endereco, apelido):
    print(f"{apelido} conectado.")
    jogadores.append(apelido)

    # Envia mensagem de aguardando outro jogador se for o primeiro
    if len(jogadores) == 1:
        conexao.send("Aguardando jogador 2...\n".encode())

    # Espera até que o segundo jogador se conecte
    while len(jogadores) < 2:
        if not threading.main_thread().is_alive():
            return  # Se o thread principal estiver encerrando, saia da função
        pass

    # Agora que ambos estão conectados, libera as escolhas
    conexao.send("Ambos jogadores conectados! \nEscolha: Pedra, Papel ou Tesoura (ou 0 para sair): ".encode())

    # Inicia o temporizador de inatividade, garantindo que o programa ainda esteja ativo
    if threading.main_thread().is_alive():
        timer_thread = threading.Thread(target=desconectar_apos_timeout, args=(conexao, apelido))
        timer_thread.daemon = True  # Thread daemon para finalizar junto com o processo principal
        timer_thread.start()

    # Flag para controle de envio de mensagens de espera
    aguardando = False

    while True:
        try:
            if len(escolhas) < 2:
                if apelido not in escolhas:
                    escolha = conexao.recv(1024).decode()

                    # Jogador decide sair
                    if escolha == '0':
                        conexao.send("Você se desconectou.".encode())
                        conexao.close()
                        jogadores.remove(apelido)
                        for jogador, jogador_conexao in jogadores_conexoes.items():
                            if jogador != apelido:
                                jogador_conexao.send(f"{apelido} se desconectou.".encode())
                        return

                    # Registra a escolha do jogador
                    escolhas[apelido] = escolha
                    print(f"{apelido} escolheu {escolha}")

                    # Quando ambos os jogadores fizerem uma escolha
                    if len(escolhas) == 2:
                        resultado = determinar_vencedor()
                        for jogador, jogador_conexao in jogadores_conexoes.items():
                            jogador_conexao.send(f"Resultado: {resultado}\n".encode())
                            jogador_conexao.send("Novo jogo! Escolha: Pedra, Papel ou Tesoura (ou 0 para sair): ".encode())
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

# Função para iniciar o servidor
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

# Função para encerrar o servidor corretamente
def encerrar_servidor(signal, frame):
    print("Encerrando o servidor...")
    for conexao in jogadores_conexoes.values():
        conexao.close()  # Fecha todas as conexões ativas
    sys.exit(0)

# Captura o sinal de interrupção (Ctrl + C) para encerrar o servidor
signal.signal(signal.SIGINT, encerrar_servidor)

iniciar_servidor()
