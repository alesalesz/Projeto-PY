import customtkinter as ctk

from calculadora import CalculadoraFrame
from email_auto import EmailFrame
from cambio import CambioFrame
from excel_precos import ExcelFrame

FUNDO = "#101010"
SIDEBAR = "#181818"
BOTAO = "#1f6aa5"
HOVER = "#323232"


class MenuApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Sistema de Automação")
        self.geometry("1100x700")
        self.minsize(1100, 700)

        self.configure(
            fg_color=FUNDO
        )

        self.sidebar = ctk.CTkFrame(
            self,
            width=200,
            fg_color=SIDEBAR,
            corner_radius=0
        )

        self.sidebar.pack(
            side="left",
            fill="y"
        )
        self.sidebar.pack_propagate(False)

        self.conteudo = ctk.CTkFrame(
            self,
            fg_color=FUNDO
        )

        self.conteudo.pack(
            side="right",
            expand=True,
            fill="both"
        )

        self.logo = ctk.CTkLabel(
            self.sidebar,
            text="AUTOMAÇÃO",
            font=("Segoe UI", 24, "bold")
        )

        self.logo.pack(
            pady=(40, 30)
        )

        self.btn_calc = self.criar_botao(
            "Calculadora",
            self.abrir_calculadora
        )

        self.btn_email = self.criar_botao(
            "Enviar E-mail",
            self.abrir_email
        )

        self.btn_cambio = self.criar_botao(
            "Câmbio",
            self.abrir_cambio
        )

        self.btn_excel = self.criar_botao(
            "Excel",
            self.abrir_excel
        )

        self.sidebar_spacer = ctk.CTkFrame(
            self.sidebar,
            fg_color="transparent"
        )

        self.sidebar_spacer.pack(
            expand=True,
            fill="both"
        )

        self.btn_login = self.criar_botao_voltar()

        self.label_inicio = ctk.CTkLabel(
            self.conteudo,
            text="Bem-vindo",
            font=("Segoe UI", 34, "bold")
        )

        self.label_inicio.pack(
            pady=(200, 10)
        )

        self.label_sub = ctk.CTkLabel(
            self.conteudo,
            text="Selecione uma opção no menu lateral",
            font=("Segoe UI", 18),
            text_color="gray"
        )

        self.label_sub.pack()

        self.frame_atual = None

    def criar_botao(self, texto, comando):

        botao = ctk.CTkButton(
            self.sidebar,
            text=texto,
            command=comando,
            height=45,
            fg_color=BOTAO,
            hover_color=HOVER,
            corner_radius=10,
            font=("Segoe UI", 14)
        )

        botao.pack(
            pady=8,
            padx=15,
            fill="x"
        )

        return botao

    def criar_botao_voltar(self):

        botao = ctk.CTkButton(
            self.sidebar,
            text="Voltar ao Login",
            command=self.voltar_login,
            height=32,
            fg_color="transparent",
            hover_color=HOVER,
            text_color="gray",
            corner_radius=8,
            font=("Segoe UI", 12)
        )

        botao.pack(
            pady=(8, 20),
            padx=22,
            fill="x"
        )

        return botao

    def limpar_frame(self):

        if self.frame_atual:
            self.frame_atual.destroy()

        self.label_inicio.pack_forget()
        self.label_sub.pack_forget()

    def abrir_calculadora(self):

        self.limpar_frame()

        self.frame_atual = CalculadoraFrame(
            self.conteudo
        )

        self.frame_atual.pack(
            expand=True,
            fill="both",
            padx=20,
            pady=20
        )

    def voltar_login(self):

        self.destroy()

        from login import LoginApp

        login = LoginApp()
        login.mainloop()

    def abrir_email(self):

        self.limpar_frame()

        self.frame_atual = EmailFrame(
            self.conteudo
        )

        self.frame_atual.pack(
            expand=True,
            fill="both",
            padx=20,
            pady=20
        )

    def abrir_cambio(self):

        self.limpar_frame()

        self.frame_atual = CambioFrame(
            self.conteudo
        )

        self.frame_atual.pack(
            expand=True,
            fill="both",
            padx=20,
            pady=20
        )

    def abrir_excel(self):

        self.limpar_frame()

        self.frame_atual = ExcelFrame(
            self.conteudo
        )

        self.frame_atual.pack(
            expand=True,
            fill="both",
            padx=20,
            pady=20
        )
