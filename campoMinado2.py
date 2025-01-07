import random
import tkinter as tk

class CampoMinado:
    def __init__(self, root):
        self.root = root
        self.root.geometry("800x600")
        self.root.configure(bg="red")
        self.root.title("Campo Minado")
        







campo_minado = CampoMinado(tk.Tk())
campo_minado.root.mainloop()