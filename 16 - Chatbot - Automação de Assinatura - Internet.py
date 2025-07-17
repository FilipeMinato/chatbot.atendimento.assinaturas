import tkinter as tk
from tkinter import messagebox

# Dados dos pacotes
pacotes = {
    "1": ("5Mb", 59.90),
    "2": ("10Mb", 79.90),
    "3": ("20Mb", 99.90)
}

prazos = {
    "1": ("Mensal", 1, 0.0),
    "2": ("Semestral", 6, 0.05),
    "3": ("Anual", 12, 0.15)
}


class PlanoInternetApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Planos de Internet")
        self.root.geometry("500x500")
        self.resetar()
        self.tela_inicio()

    def resetar(self):
        self.pacote = None
        self.valor_base = 0
        self.prazo_nome = ""
        self.meses = 0
        self.desconto_prazo = 0
        self.valor_com_desconto = 0
        self.forma_pag = ""
        self.desconto_pag = 0
        self.parcelas = 1
        self.valor_final = 0

    def limpar_tela(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def tela_inicio(self):
        self.limpar_tela()
        tk.Label(self.root, text="📡 Bem-vindo à nossa Provedora de Internet!", font=("Helvetica", 15)).pack(pady=15)
        tk.Label(self.root, text="Escolha um dos pacotes abaixo:", font=("Helvetica", 13)).pack(pady=10)

        for k, (nome, valor) in pacotes.items():
            tk.Button(self.root, text=f"{k} - {nome} por R${valor:.2f}", width=35,
                      command=lambda k=k: self.selecionar_pacote(k)).pack(pady=5)

    def selecionar_pacote(self, escolha):
        self.pacote, self.valor_base = pacotes[escolha]
        self.tela_prazo()

    def tela_prazo(self):
        # ========================
        # Etapa de seleção do prazo
        # ========================
        self.limpar_tela()  # Limpa a tela anterior antes de mostrar novas opções

        # Mostra qual pacote foi selecionado anteriormente
        tk.Label(self.root, text=f"Você escolheu o pacote {self.pacote}.", font=("Helvetica", 13)).pack(pady=10)

        # Solicita ao usuário o prazo de contratação
        tk.Label(self.root, text="Escolha o prazo de contratação:", font=("Helvetica", 13)).pack(pady=10)

        # Exibe botões com as opções de prazos definidos no dicionário `prazos`
        # Cada botão mostra o nome do plano, número de meses e o desconto aplicado
        for k, (nome, meses, desconto) in prazos.items():
            valor_desc = self.valor_base * meses * (1 - desconto)  # Valor com desconto já aplicado
            descricao_desc = "sem desconto" if desconto == 0 else f"com {int(desconto * 100)}% de desconto"
            tk.Button(
                self.root,
                text=f"{k} - {nome} - R${valor_desc:.2f} ({meses}x, {descricao_desc})",
                command=lambda k=k: self.definir_prazo(k)
            ).pack(pady=4)

        # ========================
        # Função que registra o prazo escolhido
        # ========================
        def definir_prazo(self, escolha):
            """
            Armazena o nome do prazo, meses e desconto associados à escolha do usuário.
            Em seguida, avança para a etapa de pagamento.
            """
            self.prazo_nome, self.meses, self.desconto_prazo = prazos[escolha]
            self.valor_com_desconto = self.valor_base * self.meses * (1 - self.desconto_prazo)
            self.tela_pagamento()

        # ========================
        # Tela de escolha da forma de pagamento
        # ========================
        def tela_pagamento(self):
            """
            Apresenta ao usuário duas formas de pagamento:
            - PIX (com desconto adicional)
            - Cartão de crédito (parcelamento)
            """
            self.limpar_tela()

            tk.Label(self.root, text="Escolha a forma de pagamento:", font=("Helvetica", 13)).pack(pady=10)

            valor_pix = self.valor_com_desconto * 0.9  # Aplica 10% de desconto no valor total
            tk.Button(
                self.root,
                text=f"1 - PIX (10% de desconto adicional): R${valor_pix:.2f} à vista",
                command=self.pagamento_pix
            ).pack(pady=5)

            tk.Button(
                self.root,
                text=f"2 - Cartão de crédito (até {self.meses}x sem juros)",
                command=self.pagamento_cartao
            ).pack(pady=5)

        # ========================
        # Lógica do pagamento via PIX
        # ========================
        def pagamento_pix(self):
            """
            Registra o método de pagamento como PIX.
            Aplica o desconto e define como pagamento à vista (1 parcela).
            """
            self.forma_pag = "PIX"
            self.desconto_pag = 0.10
            self.parcelas = 1
            self.valor_final = self.valor_com_desconto * (1 - self.desconto_pag)
            self.resumo()

        # ========================
        # Lógica do pagamento via Cartão de Crédito
        # ========================
        def pagamento_cartao(self):
            """
            Registra o pagamento como Cartão.
            Pergunta em quantas parcelas o usuário deseja dividir.
            """
            self.forma_pag = "Cartão de Crédito"
            self.desconto_pag = 0.0
            self.valor_final = self.valor_com_desconto

            def confirmar_parcelas():
                """
                Confirma o número de parcelas escolhido pelo usuário e prossegue para o resumo.
                """
                try:
                    p = int(entry.get())
                    if 1 <= p <= self.meses:
                        self.parcelas = p
                        popup.destroy()
                        self.resumo()
                    else:
                        messagebox.showerror("Erro", f"Digite um número entre 1 e {self.meses}.")
                except:
                    messagebox.showerror("Erro", "Digite um número válido.")

            # Janela pop-up para digitar a quantidade de parcelas desejada
            popup = tk.Toplevel(self.root)
            popup.title("Parcelamento")
            popup.geometry("300x150")
            tk.Label(popup, text=f"Quantas parcelas deseja? (1 a {self.meses})").pack(pady=10)
            entry = tk.Entry(popup)
            entry.pack()
            tk.Button(popup, text="Confirmar", command=confirmar_parcelas).pack(pady=10)

        # ========================
        # Tela de Resumo Final da Simulação
        # ========================
        def resumo(self):
            """
            Mostra todas as escolhas feitas: pacote, prazo, forma de pagamento e valores.
            Permite confirmar ou refazer a simulação.
            """
            self.limpar_tela()
            valor_parcela = self.valor_final / self.parcelas

            tk.Label(self.root, text="📄 Resumo da Simulação", font=("Helvetica", 15)).pack(pady=10)

            tk.Label(self.root, text=f"- Pacote: {self.pacote}").pack()
            tk.Label(self.root, text=f"- Prazo: {self.prazo_nome} ({self.meses} mês(es))").pack()
            tk.Label(self.root, text=f"- Valor mensal base: R${self.valor_base:.2f}").pack()
            tk.Label(self.root,
                     text=f"- Valor com desconto de prazo: R${self.valor_com_desconto:.2f} ({int(self.desconto_prazo * 100)}% de desconto)").pack()
            tk.Label(self.root, text=f"- Forma de pagamento: {self.forma_pag}").pack()

            if self.forma_pag == "PIX":
                tk.Label(self.root, text=f"- Desconto de pagamento: 10%").pack()

            tk.Label(self.root, text=f"- Valor total a pagar: R${self.valor_final:.2f}").pack()

            if self.parcelas > 1:
                tk.Label(self.root, text=f"- Parcelado em {self.parcelas}x de R${valor_parcela:.2f}").pack()

            # Botões finais
            tk.Label(self.root, text="\nDeseja confirmar a assinatura?").pack(pady=10)
            tk.Button(self.root, text="✅ Confirmar", command=self.confirmar).pack(pady=5)
            tk.Button(self.root, text="🔄 Refazer simulação", command=self.recomecar).pack(pady=5)

        # ========================
        # Confirmação da assinatura
        # ========================
        def confirmar(self):
            """
            Finaliza o processo e mostra mensagem de agradecimento.
            Fecha a janela do aplicativo.
            """
            messagebox.showinfo("Assinatura Confirmada",
                                "Obrigado pela sua assinatura! Em breve entraremos em contato para instalação. 😊")
            self.root.destroy()

        # ========================
        # Reiniciar o processo
        # ========================
        def recomecar(self):
            """
            Reinicia todas as variáveis e volta para a tela inicial.
            """
            self.resetar()
            self.tela_inicio()
