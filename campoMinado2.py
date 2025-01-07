import random
import tkinter as tk

class CampoMinado:
    def __init__(self,root,tamanho,num_minas):
        self.tamanho = tamanho
        self.num_minas = num_minas
        self.tabuleiro = []
        self.revelado = []
        self.botoes = []
        self.minas = set()
        self.jogo_terminado = False
        self.root = root
        self.root.geometry("900x700")
        self.root.configure(bg="grey")
        self.root.title("Campo Minado")
        
        
        







def inicio_do_jogo():
    root = tk.Tk()
    tamanho = 9
    num_minas = 10
    CampoMinado(root,tamanho,num_minas)
    root.mainloop()

inicio_do_jogo()