# Sistema de Automação em Python

Aplicativo desktop feito em Python com CustomTkinter. O sistema possui tela de login, menu lateral e modulos para calculadora, cambio, planilha Excel e envio de e-mail.

## Funcionalidades

- Login simples com usuario e senha padrão.
- Menu lateral com acesso aos modulos e botao discreto para voltar ao login.
- Calculadora com visual de aplicativo, display, botões de operacao e suporte ao teclado.
- Consulta de cambio com conversor entre moedas, cards de destaque e tabela comparativa.
- Edição de planilha Excel com adicionar, alterar, remover, aplicar percentual e salvar.
- Envio de e-mail com multiplos destinatarios, CC, CCO e anexos.

## Login Padrão

Use as credenciais abaixo para acessar o menu principal:

```text
Usuario: admin
Senha: 1234
```

As credenciais ficam definidas no codigo, no arquivo `TDE/login.py`.

## Como Executar

1. Instale as dependencias:

```bash
pip install customtkinter requests openpyxl
```

2. Execute o aplicativo:

```bash
python TDE/main.py
```

Se o comando `python` não estiver disponivel no Windows, tente:

```bash
py TDE/main.py
```

## Modulos

### Calculadora

A calculadora aceita cliques nos botões e entrada pelo teclado fisico.

Teclas uteis:

- `Enter`: calcular
- `Backspace`: apagar
- `Esc`: limpar
- `+`, `-`, `*`, `/`, `%`, `(`, `)`: operadores
- `^`: potencia
- `r`: raiz quadrada
- `,` ou `.`: decimal

### Câmbio

O módulo de câmbio consulta cotações pela API AwesomeAPI e permite converter valores entre:

- BRL
- USD
- EUR
- GBP
- ARS
- CAD
- AUD
- CHF
- JPY
- CNY
- BTC

A tela também mostra cards de destaque e uma tabela com compra, venda, variação e minimo/maximo do dia.

### Excel

O módulo de Excel trabalha com arquivos `.xlsx`.

A planilha deve usar as colunas:

| Produto | Preco |
| --- | --- |
| Mouse | 50 |
| Teclado | 120 |
| Monitor | 900 |

Na interface é possivel:

- Criar uma nova planilha.
- Selecionar uma planilha existente.
- Adicionar produtos.
- Editar produtos e precos diretamente na tabela.
- Remover linhas.
- Aumentar ou diminuir precos por percentual.
- Salvar no arquivo atual ou salvar como outro arquivo.

O projeto ja possui uma planilha de exemplo em `Arquivos/precos.xlsx`.

### Envio de E-mail

O modulo de e-mail permite preencher destinatarios, CC, CCO, assunto, mensagem e anexos. Também é possivel anexar a planilha padrão `Arquivos/precos.xlsx` direto pela interface.

Recursos disponiveis:

- Múltiplos destinatarios separados por virgula ou ponto e virgula.
- Campos de CC e CCO.
- Seleção de varios anexos.
- Remoção individual de anexos.
- Botão para limpar o formulario.
- Envio com `Ctrl + Enter`.
- Envio em segundo plano para evitar travar a interface.

O app não deixa a senha do e-mail salva no codigo. Antes de usar o envio, configure as variáveis de ambiente.

No PowerShell:

```powershell
$env:EMAIL_REMETENTE="seu_email@gmail.com"
$env:SENHA_EMAIL="sua_senha_de_aplicativo"
python TDE/main.py
```

Para Gmail, use uma senha de aplicativo gerada na conta Google.

## Estrutura do Projeto

```text
TDE PY/
+-- Arquivos/
|   +-- precos.xlsx
+-- TDE/
|   +-- main.py
|   +-- login.py
|   +-- menu.py
|   +-- calculadora.py
|   +-- cambio.py
|   +-- excel_precos.py
|   +-- email_auto.py
+-- .gitignore
+-- README.md
```

## Arquivos de Cache

Pastas como `__pycache__` e arquivos `.pyc` saã gerados automaticamente pelo Python. Eles não sao necessários para manter no projeto e podem ser apagados com seguranca.

O `.gitignore` do projeto ignora esses arquivos para manter a pasta mais limpa.

## Bibliotecas Usadas

- customtkinter
- requests
- openpyxl
- smtplib
- email.message
- mimetypes
- threading
- datetime
- tkinter.filedialog
