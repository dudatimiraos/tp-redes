# tp-redes
Jogo Multijogador: Pedra, Papel e Tesoura com Socket e Multithreading

Este projeto implementa um jogo de "Pedra, Papel e Tesoura" multijogador em rede local, utilizando socket para comunicação entre clientes e servidor e multithreading para permitir a conexão simultânea de dois jogadores. A interface gráfica do cliente foi construída com Tkinter para uma interação amigável e intuitiva.

Funcionalidades:
    Dois jogadores podem se conectar ao servidor e jogar "Pedra, Papel e Tesoura" em tempo real.
    A comunicação é feita através do protocolo TCP, garantindo confiabilidade na troca de dados.
    Cada jogador possui uma interface gráfica simples e clara para escolher suas jogadas.
    O servidor determina o vencedor com base nas regras do jogo e envia o resultado para ambos os jogadores.
    Implementação de um sistema de inatividade que desconecta jogadores inativos.
    Pré-requisitos
    Python 3.x

Bibliotecas padrão:
    socket
    threading
    tkinter

Instruções de Uso
1. Clonar o Repositório
Clone este repositório na sua máquina local:
git clone https://github.com/usuario/jogo-pedra-papel-tesoura.git

2. Iniciar o Servidor
Execute o seguinte comando no terminal para iniciar o servidor:
python servidor.py

    O servidor ficará aguardando a conexão de dois jogadores.

3. Iniciar o Cliente
Cada jogador deve iniciar o cliente em uma nova janela executando:
python cliente.py
    1. O jogador deverá inserir o seu número (1 ou 2) e o apelido na interface.
    2. Após ambos os jogadores se conectarem, poderão escolher entre "Pedra", "Papel" ou "Tesoura".
    3. O resultado será exibido na interface gráfica.

4. Desconectar por Inatividade
Caso um jogador fique inativo por mais de 1 minuto e 30 segundos, será exibido um aviso. Se a inatividade continuar por 30 segundos adicionais (2 minutos no total), o jogador será desconectado automaticamente.

Estrutura do Projeto
    1. servidor.py: Contém a lógica do servidor, responsável por aceitar conexões, receber jogadas e determinar o vencedor.
    2. cliente.py: Implementa a interface gráfica do cliente e a lógica de comunicação com o servidor.
    3. README.md: Documentação para instalação e uso do projeto.

Exemplo de Execução:
    Servidor
        Servidor aguardando jogadores...
        Jogador 1 conectado.
        Jogador 2 conectado.
        Resultado: Jogador 1 venceu!

    Cliente
        Após executar o cliente, a interface será aberta, onde o jogador poderá inserir seu apelido e fazer as escolhas.