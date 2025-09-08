import pyautogui
import pyperclip
import time

# -------------------------------
# CONFIGURAÇÕES INICIAIS
# -------------------------------
x_dominio = 437
y_dominio = 884
senha = "jose1234"       # senha do Domínio

# -------------------------------
# Coloque a competência para ele escrever aqui:
competencia = "09/2025"     # <--- altere para a competência desejada

# -------------------------------
# 1️⃣ Abrir Domínio e logar
# -------------------------------
time.sleep(3)
pyautogui.click(x=x_dominio, y=y_dominio)
print("Clicou no Domínio na barra de tarefas")
time.sleep(5)

pyperclip.copy(senha)
pyautogui.hotkey('ctrl', 'v')
pyautogui.press('enter')
print("Senha colada e enter pressionado")
time.sleep(25)

# -------------------------------
# 2️⃣ Entrar na empresa 4
# -------------------------------
pyautogui.click(x=135, y=89, clicks=2, interval=3)
time.sleep(10)
pyautogui.write('4')
time.sleep(10)
pyautogui.press('enter')
print("Selecionou empresa 4")
time.sleep(8)

# -------------------------------
# 3️⃣ Ações internas na empresa 4
# -------------------------------
pyautogui.click(x=555, y=47)
pyautogui.press('enter')
time.sleep(2)

# Campo de competência
pyautogui.click(x=579, y=145)     # garante que o campo esteja ativo
pyautogui.hotkey('ctrl', 'a')     # seleciona tudo
pyautogui.press('backspace')      # apaga o conteúdo antigo
time.sleep(1)
pyautogui.write(competencia)      # ⬅️ escreve a competência definida acima
time.sleep(2)
pyautogui.press('enter')
time.sleep(2)

# -------------------------------
# 4️⃣ Ticar opções
# -------------------------------
pyautogui.click(x=513, y=384)
pyautogui.press('enter')
time.sleep(2)

pyautogui.click(x=512, y=435)
pyautogui.press('enter')
time.sleep(2)

print("Opções ticadas ✅")

# -------------------------------
# 5️⃣ Acessar aba empresas
# -------------------------------
pyautogui.click(x=1056, y=368)
pyautogui.press('enter')
time.sleep(3)

# -------------------------------
# 6️⃣ Seleção e filtrar empresas
# -------------------------------
pyautogui.click(x=705, y=645)
pyautogui.press('enter')
time.sleep(2)

pyautogui.write('José')
time.sleep(2)
pyautogui.press('enter')

print("✅ Empresas filtradas")

# -------------------------------
# 7️⃣ Fechar aba antes de enviar
# -------------------------------
pyautogui.click(x=967, y=249)  # fecha a aba
print("❌ Aba fechada")
time.sleep(3)

# -------------------------------
# 8️⃣ Enviar todos
# -------------------------------
pyautogui.click(x=1050, y=310)  # botão Enviar todos
time.sleep(1)
pyautogui.click(x=1050, y=310)  # segundo clique
print("📤 Envio iniciado...")
time.sleep(1)  # aguarda 5 minutos carregando envios

# -------------------------------
# 9️⃣ Aviso de sucesso
# -------------------------------
pyautogui.click(x=901, y=505)   # botão OK
print("✅ Aviso fechado")
time.sleep(60)

# -------------------------------
# 🔟 Painel de pendências
# -------------------------------
pyautogui.click(x=901, y=505)
print("📌 Painel de pendências aberto")
time.sleep(5)

# -------------------------------
# 1️⃣1️⃣ Em processamento
# -------------------------------
pyautogui.click(x=796, y=185)
print("⚙️ Em processamento selecionado")

print("🚀 Bot do Domínio finalizado com sucesso!")
