import webbrowser
import time
import os
import subprocess
import pyautogui
import pyperclip

# -------------------------------
# 1️⃣ Abrir abas do Chrome
# -------------------------------
sites = [
    "https://github.com/zzin742",
    "https://github.com/zzin742",
    "https://github.com/zzin742",
    "https://github.com/zzin742"
]

caminhos = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
]

chrome_path = None
for caminho in caminhos:
    if os.path.exists(caminho):
        chrome_path = caminho
        break

if chrome_path:
    webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))
    for site in sites:
        webbrowser.get('chrome').open_new_tab(site)
        time.sleep(2)
else:
    print("⚠️ Não encontrei o Chrome. Verifique o caminho do executável.")

# -------------------------------
# 2️⃣ Abrir planilha Excel
# -------------------------------
nome_planilha = "JOSÉÉÉÉ 01.20251.xlsx"
caminho_planilha = os.path.join(os.getcwd(), nome_planilha)

if os.path.exists(caminho_planilha):
    subprocess.Popen(['start', '', caminho_planilha], shell=True)
    time.sleep(2)  # Espera o Excel abrir
else:
    print(f"⚠️ Não encontrei a planilha {nome_planilha}. Verifique o nome e a extensão.")

# -------------------------------
# 3️⃣ Abrir app da barra de tarefas e digitar senha
# -------------------------------
x_app = 432  # coordenada X do ícone do app na barra de tarefas
y_app = 877  # coordenada Y do ícone do app na barra de tarefas
senha = "ZEZINHO2301"  # substitua pela sua senha real

time.sleep(3)  # Dá tempo de colocar foco na tela principal
pyautogui.click(x=x_app, y=y_app)
time.sleep(5)  # Espera o app abrir

# Digitar a senha com área de transferência (mais confiável)
pyperclip.copy(senha)
pyautogui.hotkey('ctrl', 'v')
pyautogui.press('enter')

print("✅ Todas as tarefas concluídas!")
