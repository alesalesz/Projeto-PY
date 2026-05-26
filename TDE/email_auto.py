import mimetypes
import os
import re
import smtplib
from email.message import EmailMessage
from pathlib import Path
from queue import Empty, Queue
from threading import Thread
from tkinter import filedialog

import customtkinter as ctk


FUNDO = "#101010"
CARD = "#1b1b1b"
BOTAO = "#242424"
HOVER = "#323232"
AZUL = "#1f6aa5"
AZUL_HOVER = "#144870"
DISPLAY = "#111111"
EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class EmailFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(
            master,
            fg_color=FUNDO
        )

        self.anexos = []
        self.fila_envio = Queue()
        self.enviando = False
        self.smtp_factory = smtplib.SMTP_SSL
        self._atalho_envio = None

        self.titulo = ctk.CTkLabel(
            self,
            text="Envio de E-mail",
            font=("Segoe UI", 28, "bold")
        )
        self.titulo.grid(
            row=0,
            column=0,
            pady=(18, 8),
            sticky="ew"
        )

        self.area_formulario = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            corner_radius=0
        )
        self.area_formulario.grid(
            row=1,
            column=0,
            sticky="nsew"
        )
        self.grid_columnconfigure(
            0,
            weight=1
        )
        self.grid_rowconfigure(
            1,
            weight=1
        )

        self.card = ctk.CTkFrame(
            self.area_formulario,
            fg_color=CARD,
            corner_radius=15
        )
        self.card.pack(
            padx=30,
            pady=(0, 10),
            fill="x"
        )

        self.criar_campos()
        self.criar_area_anexos()
        self.criar_acoes()

        self.atualizar_lista_anexos()
        self.after(
            100,
            self.configurar_atalho
        )

    def configurar_atalho(self):
        if not self.winfo_exists():
            return

        janela = self.winfo_toplevel()
        self._atalho_envio = janela.bind(
            "<Control-Return>",
            lambda evento: self.enviar_email(),
            add="+"
        )

    def criar_campos(self):
        self.label_destinatario = ctk.CTkLabel(
            self.card,
            text="Destinatarios",
            text_color="gray",
            font=("Segoe UI", 13, "bold")
        )
        self.label_destinatario.grid(
            row=0,
            column=0,
            padx=15,
            pady=(15, 5),
            sticky="w"
        )

        self.entry_destinatario = ctk.CTkEntry(
            self.card,
            placeholder_text="email@exemplo.com, outro@exemplo.com",
            height=40
        )
        self.entry_destinatario.grid(
            row=1,
            column=0,
            columnspan=2,
            padx=15,
            pady=(0, 10),
            sticky="ew"
        )

        self.label_cc = ctk.CTkLabel(
            self.card,
            text="CC",
            text_color="gray",
            font=("Segoe UI", 13, "bold")
        )
        self.label_cc.grid(
            row=2,
            column=0,
            padx=15,
            pady=(0, 5),
            sticky="w"
        )

        self.label_cco = ctk.CTkLabel(
            self.card,
            text="CCO",
            text_color="gray",
            font=("Segoe UI", 13, "bold")
        )
        self.label_cco.grid(
            row=2,
            column=1,
            padx=15,
            pady=(0, 5),
            sticky="w"
        )

        self.entry_cc = ctk.CTkEntry(
            self.card,
            placeholder_text="copias opcionais",
            height=40
        )
        self.entry_cc.grid(
            row=3,
            column=0,
            padx=15,
            pady=(0, 10),
            sticky="ew"
        )

        self.entry_cco = ctk.CTkEntry(
            self.card,
            placeholder_text="copias ocultas",
            height=40
        )
        self.entry_cco.grid(
            row=3,
            column=1,
            padx=15,
            pady=(0, 10),
            sticky="ew"
        )

        self.label_assunto = ctk.CTkLabel(
            self.card,
            text="Assunto",
            text_color="gray",
            font=("Segoe UI", 13, "bold")
        )
        self.label_assunto.grid(
            row=4,
            column=0,
            padx=15,
            pady=(0, 5),
            sticky="w"
        )

        self.entry_assunto = ctk.CTkEntry(
            self.card,
            placeholder_text="Assunto",
            height=40
        )
        self.entry_assunto.grid(
            row=5,
            column=0,
            columnspan=2,
            padx=15,
            pady=(0, 10),
            sticky="ew"
        )

        self.label_mensagem = ctk.CTkLabel(
            self.card,
            text="Mensagem",
            text_color="gray",
            font=("Segoe UI", 13, "bold")
        )
        self.label_mensagem.grid(
            row=6,
            column=0,
            padx=15,
            pady=(0, 5),
            sticky="w"
        )

        self.texto_mensagem = ctk.CTkTextbox(
            self.card,
            height=90,
            fg_color=DISPLAY,
            corner_radius=12
        )
        self.texto_mensagem.grid(
            row=7,
            column=0,
            columnspan=2,
            padx=15,
            pady=(0, 12),
            sticky="nsew"
        )

        self.card.grid_columnconfigure(
            0,
            weight=1
        )
        self.card.grid_columnconfigure(
            1,
            weight=1
        )
        self.card.grid_rowconfigure(
            7,
            weight=0
        )

    def criar_area_anexos(self):
        self.frame_anexo_topo = ctk.CTkFrame(
            self.card,
            fg_color="transparent"
        )
        self.frame_anexo_topo.grid(
            row=8,
            column=0,
            columnspan=2,
            padx=15,
            pady=(0, 8),
            sticky="ew"
        )

        self.label_anexos = ctk.CTkLabel(
            self.frame_anexo_topo,
            text="Anexos",
            text_color="gray",
            font=("Segoe UI", 13, "bold")
        )
        self.label_anexos.pack(
            side="left"
        )

        self.btn_anexar = ctk.CTkButton(
            self.frame_anexo_topo,
            text="Selecionar Anexos",
            command=self.selecionar_anexos,
            fg_color=BOTAO,
            hover_color=HOVER,
            width=150,
            height=34
        )
        self.btn_anexar.pack(
            side="right",
            padx=(8, 0)
        )

        self.btn_planilha = ctk.CTkButton(
            self.frame_anexo_topo,
            text="Anexar Planilha",
            command=self.anexar_planilha_padrao,
            fg_color=BOTAO,
            hover_color=HOVER,
            width=145,
            height=34
        )
        self.btn_planilha.pack(
            side="right",
            padx=(8, 0)
        )

        self.btn_limpar_anexos = ctk.CTkButton(
            self.frame_anexo_topo,
            text="Limpar Anexos",
            command=self.limpar_anexos,
            fg_color=BOTAO,
            hover_color=HOVER,
            width=130,
            height=34
        )
        self.btn_limpar_anexos.pack(
            side="right"
        )

        self.lista_anexos = ctk.CTkScrollableFrame(
            self.card,
            height=76,
            fg_color=DISPLAY,
            corner_radius=12
        )
        self.lista_anexos.grid(
            row=9,
            column=0,
            columnspan=2,
            padx=15,
            pady=(0, 12),
            sticky="ew"
        )

    def criar_acoes(self):
        self.frame_acoes = ctk.CTkFrame(
            self.card,
            fg_color="transparent"
        )
        self.frame_acoes.grid(
            row=10,
            column=0,
            columnspan=2,
            padx=15,
            pady=(0, 12),
            sticky="ew"
        )

        self.frame_acoes.grid_columnconfigure(
            2,
            weight=1
        )

        self.btn_limpar = ctk.CTkButton(
            self.frame_acoes,
            text="Limpar",
            command=self.limpar_formulario,
            fg_color=BOTAO,
            hover_color=HOVER,
            width=110,
            height=40
        )
        self.btn_limpar.grid(
            row=0,
            column=0
        )

        self.btn_testar = ctk.CTkButton(
            self.frame_acoes,
            text="Testar Gmail",
            command=self.testar_gmail,
            fg_color=BOTAO,
            hover_color=HOVER,
            width=130,
            height=40
        )
        self.btn_testar.grid(
            row=0,
            column=1,
            padx=(8, 0)
        )

        self.btn_enviar = ctk.CTkButton(
            self.frame_acoes,
            text="Enviar E-mail",
            command=self.enviar_email,
            fg_color=AZUL,
            hover_color=AZUL_HOVER,
            width=150,
            height=40,
            font=("Segoe UI", 14, "bold")
        )
        self.btn_enviar.grid(
            row=0,
            column=4
        )

        self.resultado = ctk.CTkLabel(
            self.frame_acoes,
            text="",
            text_color="gray",
            font=("Segoe UI", 13),
            anchor="w"
        )
        self.resultado.grid(
            row=0,
            column=3,
            padx=(12, 12),
            sticky="ew"
        )

    def selecionar_anexos(self):
        arquivos = filedialog.askopenfilenames(
            filetypes=[
                ("Arquivos comuns", "*.xlsx *.xls *.csv *.pdf *.docx *.txt *.png *.jpg *.jpeg"),
                ("Todos os arquivos", "*.*"),
            ]
        )

        if not arquivos:
            return

        self.adicionar_anexos(arquivos)

    def anexar_planilha_padrao(self):
        caminho = (
            Path(__file__).resolve().parents[1]
            / "Arquivos"
            / "precos.xlsx"
        )

        if not caminho.exists():
            self.exibir_mensagem(
                "Planilha padrao nao encontrada",
                "red"
            )
            return

        self.adicionar_anexos([caminho])

    def adicionar_anexos(self, caminhos):
        anexos_atuais = {
            str(path.resolve())
            for path in self.anexos
        }
        adicionados = 0

        for caminho in caminhos:
            path = Path(caminho)

            if not path.exists() or not path.is_file():
                continue

            caminho_resolvido = str(path.resolve())

            if caminho_resolvido in anexos_atuais:
                continue

            self.anexos.append(path)
            anexos_atuais.add(caminho_resolvido)
            adicionados += 1

        if adicionados:
            self.exibir_mensagem(
                f"{adicionados} anexo(s) adicionado(s)"
            )

        else:
            self.exibir_mensagem(
                "Nenhum anexo novo foi adicionado",
                "gray"
            )

        self.atualizar_lista_anexos()

    def atualizar_lista_anexos(self):
        for widget in self.lista_anexos.winfo_children():
            widget.destroy()

        if not self.anexos:
            vazio = ctk.CTkLabel(
                self.lista_anexos,
                text="Nenhum anexo selecionado",
                text_color="gray",
                font=("Segoe UI", 13)
            )
            vazio.pack(
                pady=24
            )
            return

        for caminho in self.anexos:
            linha = ctk.CTkFrame(
                self.lista_anexos,
                fg_color="transparent"
            )
            linha.pack(
                fill="x",
                padx=8,
                pady=5
            )

            nome = ctk.CTkLabel(
                linha,
                text=caminho.name,
                anchor="w",
                font=("Segoe UI", 13)
            )
            nome.pack(
                side="left",
                fill="x",
                expand=True
            )

            tamanho = ctk.CTkLabel(
                linha,
                text=self.formatar_tamanho(caminho),
                text_color="gray",
                width=80,
                font=("Segoe UI", 12)
            )
            tamanho.pack(
                side="left",
                padx=8
            )

            remover = ctk.CTkButton(
                linha,
                text="Remover",
                command=lambda path=caminho: self.remover_anexo(path),
                fg_color=BOTAO,
                hover_color=HOVER,
                width=90,
                height=30
            )
            remover.pack(
                side="right"
            )

    def remover_anexo(self, caminho):
        self.anexos = [
            anexo
            for anexo in self.anexos
            if anexo.resolve() != caminho.resolve()
        ]
        self.exibir_mensagem("Anexo removido")
        self.atualizar_lista_anexos()

    def limpar_anexos(self):
        self.anexos = []
        self.exibir_mensagem("Anexos removidos")
        self.atualizar_lista_anexos()

    def enviar_email(self):
        if self.enviando:
            return

        dados = self.coletar_dados()

        if not dados:
            return

        self.definir_ocupado(True, "enviar")
        self.exibir_mensagem("Enviando e-mail...")

        Thread(
            target=self.enviar_em_segundo_plano,
            args=(dados,),
            daemon=True
        ).start()
        self.after(
            100,
            self.verificar_fila_envio
        )

    def testar_gmail(self):
        if self.enviando:
            return

        credenciais = self.obter_credenciais()

        if not credenciais:
            return

        self.definir_ocupado(True, "testar")
        self.exibir_mensagem("Testando conexao com o Gmail...")

        Thread(
            target=self.testar_gmail_em_segundo_plano,
            args=(credenciais,),
            daemon=True
        ).start()
        self.after(
            100,
            self.verificar_fila_envio
        )

    def definir_ocupado(self, ocupado, acao=None):
        self.enviando = ocupado
        estado = "disabled" if ocupado else "normal"

        self.btn_enviar.configure(
            text="Enviando..." if acao == "enviar" else "Enviar E-mail",
            state=estado
        )
        self.btn_testar.configure(
            text="Testando..." if acao == "testar" else "Testar Gmail",
            state=estado
        )
        self.btn_limpar.configure(state=estado)

    def coletar_dados(self):
        destinatarios = self.parse_emails(
            self.entry_destinatario.get()
        )
        cc = self.parse_emails(
            self.entry_cc.get()
        )
        cco = self.parse_emails(
            self.entry_cco.get()
        )
        assunto = self.entry_assunto.get().strip()
        mensagem = self.texto_mensagem.get(
            "1.0",
            "end"
        ).strip()

        todos_emails = destinatarios + cc + cco

        if not destinatarios:
            self.exibir_mensagem(
                "Informe ao menos um destinatario",
                "red"
            )
            return None

        invalidos = [
            email
            for email in todos_emails
            if not self.email_valido(email)
        ]

        if invalidos:
            self.exibir_mensagem(
                f"E-mail invalido: {invalidos[0]}",
                "red"
            )
            return None

        if not assunto:
            self.exibir_mensagem(
                "Informe o assunto",
                "red"
            )
            return None

        if not mensagem:
            self.exibir_mensagem(
                "Digite a mensagem",
                "red"
            )
            return None

        anexos_validos = []

        for caminho in self.anexos:
            if not caminho.exists() or not caminho.is_file():
                self.exibir_mensagem(
                    f"Anexo nao encontrado: {caminho.name}",
                    "red"
                )
                return None

            anexos_validos.append(caminho)

        credenciais = self.obter_credenciais()

        if not credenciais:
            return None

        return {
            "remetente": credenciais["remetente"],
            "senha": credenciais["senha"],
            "destinatarios": destinatarios,
            "cc": cc,
            "cco": cco,
            "assunto": assunto,
            "mensagem": mensagem,
            "anexos": anexos_validos,
        }

    def obter_credenciais(self):
        email_remetente = os.getenv("EMAIL_REMETENTE")
        senha_email = os.getenv("SENHA_EMAIL")

        if not email_remetente or not senha_email:
            self.exibir_mensagem(
                "Configure EMAIL_REMETENTE e SENHA_EMAIL",
                "red"
            )
            return None

        if not self.email_valido(email_remetente):
            self.exibir_mensagem(
                "EMAIL_REMETENTE invalido",
                "red"
            )
            return None

        return {
            "remetente": email_remetente,
            "senha": senha_email,
        }

    def enviar_em_segundo_plano(self, dados):
        try:
            email = EmailMessage()
            email["From"] = dados["remetente"]
            email["To"] = ", ".join(dados["destinatarios"])
            email["Subject"] = dados["assunto"]

            if dados["cc"]:
                email["Cc"] = ", ".join(dados["cc"])

            email.set_content(dados["mensagem"])

            for caminho in dados["anexos"]:
                self.adicionar_anexo_ao_email(
                    email,
                    caminho
                )

            destinatarios_envio = (
                dados["destinatarios"]
                + dados["cc"]
                + dados["cco"]
            )

            with self.smtp_factory(
                "smtp.gmail.com",
                465,
                timeout=20
            ) as smtp:
                smtp.login(
                    dados["remetente"],
                    dados["senha"]
                )
                smtp.send_message(
                    email,
                    from_addr=dados["remetente"],
                    to_addrs=destinatarios_envio
                )

            self.fila_envio.put(
                ("sucesso", "E-mail enviado com sucesso")
            )

        except smtplib.SMTPAuthenticationError:
            self.fila_envio.put(
                (
                    "erro",
                    "Erro de autenticacao. Verifique a senha de aplicativo"
                )
            )

        except (smtplib.SMTPException, OSError) as erro:
            self.fila_envio.put(
                (
                    "erro",
                    f"Erro ao enviar e-mail: {erro}"
                )
            )

        except Exception as erro:
            self.fila_envio.put(
                (
                    "erro",
                    f"Erro: {erro}"
                )
            )

    def testar_gmail_em_segundo_plano(self, credenciais):
        try:
            with self.smtp_factory(
                "smtp.gmail.com",
                465,
                timeout=20
            ) as smtp:
                smtp.login(
                    credenciais["remetente"],
                    credenciais["senha"]
                )

            self.fila_envio.put(
                ("sucesso", "Gmail conectado com sucesso")
            )

        except smtplib.SMTPAuthenticationError:
            self.fila_envio.put(
                (
                    "erro",
                    "Erro de autenticacao. Verifique a senha de aplicativo"
                )
            )

        except (smtplib.SMTPException, OSError) as erro:
            self.fila_envio.put(
                (
                    "erro",
                    f"Erro ao conectar no Gmail: {erro}"
                )
            )

        except Exception as erro:
            self.fila_envio.put(
                (
                    "erro",
                    f"Erro: {erro}"
                )
            )

    def verificar_fila_envio(self):
        try:
            status, mensagem = self.fila_envio.get_nowait()

        except Empty:
            self.after(
                100,
                self.verificar_fila_envio
            )
            return

        self.definir_ocupado(False)

        if status == "sucesso":
            self.exibir_mensagem(
                mensagem,
                "green"
            )
            return

        self.exibir_mensagem(
            mensagem,
            "red"
        )

    def adicionar_anexo_ao_email(self, email, caminho):
        mime_type, _ = mimetypes.guess_type(caminho)

        if mime_type:
            maintype, subtype = mime_type.split(
                "/",
                1
            )

        else:
            maintype = "application"
            subtype = "octet-stream"

        with open(caminho, "rb") as arquivo:
            email.add_attachment(
                arquivo.read(),
                maintype=maintype,
                subtype=subtype,
                filename=caminho.name
            )

    def limpar_formulario(self):
        self.entry_destinatario.delete(
            0,
            "end"
        )
        self.entry_cc.delete(
            0,
            "end"
        )
        self.entry_cco.delete(
            0,
            "end"
        )
        self.entry_assunto.delete(
            0,
            "end"
        )
        self.texto_mensagem.delete(
            "1.0",
            "end"
        )
        self.anexos = []
        self.atualizar_lista_anexos()
        self.exibir_mensagem("Formulario limpo")

    def parse_emails(self, texto):
        return [
            email.strip()
            for email in re.split(r"[;,]", texto)
            if email.strip()
        ]

    def email_valido(self, email):
        return bool(
            EMAIL_REGEX.match(email)
        )

    def formatar_tamanho(self, caminho):
        try:
            tamanho = caminho.stat().st_size

        except OSError:
            return "--"

        if tamanho < 1024:
            return f"{tamanho} B"

        if tamanho < 1024 * 1024:
            return f"{tamanho / 1024:.1f} KB"

        return f"{tamanho / (1024 * 1024):.1f} MB"

    def exibir_mensagem(self, mensagem, cor="gray"):
        self.resultado.configure(
            text=mensagem,
            text_color=cor
        )

    def destroy(self):
        if self._atalho_envio:
            janela = self.winfo_toplevel()
            janela.unbind(
                "<Control-Return>",
                self._atalho_envio
            )

        super().destroy()
