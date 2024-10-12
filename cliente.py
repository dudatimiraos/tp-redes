import socket
import tkinter as tk
from tkinter import messagebox
import threading

class Jogo:
    def __init__(self, master, numero_jogador):
        self.master = master
        self.numero_jogador = numero_jogador
        self.master.title(f"Jogador {numero_jogador}: Pedra, Papel e Tesoura")
        self.master.geometry("400x400")
        self.master.configure(bg="#f0f8ff")  # Cor de fundo suave

        # Estilo delicado
        self.font_title = ("Helvetica", 14, "bold")
        self.font_normal = ("Helvetica", 12)
        self.bg_color = "#f0f8ff"
        self.btn_color = "#FB37A3"
        self.text_color = "#2F4F4F"

        # Entrada para o apelido
        self.apelido_label = tk.Label(master, text=f"Apelido do Jogador {numero_jogador}:", 
                                      font=self.font_normal, bg=self.bg_color, fg=self.text_color)
        self.apelido_label.pack(pady=10)
        self.apelido_entry = tk.Entry(master, font=self.font_normal)
        self.apelido_entry.pack(pady=5)

        # Botão para enviar o apelido
        self.enviar_button = tk.Button(master, text="Enviar Apelido", font=self.font_normal,
                                       bg=self.btn_color, fg="white", command=self.enviar_apelido)
        self.enviar_button.pack(pady=10)

        # Labels para as escolhas e resultados
        self.resultado_label = tk.Label(master, text="", font=self.font_normal, bg=self.bg_color, fg=self.text_color)
        self.resultado_label.pack(pady=10)

        # Conectar ao servidor
        self.cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cliente.connect(('localhost', 2002))

        # Armazenar a escolha do jogador
        self.escolha = None

        # Thread para ouvir o servidor
        thread_ouvir = threading.Thread(target=self.ouvir_servidor)
        thread_ouvir.daemon = True
        thread_ouvir.start()

        # Variáveis para o timer
        self.timer_warning = None
        self.timer_disconnect = None

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

        # Iniciar o timer de inatividade
        self.iniciar_timer()

    def exibir_opcoes(self):
        # Botões para as escolhas com um layout mais espaçado
        self.pedra_button = tk.Button(self.master, text="Pedra", font=self.font_normal,
                                      bg=self.btn_color, fg="white", width=12, command=lambda: self.fazer_escolha("Pedra"))
        self.pedra_button.pack(pady=5)

        self.papel_button = tk.Button(self.master, text="Papel", font=self.font_normal,
                                      bg=self.btn_color, fg="white", width=12, command=lambda: self.fazer_escolha("Papel"))
        self.papel_button.pack(pady=5)

        self.tesoura_button = tk.Button(self.master, text="Tesoura", font=self.font_normal,
                                        bg=self.btn_color, fg="white", width=12, command=lambda: self.fazer_escolha("Tesoura"))
        self.tesoura_button.pack(pady=5)

    def fazer_escolha(self, escolha):
        self.escolha = escolha
        self.cliente.send(escolha.encode())
        self.desabilitar_botoes()

        # Reiniciar o timer após uma escolha
        self.reiniciar_timer()

    def desabilitar_botoes(self):
        # Desabilitar os botões após a escolha
        self.pedra_button.config(state=tk.DISABLED)
        self.papel_button.config(state=tk.DISABLED)
        self.tesoura_button.config(state=tk.DISABLED)

    def habilitar_botoes(self):
        # Habilitar os botões para um novo jogo
        self.pedra_button.config(state=tk.NORMAL)
        self.papel_button.config(state=tk.NORMAL)
        self.tesoura_button.config(state=tk.NORMAL)

        # Reiniciar o timer para uma nova rodada
        self.reiniciar_timer()

    def ouvir_servidor(self):
        while True:
            try:
                mensagem = self.cliente.recv(1024).decode()
                if "Resultado" in mensagem:
                    self.resultado_label.config(text=mensagem)
                    # Habilitar botões para o próximo jogo
                    self.habilitar_botoes()
            except:
                print("Erro ao se comunicar com o servidor.")
                break

    def iniciar_timer(self):
        # Inicia o timer de aviso e desconexão
        self.timer_warning = self.master.after(90000, self.exibir_aviso)  # 1:30 minutos
        self.timer_disconnect = self.master.after(120000, self.desconectar_jogador)  # 2 minutos

    def reiniciar_timer(self):
        # Cancela os timers e os reinicia
        if self.timer_warning:
            self.master.after_cancel(self.timer_warning)
        if self.timer_disconnect:
            self.master.after_cancel(self.timer_disconnect)
        self.iniciar_timer()

    def exibir_aviso(self):
        messagebox.showwarning("Aviso", "Escolha uma ação ou será desconectado em 30 segundos!")

    def desconectar_jogador(self):
        messagebox.showinfo("Desconectado", "Você foi desconectado por inatividade.")
        self.master.quit()  # Fecha a interface
        self.cliente.close()  # Fecha a conexão


# Inicialize a interface para o Jogador quando você decidir
if __name__ == "__main__":
    root = tk.Tk()
    numero_jogador = input("Digite o número do jogador (1 ou 2): ")  # Permite abrir a interface para o jogador correto
    jogo = Jogo(root, numero_jogador)
    root.mainloop()
