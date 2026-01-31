# Desktop Control Skill

🤖 **AI Agent Skill** for desktop automation using PyAutoGUI.

Control mouse, keyboard, and screen programmatically through a simple CLI interface.

---

## 🎯 For AI Agents

This project is packaged as an **AI Agent Skill**. To use it:

1. **Read the skill documentation**: [SKILL.md](SKILL.md)
2. **Install the skill**: Run `python scripts/install.py`
3. **Invoke commands**: Use `python main.py <category> <command>`

**Quick Reference for Agents:**
- All commands documented in [SKILL.md](SKILL.md)
- Practical examples in [examples/automation_examples.md](examples/automation_examples.md)
- Help system: `python main.py --help`

---

## 📦 Installation

### Quick Install (Recommended)

```bash
# Clone or download this repository
cd desktop-skill

# Run installation script
python scripts/install.py
```

### Manual Install


## Uso

A CLI está organizada em categorias de comandos:

### 🖱️ Mouse (`mouse`)

```bash
# Mover mouse para coordenadas
python main.py mouse move 100 200

# Mover com duração (animação)
python main.py mouse move 100 200 --duration 1.0

# Clicar na posição atual
python main.py mouse click

# Clicar em coordenadas específicas
python main.py mouse click 500 500

# Clique direito
python main.py mouse right-click

# Duplo clique
python main.py mouse double-click 300 400

# Arrastar para coordenadas
python main.py mouse drag 200 300

# Rolar tela (positivo = cima, negativo = baixo)
python main.py mouse scroll 5
python main.py mouse scroll -3

# Obter posição atual do mouse
python main.py mouse position
```

### ⌨️ Teclado (`keyboard`)

```bash
# Escrever texto
python main.py keyboard write "Hello World"

# Escrever com intervalo entre teclas
python main.py keyboard write "Slow typing" --interval 0.1

# Pressionar uma tecla
python main.py keyboard press enter

# Pressionar múltiplas vezes
python main.py keyboard press a --presses 5

# Executar atalho de teclado
python main.py keyboard hotkey "ctrl,c"
python main.py keyboard hotkey "ctrl,shift,esc"

# Segurar/soltar tecla
python main.py keyboard keydown shift
python main.py keyboard keyup shift
```

### 🖼️ Tela (`screen`)

```bash
# Capturar screenshot
python main.py screen screenshot minha_tela.png

# Screenshot de região específica (x,y,largura,altura)
python main.py screen screenshot regiao.png --region "100,100,500,400"

# Localizar imagem na tela
python main.py screen locate imagem.png

# Localizar centro da imagem
python main.py screen locate-center botao.png --confidence 0.8

# Obter cor de um pixel
python main.py screen pixel 100 200

# Obter tamanho da tela
python main.py screen size

# Verificar se coordenadas estão na tela
python main.py screen on-screen 5000 5000
```

### 💬 Mensagens (`message`)

```bash
# Mostrar alerta
python main.py message alert "Olá!"

# Confirmação
python main.py message confirm "Você tem certeza?"

# Prompt de entrada
python main.py message prompt "Digite seu nome:"

# Senha
python main.py message password "Digite sua senha:"
```

## Exemplos de Automação

### Abrir Notepad e escrever

```bash
python main.py keyboard hotkey "win,r"
python main.py keyboard write "notepad"
python main.py keyboard press enter
# Aguardar notepad abrir...
python main.py keyboard write "Olá do Desktop Skill!"
```

### Capturar screenshot e analisar

```bash
python main.py screen screenshot tela_completa.png
python main.py screen pixel 500 500
```

## Comandos Disponíveis

Execute `python main.py --help` para ver todos os comandos:

```bash
python main.py --help
python main.py mouse --help
python main.py keyboard --help
python main.py screen --help
python main.py message --help
```

## Estrutura do Projeto

```
desktop-skill/
├── main.py              # Entry point da CLI
├── commands/            # Módulos de comandos
│   ├── __init__.py
│   ├── mouse.py        # Comandos de mouse
│   ├── keyboard.py     # Comandos de teclado
│   ├── screen.py       # Comandos de tela/screenshot
│   └── message.py      # Caixas de mensagem
├── pyproject.toml      # Configuração do projeto
└── README.md           # Esta documentação
```

## Tecnologias

- **PyAutoGUI**: Automação de GUI
- **Typer**: Framework CLI moderno
