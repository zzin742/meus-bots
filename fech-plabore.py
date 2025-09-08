import pyautogui
import time

# =========================
# CONFIGURAÇÕES DO BOT
# =========================
empresa_codigo = "4"       # Código da empresa
competencia = "08/2025"    # Competência
usuario = "José"           # Nome do usuário

# =========================
# FUNÇÃO DE EXECUÇÃO
# =========================
def executar_bot():
    # Passo 1: Executar empresa
    print("Executando empresa...")
    pyautogui.moveTo(135, 101)
    
    # Duplo clique separado com sleep
    pyautogui.click()
    time.sleep(1)  # intervalo de 1 segundo
    pyautogui.click()
    time.sleep(1)  # espera antes de digitar

    # Digitar código da empresa
    pyautogui.write(empresa_codigo)
    time.sleep(0.5)
    pyautogui.press('enter')
    
    # Espera extra para garantir que entrou na empresa
    time.sleep(7)  # aumentei de 5 para 7 segundos

    # Passo 2: Aba eSocial
    print("Acessando aba eSocial...")
    pyautogui.moveTo(556, 55)
    pyautogui.click()
    time.sleep(0.5)
    pyautogui.moveTo(556, 144)
    pyautogui.click()
    time.sleep(1)

    # Passo 3: Competência e ticar caixinha
    print("Inserindo competência...")
    pyautogui.write(competencia)
    pyautogui.press('enter')
    pyautogui.press('enter')

    # Passo 4: Ticar opção "Fechamento dos eventos periódicos"
    print("Marcando opção de fechamento...")
    pyautogui.moveTo(515, 585)
    pyautogui.click()
    time.sleep(0.5)

    # Passo 5: Ir na rotina e executar todas empresas
    print("Executando rotina...")
    pyautogui.moveTo(1047, 371)
    pyautogui.click()
    time.sleep(0.5)
    pyautogui.moveTo(716, 638)
    pyautogui.click()
    time.sleep(0.5)
    pyautogui.write(usuario)
    pyautogui.press('enter')
    time.sleep(0.5)

    # Passo 6: Clicar no botão OK
    print("Clicando OK...")
    pyautogui.moveTo(943, 277)
    pyautogui.click()
    print("Processo finalizado!")

# =========================
# EXECUTAR BOT
# =========================
if __name__ == "__main__":
    print("Bot vai iniciar em 5 segundos. Prepare a tela...")
    time.sleep(5)
    executar_bot()
