import tkinter as tk
from ctypes.wintypes import SIZE
from tkinter import ttk, messagebox, Tk

from fpdf import FPDF

def gerar_pdf():
    cliente = entrada_cliente.get()
    servico = combo_servico.get()
    valor = entrada_valor.get()

    if not cliente or not servico or not valor:
        messagebox.showwarning("Atenção", "Preencha todos os campos")
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('arial',size=12)
        #                       //alinhamento de centro = align='C'
        pdf.cell(200,10,txt="ORDEM DE SERVIÇO", ln=1, align='C')
        pdf.ln(10)

        pdf.cell(200, 10, txt=f"Cliente: {cliente}", ln=1)
        pdf.cell(200, 10, txt=f"Serviço: {servico}",ln=1)
        pdf.cell(200,10,txt=f"Valor: {valor}", ln=1)

        pdf.output("ordem_servico.pdf")

        # Exibe mensagem de sucesso para o usuario

        messagebox.showinfo("Sucesso", "PDF gerado com sucesso!")
    except Exception as e:
        # Se ocorrer qualquer erro, exibe mensagem de erro
        messagebox.showerror("Erro", f"Erro ao gravar PDF: {e}")

#   Criação da interface grafica (Tkinter)

janela = tk.Tk()
janela.title("Gerador de Ordem de Serviço Tabajara")
janela.geometry("350x220")

(tk.Label(janela, text= "Cliente:").grid(
    row=0,
    column=0,
    sticky="w",
    pady=5,
    padx=5
))

entrada_cliente = Tk.Entry(janela, width=35)
entrada_cliente.grid(row=0,
                     column=1,
                     padx=10,
                     pady=5)

# Campo: SERVIÇO

(tk.Label(janela, text= "Serviço:")
 .grid(row=1,
       column=0,
       sticky="w",
       pady=5,
       padx=5
))

entrada_cliente = tk.Entry(janela, width=35)
entrada_cliente.grid(row=1, column=1, padx=5, pady=5)


servicos = [
    "Formatação de Computador",
    "Instalação do Windows",
    "Criação de Site",
    "Suporte Tecnico"
]

combo_servico = ttk.Combobox(janela,values = servicos, width=26, state="readonly")
combo_servico.grid(row=1, column=1, padx=10, pady=5)

janela.mainloop()