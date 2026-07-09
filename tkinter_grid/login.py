import tkinter as tk
from tkinter import Tk
from tkinter import messagebox



janela = tk.Tk()
janela.title("SISTEMA DE LOGIN")
janela.geometry("400x300")
#Janela principal
def login():
    usuario = edt_login.get()
    senha = edt_senha.get()

    if usuario == "admin" and senha == "1234":
        messagebox.showinfo("Login", "Login bem-sucedido!") 
        nova_janela = tk.Toplevel()
        nova_janela.title("MENU PRINCIPAL")
        nova_janela.geometry("400x300")

        lbl_boas_vindas = tk.Label(nova_janela, text=f"Bem-vindo, {usuario}!", font=("Arial", 16))
        lbl_boas_vindas.pack(pady=30)
    else:
        messagebox.showerror("Login", "Usuário ou senha incorretos!")



# LOGIN
lbl_login = tk.Label(janela, text="Login:")

lbl_login.grid(row=0, column=0, padx=10, pady=10)

# Campo de entrada de texto login
edt_login = tk.Entry(janela, width=35)

edt_login.grid(row=0, column=1, padx=10, pady=10)

# SENHA

lbl_senha = tk.Label(janela, text="Senha:")
lbl_senha.grid(row=1, column=0, padx=10, pady=10)

# Campo de entrada de texto senha
edt_senha = tk.Entry(janela, width=35, show="*")
edt_senha.grid(row=1, column=1, padx=10, pady=10)


#BOTAO DE LOGIN

btn_login = tk.Button(janela, text="ENTRAR", command=login)
btn_login.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
janela.mainloop()






