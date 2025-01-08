import tkinter as tk
from tkinter import messagebox
import random
import time

class CampoMinado:
    def __init__(self, linhas=9, colunas=9, bombas=10):
        self.linhas = linhas
        self.colunas = colunas
        self.bombas = bombas
        self.bandeiras_restantes = bombas
        self.tabuleiro = []
        self.botoes = []
        self.janela = None
        self.tempo_inicial = None
        self.label_tempo = None
        self.label_bandeiras = None
        self.jogo_iniciado = False
        self.criar_tabuleiro()

    def criar_tabuleiro(self):
        self.tabuleiro = [[0 for _ in range(self.colunas)] for _ in range(self.linhas)]
        bombas_posicionadas = 0
        while bombas_posicionadas < self.bombas:
            linha = random.randint(0, self.linhas - 1)
            coluna = random.randint(0, self.colunas - 1)
            if self.tabuleiro[linha][coluna] != -1:
                self.tabuleiro[linha][coluna] = -1
                bombas_posicionadas += 1
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        nova_linha = linha + i
                        nova_coluna = coluna + j
                        if 0 <= nova_linha < self.linhas and 0 <= nova_coluna < self.colunas and self.tabuleiro[nova_linha][nova_coluna] != -1:
                            self.tabuleiro[nova_linha][nova_coluna] += 1

    def atualizar_tempo(self):
        if self.tempo_inicial and self.jogo_iniciado:
            tempo_atual = int(time.time() - self.tempo_inicial)
            self.label_tempo.config(text=f"Tempo: {tempo_atual}s")
            self.janela.after(1000, self.atualizar_tempo)

    def iniciar_interface(self):
        self.janela = tk.Tk()
        self.janela.title("Campo Minado")
        

        # Configura o estilo da janela
        self.janela.configure(bg='#f0f0f0')
        
        # Frame principal centralizado
        frame_principal = tk.Frame(self.janela, bg='#f0f0f0')
        frame_principal.pack(expand=True, padx=20, pady=20)

        # Frame para informações do jogo
        frame_info = tk.Frame(frame_principal, bg='#f0f0f0')
        frame_info.pack(fill='x', pady=(0, 10))

        self.label_bandeiras = tk.Label(frame_info, text=f"Bandeiras: {self.bandeiras_restantes}", 
                                      bg='#f0f0f0', font=('Arial', 10))
        self.label_bandeiras.pack(side=tk.LEFT, padx=10)

        self.label_tempo = tk.Label(frame_info, text="Tempo: 0s", 
                                  bg='#f0f0f0', font=('Arial', 10))
        self.label_tempo.pack(side=tk.LEFT, padx=10)

        btn_reiniciar = tk.Button(frame_info, text="Reiniciar", 
                                command=self.reiniciar_jogo,
                                relief=tk.RAISED,
                                bg='#e0e0e0',
                                font=('Arial', 10))
        btn_reiniciar.pack(side=tk.LEFT, padx=10)

        # Frame para o tabuleiro
        frame_tabuleiro = tk.Frame(frame_principal, bg='#f0f0f0')
        frame_tabuleiro.pack(padx=10, pady=10)

        for linha in range(self.linhas):
            for coluna in range(self.colunas):
                botao = tk.Button(
                    frame_tabuleiro,
                    text="",
                    width=2,
                    height=1,
                    font=('Arial', 10, 'bold'),
                    relief=tk.RAISED,
                    bg='#e0e0e0'
                )
                botao.grid(row=linha, column=coluna, padx=1, pady=1)
                botao.bind('<Button-1>', lambda e, l=linha, c=coluna: self.revelar_celula(l, c))
                botao.bind('<Button-3>', lambda e, l=linha, c=coluna: self.marcar_bandeira(l, c))
                if not self.botoes:
                    self.botoes.append([])
                if len(self.botoes) <= linha:
                    self.botoes.append([])
                self.botoes[linha].append(botao)

        # Centraliza a janela na tela
        self.janela.eval('tk::PlaceWindow . center')
        
        self.janela.mainloop()

    def marcar_bandeira(self, linha, coluna):
        if not self.jogo_iniciado:
            self.jogo_iniciado = True
            self.tempo_inicial = time.time()
            self.atualizar_tempo()
        
        botao = self.botoes[linha][coluna]
        if botao["state"] == "normal":
            if botao["text"] == "":
                if self.bandeiras_restantes > 0:
                    botao.config(text="🚩", fg="red")
                    self.bandeiras_restantes -= 1
            elif botao["text"] == "🚩":
                botao.config(text="")
                self.bandeiras_restantes += 1
            self.label_bandeiras.config(text=f"Bandeiras: {self.bandeiras_restantes}")
            self.verificar_vitoria()

    def revelar_celula(self, linha, coluna):
        if not self.jogo_iniciado:
            self.jogo_iniciado = True
            self.tempo_inicial = time.time()
            self.atualizar_tempo()

        botao = self.botoes[linha][coluna]
        if botao["text"] == "🚩" or botao["state"] == "disabled":
            return

        valor = self.tabuleiro[linha][coluna]
        cores = {1: 'blue', 2: 'green', 3: 'red', 4: 'purple', 
                5: 'maroon', 6: 'turquoise', 7: 'black', 8: 'gray'}

        if valor == -1:
            botao.config(text="💣", bg="red")
            self.fim_de_jogo("Você perdeu! 💥")
        else:
            if valor > 0:
                botao.config(text=str(valor), 
                           state="disabled", 
                           relief=tk.SUNKEN,
                           fg=cores.get(valor, 'black'))
            else:
                botao.config(text="", state="disabled", relief=tk.SUNKEN)
                self.expandir_vazios(linha, coluna)
            
            self.verificar_vitoria()

    def expandir_vazios(self, linha, coluna):
        for i in range(-1, 2):
            for j in range(-1, 2):
                nova_linha = linha + i
                nova_coluna = coluna + j
                if 0 <= nova_linha < self.linhas and 0 <= nova_coluna < self.colunas:
                    botao = self.botoes[nova_linha][nova_coluna]
                    if botao["state"] == "normal" and botao["text"] != "🚩":
                        self.revelar_celula(nova_linha, nova_coluna)

    def verificar_vitoria(self):
        for linha in range(self.linhas):
            for coluna in range(self.colunas):
                botao = self.botoes[linha][coluna]
                if self.tabuleiro[linha][coluna] != -1 and botao["state"] == "normal":
                    return False
        self.fim_de_jogo("Parabéns! Você venceu! ")
        return True

    def fim_de_jogo(self, mensagem):
        self.jogo_iniciado = False
        for linha in range(self.linhas):
            for coluna in range(self.colunas):
                botao = self.botoes[linha][coluna]
                valor = self.tabuleiro[linha][coluna]
                if valor == -1:
                    if botao["text"] != "🚩":
                        botao.config(text="💣", bg="red")
                elif botao["text"] == "🚩" and valor != -1:
                    botao.config(text="❌", bg="orange")
        messagebox.showinfo("Fim de Jogo", mensagem)

    def reiniciar_jogo(self):
        self.janela.destroy()
        self.__init__(self.linhas, self.colunas, self.bombas)
        self.iniciar_interface()

if __name__ == "__main__":
    jogo = CampoMinado(linhas=9, colunas=9, bombas=10)
    jogo.iniciar_interface()
