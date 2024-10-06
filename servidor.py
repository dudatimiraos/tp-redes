import socket #socket para criar a comunicação em rede
import threading #para o servidor gerenciar múltiplos clientes simultaneamente

jogadores = [] #armazenar os apelidos dos jogadores
escolhas = {}  #armazenar as escolhas dos jogares

#Compara as escolhas dos jogadores e determina o vencedor
def determinar_vencedor():
    #extrai o apelido dos 2 jogadores
    jogador1, jogador2 = list(escolhas.keys())
    #obtém a escolha de cada jogador
    escolha1, escolha2 = escolhas[jogador1].capitalize(), escolhas[jogador2].capitalize()

    if escolha1 == escolha2:
        return "Empate!"

    elif (escolha1 == "Pedra" and escolha2 == "Tesoura") or \
        ( escolha1 == "Tesoura" and escolha2 == "Papel") or \
        ( escolha1 == "Papel" and escolha2 == "Pedra"):
        return f"{jogador1} venceu!"

    else:
        return f"{jogador2} venceu!"

#lida com a comunicação de cada cliente
def comunicacao_cliente(conexao, endereco, apelido):
    #Exibe no servidor que o jogador está conectado
    print(f"{apelido} conectado.")
    #adiciona o apelido do jogador a lista de jogadores conectados
    jogadores.append(apelido)

    #envia uma mensagem ao cliente para fazer sua escolha
    conexao.send("Escolha: Pedra, Papel ou Tesoura: ".encode())
    
    #Recebe a escolha do jogador a partir do cliente (em formato de string)
    escolha = conexao.recv(1024).decode()

    #armazena a escolha do jogador no dicionário 'escolhas' usando o apelido como chave
    escolhas[apelido] =escolha
    #Exibe no servidor qual foi a escolha do jogador
    print(f"{apelido} escolheu {escolha}")

    #Verifica se ambos os jogadores já fizeram suas escolhas
    if len(escolhas) == 2:
        #determina o vencedor comparando as escolhas dos jogadores
        resultado = determinar_vencedor()
        #envia o resultado da partida para todos os jogadores conectados
        for jogador_conexao in jogadores_conexoes.values():
            jogador_conexao.send(resultado.encode())
        
        #Limpa o dicionario de escolhas para permitir uma nova partida
        escolhas.clear()

#função principal do servidor que inicia e gerencia as conexões
def iniciar_servidor():
    #Cria o socket TCP para o servidor (AF_INET para ipv4 e SOCK_STREAM para TPC)
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #Define o endereço IP e a porta do servidor (localhost e porta 2002)
    servidor.bind(('localhost', 2002)) #Porta para o servidor 
    #Coloca o servidor em modo de escuta, permitindo até 2 conexões de clientes
    servidor.listen(2)
    print("Servidor aguardando jogadores...")

    #Loop que aguarda até que dois jogadores estejam conectados
    while len(jogadores) < 2:
        #Aceita uma nova conexão de um cliente
        conexao, endereco = servidor.accept()
        # Envia ao cliente uma mensagem pedindo o apelido
        conexao.send("Digite seu apelido: ".encode())
        # Recebe o apelido do jogador a partir do cliente
        apelido = conexao.recv(1024).decode()
        #Armazena a conexão associada ao apelido do jogador no dicionario 'jogadores_conexoes'
        jogadores_conexoes[apelido] = conexao
        #Cria uma nova thread para lidar com a comunicação deste cliente (para não bloquear o servidor)
        thread = threading.Thread(target=comunicacao_cliente, args=(conexao,endereco,apelido))
        #Inicia a execução da thread
        thread.start()

#Dicionário que armazena as conexões dos jogadores usando o apelido como chave
jogadores_conexoes = {}

#Inicia o servidor 
iniciar_servidor()








































