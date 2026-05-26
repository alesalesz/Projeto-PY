import customtkinter as ctk

from menu import MenuApp


USUARIO_PADRAO = "admin"
SENHA_PADRAO = "1234"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

FUNDO = "#0f0f0f"
CARD = "#1a1a1a"
AZUL = "#1f6aa5"
HOVER = "#144870"


class LoginApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Sistema de Automação")
        self.geometry("550x430")
        self.resizable(False, False)
        self.configure(fg_color=FUNDO)

        self.frame = ctk.CTkFrame(
            self,
            fg_color=CARD,
            corner_radius=20
        )
        self.frame.pack(
            expand=True,
            fill="both",
            padx=30,
            pady=30
        )

        self.titulo = ctk.CTkLabel(
            self.frame,
            text="Sistema de Automação",
            font=("Segoe UI", 30, "bold")
        )
        self.titulo.pack(pady=(40, 10))

        self.subtitulo = ctk.CTkLabel(
            self.frame,
            text="Acesse para continuar",
            font=("Segoe UI", 16)
        )
        self.subtitulo.pack(pady=(0, 30))

        self.entry_usuario = ctk.CTkEntry(
            self.frame,
            placeholder_text="Usuário",
            width=320,
            height=45,
            corner_radius=12
        )
        self.entry_usuario.pack(pady=10)

        self.entry_senha = ctk.CTkEntry(
            self.frame,
            placeholder_text="Senha",
            show="*",
            width=320,
            height=45,
            corner_radius=12
        )
        self.entry_senha.pack(pady=10)

        self.botao_login = ctk.CTkButton(
            self.frame,
            text="Entrar",
            width=320,
            height=45,
            corner_radius=12,
            fg_color=AZUL,
            hover_color=HOVER,
            font=("Segoe UI", 15, "bold"),
            command=self.verificar_login
        )
        self.botao_login.pack(pady=(20, 10))

        self.label_resultado = ctk.CTkLabel(
            self.frame,
            text="",
            font=("Segoe UI", 14)
        )
        self.label_resultado.pack(pady=20)

        self.bind(
            "<Return>",
            lambda event: self.verificar_login()
        )

    def verificar_login(self):
        usuario = self.entry_usuario.get().strip()
        senha = self.entry_senha.get().strip()

        if not usuario or not senha:
            self.label_resultado.configure(
                text="Preencha usuário e senha",
                text_color="red"
            )
            return

        if usuario == USUARIO_PADRAO and senha == SENHA_PADRAO:
            self.destroy()

            menu = MenuApp()
            menu.mainloop()
            return

        self.label_resultado.configure(
            text="Usuário ou senha incorretos",
            text_color="red"
        )
