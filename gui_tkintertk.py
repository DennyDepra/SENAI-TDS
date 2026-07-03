import tkinter as tk

from tkinter import Tk

janela = tk.Tk()
janela.title("meu app")
janela.geometry("400x300")

#loop eventos
label = tk.Label(janela, text="Olá, mundo!", font=("Arial", 20))
label.pack(pady=20, padx=20)

texto = tk.Text(janela,width=20)
texto.pack(pady=20)

janela.mainloop()
