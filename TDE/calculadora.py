import ast
import math
import operator

import customtkinter as ctk


FUNDO = "#101010"
CARD = "#1b1b1b"
DISPLAY = "#111111"
BOTAO = "#242424"
HOVER = "#323232"
AZUL = "#1f6aa5"
AZUL_HOVER = "#144870"
TEXTO_SECUNDARIO = "gray"


class CalculadoraFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(
            master,
            fg_color=FUNDO
        )

        self.expressao = ""
        self.display_var = ctk.StringVar(value="0")
        self.status_var = ctk.StringVar(
            value="Use os botoes ou o teclado"
        )
        self._atalho_teclado = None

        self.titulo = ctk.CTkLabel(
            self,
            text="Calculadora",
            font=("Segoe UI", 28, "bold")
        )
        self.titulo.pack(pady=(20, 8))

        self.card = ctk.CTkFrame(
            self,
            fg_color=CARD,
            corner_radius=15
        )
        self.card.pack(
            padx=30,
            pady=15
        )

        self.display = ctk.CTkLabel(
            self.card,
            textvariable=self.display_var,
            width=420,
            height=80,
            fg_color=DISPLAY,
            corner_radius=12,
            anchor="e",
            font=("Segoe UI", 34, "bold")
        )
        self.display.grid(
            row=0,
            column=0,
            columnspan=5,
            padx=15,
            pady=(15, 8),
            sticky="ew"
        )

        self.status = ctk.CTkLabel(
            self.card,
            textvariable=self.status_var,
            text_color=TEXTO_SECUNDARIO,
            font=("Segoe UI", 13)
        )
        self.status.grid(
            row=1,
            column=0,
            columnspan=5,
            pady=(0, 10)
        )

        botoes = [
            ["C", "DEL", "(", ")", "%"],
            ["7", "8", "9", "/", "sqrt"],
            ["4", "5", "6", "*", "^"],
            ["1", "2", "3", "-", "x2"],
            ["0", ".", "+/-", "+", "="],
        ]

        for linha, itens in enumerate(botoes, start=2):
            for coluna, texto in enumerate(itens):
                self.criar_botao(texto, linha, coluna)

        for coluna in range(5):
            self.card.grid_columnconfigure(
                coluna,
                weight=1
            )

        self.after(
            100,
            self.configurar_teclado
        )

    def criar_botao(self, texto, linha, coluna):
        destaque = texto == "="

        botao = ctk.CTkButton(
            self.card,
            text=texto,
            width=74,
            height=56,
            corner_radius=10,
            fg_color=AZUL if destaque else BOTAO,
            hover_color=AZUL_HOVER if destaque else HOVER,
            font=("Segoe UI", 17, "bold"),
            command=lambda valor=texto: self.processar_botao(valor)
        )

        botao.grid(
            row=linha,
            column=coluna,
            padx=7,
            pady=7,
            sticky="nsew"
        )

    def configurar_teclado(self):
        if not self.winfo_exists():
            return

        janela = self.winfo_toplevel()
        self._atalho_teclado = janela.bind(
            "<Key>",
            self.processar_tecla,
            add="+"
        )
        self.focus_set()

    def processar_tecla(self, evento):
        tecla = evento.keysym
        caractere = evento.char

        if tecla in ("Return", "KP_Enter", "equal"):
            self.calcular()
            return "break"

        if tecla == "BackSpace":
            self.apagar()
            return "break"

        if tecla == "Escape":
            self.limpar()
            return "break"

        if caractere in "0123456789.+-*/()%":
            self.adicionar(caractere)
            return "break"

        if caractere == ",":
            self.adicionar(".")
            return "break"

        if caractere == "^":
            self.adicionar("**")
            return "break"

        if caractere.lower() == "x":
            self.adicionar("*")
            return "break"

        if caractere.lower() == "r":
            self.adicionar("sqrt(")
            return "break"

        return None

    def processar_botao(self, valor):
        acoes = {
            "C": self.limpar,
            "DEL": self.apagar,
            "=": self.calcular,
            "+/-": self.inverter_sinal,
            "sqrt": lambda: self.adicionar("sqrt("),
            "x2": lambda: self.adicionar("**2"),
            "^": lambda: self.adicionar("**"),
        }

        if valor in acoes:
            acoes[valor]()
            return

        self.adicionar(valor)

    def adicionar(self, valor):
        if valor == "." and self.ultimo_numero_tem_decimal():
            return

        self.expressao += valor
        self.atualizar_display()

    def apagar(self):
        self.expressao = self.expressao[:-1]
        self.atualizar_display()

    def limpar(self):
        self.expressao = ""
        self.status_var.set("Use os botoes ou o teclado")
        self.atualizar_display()

    def inverter_sinal(self):
        if not self.expressao:
            self.expressao = "-"
            self.atualizar_display()
            return

        try:
            resultado = self.avaliar(self.expressao) * -1
            self.expressao = self.formatar_resultado(resultado)

        except (ValueError, ZeroDivisionError, SyntaxError):
            self.expressao = f"-({self.expressao})"

        self.atualizar_display()

    def calcular(self):
        if not self.expressao:
            return

        try:
            resultado = self.avaliar(self.expressao)
            self.expressao = self.formatar_resultado(resultado)
            self.status_var.set("Resultado")
            self.atualizar_display()

        except ZeroDivisionError:
            self.status_var.set("Erro: divisao por zero")

        except (ValueError, SyntaxError):
            self.status_var.set("Expressao invalida")

    def atualizar_display(self):
        texto = self.expressao or "0"
        texto = texto.replace("**", "^")

        self.display_var.set(texto)

    def ultimo_numero_tem_decimal(self):
        ultimo_operador = max(
            self.expressao.rfind("+"),
            self.expressao.rfind("-"),
            self.expressao.rfind("*"),
            self.expressao.rfind("/"),
            self.expressao.rfind("%"),
            self.expressao.rfind("("),
            self.expressao.rfind(")"),
        )
        trecho = self.expressao[ultimo_operador + 1:]

        return "." in trecho

    def avaliar(self, expressao):
        arvore = ast.parse(expressao, mode="eval")

        return self.avaliar_no(arvore)

    def avaliar_no(self, no):
        operadores_binarios = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.Mod: operator.mod,
            ast.Pow: operator.pow,
        }
        operadores_unarios = {
            ast.UAdd: operator.pos,
            ast.USub: operator.neg,
        }
        funcoes = {
            "sqrt": math.sqrt,
            "abs": abs,
        }

        if isinstance(no, ast.Expression):
            return self.avaliar_no(no.body)

        if isinstance(no, ast.Constant) and isinstance(no.value, (int, float)):
            return no.value

        if isinstance(no, ast.BinOp) and type(no.op) in operadores_binarios:
            esquerda = self.avaliar_no(no.left)
            direita = self.avaliar_no(no.right)

            return operadores_binarios[type(no.op)](esquerda, direita)

        if isinstance(no, ast.UnaryOp) and type(no.op) in operadores_unarios:
            return operadores_unarios[type(no.op)](
                self.avaliar_no(no.operand)
            )

        if isinstance(no, ast.Call) and isinstance(no.func, ast.Name):
            nome = no.func.id

            if nome not in funcoes or len(no.args) != 1:
                raise ValueError("Funcao invalida")

            return funcoes[nome](
                self.avaliar_no(no.args[0])
            )

        raise ValueError("Expressao invalida")

    def formatar_resultado(self, valor):
        if isinstance(valor, float) and valor.is_integer():
            return str(int(valor))

        return f"{valor:.10g}"

    def destroy(self):
        if self._atalho_teclado:
            janela = self.winfo_toplevel()
            janela.unbind(
                "<Key>",
                self._atalho_teclado
            )

        super().destroy()
