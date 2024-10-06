import socket
import tkinter as tk
from tkinter import messagebox


class Jogo:
    def __init__(self, master, numero_jogador):
        self.master = master
        self.numero_jogador = numero_jogador
        self.master.title(f"Jogador {numero_jogador}: Pedra, Papel e Tesoura")

        # Entrada para o apelido
        self.apelido_label = tk.Label(master, text=f"Apelido do Jogador {numero_jogador}:")
        self.apelido_label.pack()
        self.apelido_entry = tk.Entry(master)
        self.apelido_entry.pack()

        # Botão para enviar o apelido
        self.enviar_button = tk.Button(master, text="Enviar Apelido", command=self.enviar_apelido)
        self.enviar_button.pack()

        # Labels para as escolhas e resultados
        self.resultado_label = tk.Label(master, text="")
        self.resultado_label.pack()

        # Conectar ao servidor
        self.cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cliente.connect(('localhost', 2002))

        # Armazenar a escolha do jogador
        self.escolha = None

    def enviar_apelido(self):
        # Enviar apelido para o servidor
        apelido = self.apelido_entry.get()
        self.cliente.send(apelido.encode())

        # Habilitar botões de escolha após o apelido ser enviado
        self.apelido_label.config(state=tk.DISABLED)
        self.apelido_entry.config(state=tk.DISABLED)
        self.enviar_button.config(state=tk.DISABLED)

        # Exibir opções de escolha
        self.exibir_opcoes()

    def exibir_opcoes(self):
        # Botões para as escolhas
        self.pedra_button = tk.Button(self.master, text="Pedra", command=lambda: self.fazer_escolha("Pedra"))
        self.pedra_button.pack()

        self.papel_button = tk.Button(self.master, text="Papel", command=lambda: self.fazer_escolha("Papel"))
        self.papel_button.pack()

        self.tesoura_button = tk.Button(self.master, text="Tesoura", command=lambda: self.fazer_escolha("Tesoura"))
        self.tesoura_button.pack()

    def fazer_escolha(self, escolha):
        self.escolha = escolha
        self.cliente.send(escolha.encode())

        # Receber o resultado da partida
        resultado = self.cliente.recv(1024).decode()
        self.resultado_label.config(text=resultado)


# Inicializar a interface para o Jogador 1
root1 = tk.Tk()
jogo1 = Jogo(root1, 1)
root1.mainloop()

# Inicializar a interface para o Jogador 2
root2 = tk.Tk()
jogo2 = Jogo(root2, 2)
root2.mainloop()
