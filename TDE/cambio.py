from datetime import datetime
from queue import Empty, Queue
from threading import Thread

import customtkinter as ctk
import requests


FUNDO = "#101010"
CARD = "#1b1b1b"
DISPLAY = "#111111"
BOTAO = "#242424"
HOVER = "#323232"
AZUL = "#1f6aa5"
AZUL_HOVER = "#144870"

MOEDAS = {
    "BRL": {"nome": "Real brasileiro", "simbolo": "R$"},
    "USD": {"nome": "Dólar americano", "simbolo": "US$"},
    "EUR": {"nome": "Euro", "simbolo": "€"},
    "GBP": {"nome": "Libra esterlina", "simbolo": "£"},
    "ARS": {"nome": "Peso argentino", "simbolo": "AR$"},
    "CAD": {"nome": "Dólar canadense", "simbolo": "C$"},
    "AUD": {"nome": "Dólar australiano", "simbolo": "A$"},
    "CHF": {"nome": "Franco suico", "simbolo": "CHF"},
    "JPY": {"nome": "Iene japonês", "simbolo": "¥"},
    "CNY": {"nome": "Yuan chinês", "simbolo": "¥"},
    "BTC": {"nome": "Bitcoin", "simbolo": "BTC"},
}

MOEDAS_API = [
    "USD",
    "EUR",
    "GBP",
    "ARS",
    "CAD",
    "AUD",
    "CHF",
    "JPY",
    "CNY",
    "BTC",
]

DESTAQUES = [
    "USD",
    "EUR",
    "GBP",
    "BTC",
]


class CambioFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(
            master,
            fg_color=FUNDO
        )

        self.cotacoes = {}
        self.cards_destaque = {}
        self.converter_apos_consulta = False
        self.fila_consulta = Queue()

        self.valor_var = ctk.StringVar(value="1")
        self.origem_var = ctk.StringVar(value="USD")
        self.destino_var = ctk.StringVar(value="BRL")
        self.resultado_var = ctk.StringVar(
            value="Atualize as cotações para converter"
        )
        self.status_var = ctk.StringVar(value="")

        self.titulo = ctk.CTkLabel(
            self,
            text="Câmbio",
            font=("Segoe UI", 28, "bold")
        )
        self.titulo.pack(pady=(18, 8))

        self.painel = ctk.CTkFrame(
            self,
            fg_color=CARD,
            corner_radius=15
        )
        self.painel.pack(
            padx=30,
            pady=(8, 12),
            fill="x"
        )

        self.criar_formulario()

        self.resultado = ctk.CTkLabel(
            self.painel,
            textvariable=self.resultado_var,
            fg_color=DISPLAY,
            corner_radius=12,
            height=64,
            font=("Segoe UI", 23, "bold")
        )
        self.resultado.grid(
            row=2,
            column=0,
            columnspan=6,
            padx=15,
            pady=(6, 15),
            sticky="ew"
        )

        self.status = ctk.CTkLabel(
            self,
            textvariable=self.status_var,
            text_color="gray",
            font=("Segoe UI", 13)
        )
        self.status.pack(pady=(0, 8))

        self.frame_cards = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        self.frame_cards.pack(
            padx=30,
            pady=(0, 10),
            fill="x"
        )
        self.criar_cards_destaque()

        self.tabela = ctk.CTkScrollableFrame(
            self,
            width=780,
            height=260,
            fg_color=CARD,
            corner_radius=15
        )
        self.tabela.pack(
            padx=30,
            pady=(0, 20),
            fill="both",
            expand=True
        )

        self.atualizar_tabela()

    def criar_formulario(self):
        self.label_valor = ctk.CTkLabel(
            self.painel,
            text="Valor",
            text_color="gray",
            font=("Segoe UI", 13, "bold")
        )
        self.label_valor.grid(
            row=0,
            column=0,
            padx=(15, 6),
            pady=(15, 5),
            sticky="w"
        )

        self.label_origem = ctk.CTkLabel(
            self.painel,
            text="De",
            text_color="gray",
            font=("Segoe UI", 13, "bold")
        )
        self.label_origem.grid(
            row=0,
            column=1,
            padx=6,
            pady=(15, 5),
            sticky="w"
        )

        self.label_destino = ctk.CTkLabel(
            self.painel,
            text="Para",
            text_color="gray",
            font=("Segoe UI", 13, "bold")
        )
        self.label_destino.grid(
            row=0,
            column=2,
            padx=6,
            pady=(15, 5),
            sticky="w"
        )

        self.entry_valor = ctk.CTkEntry(
            self.painel,
            textvariable=self.valor_var,
            width=150,
            height=40
        )
        self.entry_valor.grid(
            row=1,
            column=0,
            padx=(15, 6),
            pady=(0, 12),
            sticky="ew"
        )

        self.combo_origem = ctk.CTkComboBox(
            self.painel,
            values=list(MOEDAS.keys()),
            variable=self.origem_var,
            width=120,
            height=40
        )
        self.combo_origem.grid(
            row=1,
            column=1,
            padx=6,
            pady=(0, 12),
            sticky="w"
        )

        self.combo_destino = ctk.CTkComboBox(
            self.painel,
            values=list(MOEDAS.keys()),
            variable=self.destino_var,
            width=120,
            height=40
        )
        self.combo_destino.grid(
            row=1,
            column=2,
            padx=6,
            pady=(0, 12),
            sticky="w"
        )

        self.btn_inverter = ctk.CTkButton(
            self.painel,
            text="Inverter",
            command=self.inverter_moedas,
            fg_color=BOTAO,
            hover_color=HOVER,
            width=95,
            height=40
        )
        self.btn_inverter.grid(
            row=1,
            column=3,
            padx=6,
            pady=(0, 12)
        )

        self.btn_converter = ctk.CTkButton(
            self.painel,
            text="Converter",
            command=self.converter,
            fg_color=AZUL,
            hover_color=AZUL_HOVER,
            width=110,
            height=40
        )
        self.btn_converter.grid(
            row=1,
            column=4,
            padx=6,
            pady=(0, 12)
        )

        self.btn_consultar = ctk.CTkButton(
            self.painel,
            text="Atualizar",
            command=self.consultar,
            fg_color=BOTAO,
            hover_color=HOVER,
            width=105,
            height=40
        )
        self.btn_consultar.grid(
            row=1,
            column=5,
            padx=(6, 15),
            pady=(0, 12)
        )

        self.entry_valor.bind(
            "<Return>",
            lambda evento: self.converter()
        )

        for coluna in range(6):
            self.painel.grid_columnconfigure(
                coluna,
                weight=1
            )

    def criar_cards_destaque(self):
        for coluna, codigo in enumerate(DESTAQUES):
            card = ctk.CTkFrame(
                self.frame_cards,
                fg_color=CARD,
                corner_radius=15
            )
            card.grid(
                row=0,
                column=coluna,
                padx=6,
                sticky="ew"
            )
            self.frame_cards.grid_columnconfigure(
                coluna,
                weight=1
            )

            titulo = ctk.CTkLabel(
                card,
                text=f"{codigo} / BRL",
                text_color="gray",
                font=("Segoe UI", 13, "bold")
            )
            titulo.pack(pady=(12, 2))

            valor = ctk.CTkLabel(
                card,
                text="--",
                font=("Segoe UI", 20, "bold")
            )
            valor.pack(pady=2)

            variacao = ctk.CTkLabel(
                card,
                text="Aguardando",
                text_color="gray",
                font=("Segoe UI", 12)
            )
            variacao.pack(pady=(0, 12))

            self.cards_destaque[codigo] = {
                "valor": valor,
                "variacao": variacao,
            }

    def consultar(self, converter_depois=False):
        self.converter_apos_consulta = converter_depois
        self.status_var.set("Buscando cotações...")
        self.btn_consultar.configure(
            text="Atualizando...",
            state="disabled"
        )

        Thread(
            target=self.buscar_cotacoes,
            daemon=True
        ).start()
        self.after(
            100,
            self.verificar_fila_consulta
        )

    def buscar_cotacoes(self):
        try:
            pares = ",".join(
                f"{codigo}-BRL" for codigo in MOEDAS_API
            )
            url = f"https://economia.awesomeapi.com.br/json/last/{pares}"
            resposta = requests.get(
                url,
                timeout=10
            )
            resposta.raise_for_status()
            dados = resposta.json()
            cotacoes = self.normalizar_cotacoes(dados)

            self.fila_consulta.put(
                ("sucesso", cotacoes)
            )

        except requests.exceptions.RequestException:
            self.fila_consulta.put(
                (
                    "erro",
                    "Erro de conexao com a internet ou com a API"
                )
            )

        except (KeyError, ValueError):
            self.fila_consulta.put(
                (
                    "erro",
                    "Erro ao interpretar os dados recebidos da API"
                )
            )

    def verificar_fila_consulta(self):
        try:
            status, payload = self.fila_consulta.get_nowait()

        except Empty:
            self.after(
                100,
                self.verificar_fila_consulta
            )
            return

        if status == "sucesso":
            self.aplicar_cotacoes(payload)
            return

        self.exibir_erro(payload)

    def normalizar_cotacoes(self, dados):
        cotacoes = {}

        for codigo in MOEDAS_API:
            chave = f"{codigo}BRL"

            if chave not in dados:
                continue

            item = dados[chave]
            cotacoes[codigo] = {
                "nome": MOEDAS[codigo]["nome"],
                "bid": float(item["bid"]),
                "ask": float(item.get("ask", item["bid"])),
                "high": float(item.get("high", item["bid"])),
                "low": float(item.get("low", item["bid"])),
                "pct": float(item.get("pctChange", 0)),
                "create_date": item.get("create_date", ""),
            }

        if not cotacoes:
            raise ValueError("sem cotações")

        return cotacoes

    def aplicar_cotacoes(self, cotacoes):
        self.cotacoes = cotacoes
        horario = self.obter_horario_cotacao()

        self.status_var.set(
            f"Cotações atualizadas em {horario}"
        )
        self.btn_consultar.configure(
            text="Atualizar",
            state="normal"
        )

        self.atualizar_cards()
        self.atualizar_tabela()

        if self.converter_apos_consulta:
            self.converter_apos_consulta = False
            self.converter()

    def exibir_erro(self, mensagem):
        self.status_var.set(mensagem)
        self.resultado_var.set("Não foi possivel atualizar agora")
        self.btn_consultar.configure(
            text="Atualizar",
            state="normal"
        )

    def atualizar_cards(self):
        for codigo, widgets in self.cards_destaque.items():
            cotacao = self.cotacoes.get(codigo)

            if not cotacao:
                widgets["valor"].configure(text="--")
                widgets["variacao"].configure(
                    text="Sem dados",
                    text_color="gray"
                )
                continue

            pct = cotacao["pct"]
            cor = "#4ade80" if pct >= 0 else "#f87171"
            sinal = "+" if pct >= 0 else ""

            widgets["valor"].configure(
                text=self.formatar_brl(cotacao["bid"])
            )
            widgets["variacao"].configure(
                text=f"{sinal}{pct:.2f}% no dia",
                text_color=cor
            )

    def atualizar_tabela(self):
        for widget in self.tabela.winfo_children():
            widget.destroy()

        self.criar_cabecalho_tabela()

        if not self.cotacoes:
            label = ctk.CTkLabel(
                self.tabela,
                text="Clique em Atualizar para carregar as cotações",
                text_color="gray",
                font=("Segoe UI", 14)
            )
            label.grid(
                row=1,
                column=0,
                columnspan=6,
                padx=12,
                pady=30
            )
            return

        for indice, codigo in enumerate(MOEDAS_API, start=1):
            cotacao = self.cotacoes.get(codigo)

            if not cotacao:
                continue

            self.criar_linha_tabela(
                indice,
                codigo,
                cotacao
            )

    def criar_cabecalho_tabela(self):
        colunas = [
            ("Moeda", 70),
            ("Nome", 170),
            ("Compra", 100),
            ("Venda", 100),
            ("Variação", 80),
            ("Min / Max", 180),
        ]

        pesos = [1, 2, 1, 1, 1, 2]

        for coluna, (texto, largura) in enumerate(colunas):
            self.tabela.grid_columnconfigure(
                coluna,
                weight=pesos[coluna],
                minsize=largura
            )

            label = ctk.CTkLabel(
                self.tabela,
                text=texto,
                width=largura,
                font=("Segoe UI", 13, "bold"),
                text_color="gray"
            )
            label.grid(
                row=0,
                column=coluna,
                padx=6,
                pady=(8, 6),
                sticky="ew"
            )

    def criar_linha_tabela(self, linha, codigo, cotacao):
        pct = cotacao["pct"]
        cor_pct = "#4ade80" if pct >= 0 else "#f87171"
        sinal = "+" if pct >= 0 else ""
        valores = [
            codigo,
            cotacao["nome"],
            self.formatar_brl(cotacao["bid"]),
            self.formatar_brl(cotacao["ask"]),
            f"{sinal}{pct:.2f}%",
            (
                f"{self.formatar_brl(cotacao['low'])} / "
                f"{self.formatar_brl(cotacao['high'])}"
            ),
        ]

        for coluna, texto in enumerate(valores):
            label = ctk.CTkLabel(
                self.tabela,
                text=texto,
                width=[70, 170, 100, 100, 80, 180][coluna],
                font=("Segoe UI", 12),
                text_color=cor_pct if coluna == 4 else "white"
            )
            label.grid(
                row=linha,
                column=coluna,
                padx=6,
                pady=5,
                sticky="ew"
            )

    def converter(self):
        if not self.cotacoes:
            self.consultar(converter_depois=True)
            return

        try:
            valor = self.converter_numero(
                self.valor_var.get()
            )

        except ValueError:
            self.resultado_var.set("Digite um valor valido")
            self.status_var.set("")
            return

        origem = self.origem_var.get()
        destino = self.destino_var.get()

        if origem == destino:
            convertido = valor

        else:
            try:
                valor_brl = self.converter_para_brl(
                    valor,
                    origem
                )
                convertido = self.converter_de_brl(
                    valor_brl,
                    destino
                )

            except KeyError:
                self.resultado_var.set(
                    "Cotação indisponível para essa conversão"
                )
                return

        texto = (
            f"{self.formatar_moeda(valor, origem)} = "
            f"{self.formatar_moeda(convertido, destino)}"
        )
        self.resultado_var.set(texto)

    def converter_para_brl(self, valor, codigo):
        if codigo == "BRL":
            return valor

        return valor * self.cotacoes[codigo]["bid"]

    def converter_de_brl(self, valor_brl, codigo):
        if codigo == "BRL":
            return valor_brl

        return valor_brl / self.cotacoes[codigo]["bid"]

    def inverter_moedas(self):
        origem = self.origem_var.get()
        destino = self.destino_var.get()

        self.origem_var.set(destino)
        self.destino_var.set(origem)
        self.converter()

    def obter_horario_cotacao(self):
        datas = [
            item["create_date"]
            for item in self.cotacoes.values()
            if item.get("create_date")
        ]

        if datas:
            return datas[0]

        return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    def converter_numero(self, valor):
        texto = str(valor).strip()

        if not texto:
            raise ValueError("valor vazio")

        texto = (
            texto.replace("US$", "")
            .replace("AR$", "")
            .replace("C$", "")
            .replace("A$", "")
            .replace("R$", "")
            .replace("CHF", "")
            .replace("BTC", "")
            .replace("€", "")
            .replace("£", "")
            .replace("¥", "")
            .replace(" ", "")
        )

        if "," in texto and "." in texto:
            texto = texto.replace(".", "")
            texto = texto.replace(",", ".")

        else:
            texto = texto.replace(",", ".")

        return float(texto)

    def formatar_decimal(self, valor, casas=2):
        texto = f"{valor:,.{casas}f}"
        return (
            texto.replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
        )

    def formatar_brl(self, valor):
        casas = 2 if abs(valor) >= 1 else 4
        return f"R$ {self.formatar_decimal(valor, casas)}"

    def formatar_moeda(self, valor, codigo):
        simbolo = MOEDAS[codigo]["simbolo"]
        casas = 8 if codigo == "BTC" else 2

        if codigo in ("JPY",):
            casas = 0

        return f"{simbolo} {self.formatar_decimal(valor, casas)}"
