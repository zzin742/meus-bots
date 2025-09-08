import subprocess
import threading
import os
import signal
import customtkinter as ctk
from datetime import datetime

class BotController:
    def __init__(self):
        # Dicionário de bots atualizado
        self.BOTS = {
            "Abrir Onvio": "abreonvio.py",
            "Remuneração Pró-Labore": "rm-pg-plabore.py",
            "Fechamento Pró-Labore": "fech-plabore.py",
        }
        
        # Dicionários para controle
        self.processos = {}
        self.status_bots = {}
        self.threads = {}
        
        # Configuração da interface
        self.setup_ui()
        
    def setup_ui(self):
        # Configuração de aparência
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Janela principal
        self.janela = ctk.CTk()
        self.janela.title("Painel de Controle dos Bots")
        self.janela.geometry("800x600")
        self.janela.grid_rowconfigure(0, weight=1)
        self.janela.grid_columnconfigure(1, weight=1)
        
        # Menu lateral
        self.menu_frame = ctk.CTkFrame(self.janela, width=200, corner_radius=0)
        self.menu_frame.grid(row=0, column=0, sticky="nswe")
        
        menu_label = ctk.CTkLabel(self.menu_frame, text="Menu", font=("Arial", 18, "bold"))
        menu_label.pack(pady=20)
        
        # Frame de conteúdo
        self.conteudo_frame = ctk.CTkFrame(self.janela, corner_radius=10)
        self.conteudo_frame.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)
        
        # Inicializa variáveis da interface
        self.log_text = None
        self.status_label = None
        self.bot_atual = None
        
        # Cria os componentes do menu
        self.criar_menu()
        
        # Mostra tela inicial
        self.mostrar_inicio()
        
    def criar_menu(self):
        # Botão de início
        btn_inicio = ctk.CTkButton(
            self.menu_frame, 
            text="🏠 Início", 
            width=180,
            command=self.mostrar_inicio
        )
        btn_inicio.pack(pady=5, padx=10, fill="x")
        
        # Separador
        separador = ctk.CTkFrame(self.menu_frame, height=2, fg_color="gray")
        separador.pack(pady=10, padx=10, fill="x")
        
        # Botões e indicadores para os bots
        for nome, arquivo in self.BOTS.items():
            # Frame do botão + status
            frame_bot = ctk.CTkFrame(self.menu_frame, corner_radius=10, fg_color="transparent")
            frame_bot.pack(pady=5, fill="x", padx=10)
            
            # Botão do bot
            btn = ctk.CTkButton(
                frame_bot, 
                text=nome, 
                width=150,
                command=lambda n=nome, a=arquivo: self.executar_bot(n, a)
            )
            btn.pack(side="left", padx=(0, 5))
            
            # Indicador de status
            indicador = ctk.CTkLabel(
                frame_bot, 
                text="", 
                width=20, 
                height=20, 
                fg_color="red", 
                corner_radius=10
            )
            indicador.pack(side="left")
            
            # Armazena referência ao indicador
            self.status_bots[nome] = indicador
    
    def atualizar_log(self, linha, tipo="info"):
        if not self.log_text:
            return
            
        self.log_text.configure(state="normal")
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        if tipo == "info":
            self.log_text.insert("end", f"[{timestamp}] ℹ️ {linha}\n", "info")
        elif tipo == "success":
            self.log_text.insert("end", f"[{timestamp}] ✅ {linha}\n", "success")
        elif tipo == "error":
            self.log_text.insert("end", f"[{timestamp}] ❌ {linha}\n", "error")
        elif tipo == "warning":
            self.log_text.insert("end", f"[{timestamp}] ⚠️ {linha}\n", "warning")
            
        self.log_text.see("end")
        self.log_text.configure(state="disabled")
    
    def atualizar_status(self, nome, cor):
        if nome in self.status_bots:
            self.status_bots[nome].configure(fg_color=cor)
    
    def executar_bot(self, nome, arquivo):
        # Verifica se o arquivo existe
        if not os.path.exists(arquivo):
            self.mostrar_erro(f"Arquivo {arquivo} não encontrado!")
            return
            
        # Se o bot já está em execução, pergunta se quer reiniciar
        if nome in self.processos and self.processos[nome] and self.processos[nome].poll() is None:
            if not self.confirmar_reinicio(nome):
                return
            else:
                self.parar_bot(nome)
        
        # Limpa a área de conteúdo
        for widget in self.conteudo_frame.winfo_children():
            widget.destroy()
        
        self.bot_atual = nome
        
        # Título
        titulo = ctk.CTkLabel(
            self.conteudo_frame, 
            text=f"Controle - {nome}", 
            font=("Arial", 20, "bold")
        )
        titulo.pack(pady=10)
        
        # Frame para botões de controle
        controle_frame = ctk.CTkFrame(self.conteudo_frame, fg_color="transparent")
        controle_frame.pack(pady=5, fill="x", padx=10)
        
        # Botão para parar o bot
        btn_parar = ctk.CTkButton(
            controle_frame,
            text="⏹️ Parar Bot",
            width=120,
            command=lambda: self.parar_bot(nome),
            fg_color="#d32f2f"
        )
        btn_parar.pack(side="left", padx=5)
        
        # Botão para limpar logs
        btn_limpar = ctk.CTkButton(
            controle_frame,
            text="🧹 Limpar Logs",
            width=120,
            command=self.limpar_logs
        )
        btn_limpar.pack(side="left", padx=5)
        
        # Área de logs
        self.log_text = ctk.CTkTextbox(
            self.conteudo_frame, 
            width=700, 
            height=300, 
            state="disabled",
            fg_color="#1e1e1e", 
            text_color="white", 
            corner_radius=8,
            wrap="word"
        )
        self.log_text.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Configuração de cores para diferentes tipos de mensagem
        self.log_text.tag_config("info", foreground="lightblue")
        self.log_text.tag_config("success", foreground="lightgreen")
        self.log_text.tag_config("error", foreground="#ff6b6b")
        self.log_text.tag_config("warning", foreground="yellow")
        
        # Status
        self.status_label = ctk.CTkLabel(
            self.conteudo_frame, 
            text="Iniciando...", 
            font=("Arial", 14)
        )
        self.status_label.pack(pady=5)
        
        # Função para executar o bot em uma thread separada
        def run():
            try:
                self.atualizar_status(nome, "green")  # Bot rodando
                self.status_label.configure(text=f"{nome} em execução...")
                self.atualizar_log(f"Iniciando execução do bot {nome}", "info")
                
                # Inicia o processo
                self.processos[nome] = subprocess.Popen(
                    ["python", arquivo],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0
                )
                
                # Lê a saída do processo
                for linha in iter(self.processos[nome].stdout.readline, ''):
                    linha = linha.strip()
                    if not linha:
                        continue
                        
                    # Classifica a mensagem
                    if any(palavra in linha.lower() for palavra in ["erro", "error", "falha", "exception", "traceback"]):
                        self.atualizar_log(linha, "error")
                    elif any(palavra in linha.lower() for palavra in ["concluído", "sucesso", "finalizado", "completed"]):
                        self.atualizar_log(linha, "success")
                    elif any(palavra in linha.lower() for palavra in ["aviso", "warning", "atenção"]):
                        self.atualizar_log(linha, "warning")
                    else:
                        self.atualizar_log(linha, "info")
                
                # Verifica o código de saída
                codigo_saida = self.processos[nome].poll()
                if codigo_saida == 0:
                    self.atualizar_log(f"Bot {nome} finalizado com sucesso", "success")
                else:
                    self.atualizar_log(f"Bot {nome} finalizado com código de erro: {codigo_saida}", "error")
                
                self.atualizar_status(nome, "red")  # Bot parado
                self.status_label.configure(text=f"{nome} finalizado")
                
            except Exception as e:
                self.atualizar_log(f"Erro ao executar bot: {str(e)}", "error")
                self.atualizar_status(nome, "red")
                self.status_label.configure(text=f"{nome} com erros")
        
        # Inicia a thread
        self.threads[nome] = threading.Thread(target=run, daemon=True)
        self.threads[nome].start()
    
    def parar_bot(self, nome):
        if nome in self.processos and self.processos[nome]:
            try:
                if os.name == 'nt':  # Windows
                    self.processos[nome].send_signal(signal.CTRL_BREAK_EVENT)
                else:  # Linux/Mac
                    self.processos[nome].send_signal(signal.SIGINT)
                
                self.atualizar_log(f"Solicitação de parada enviada para {nome}", "warning")
                self.status_label.configure(text=f"Parando {nome}...")
                
                # Espera um pouco para o processo terminar
                self.processos[nome].wait(timeout=5)
                self.atualizar_log(f"Bot {nome} parado com sucesso", "success")
                self.atualizar_status(nome, "red")
                self.status_label.configure(text=f"{nome} parado")
                
            except subprocess.TimeoutExpired:
                self.atualizar_log(f"Timeout ao parar bot {nome}, forçando término", "error")
                self.processos[nome].kill()
                self.atualizar_status(nome, "red")
                self.status_label.configure(text=f"{nome} forçado a parar")
                
            except Exception as e:
                self.atualizar_log(f"Erro ao parar bot: {str(e)}", "error")
    
    def limpar_logs(self):
        if self.log_text:
            self.log_text.configure(state="normal")
            self.log_text.delete("1.0", "end")
            self.log_text.configure(state="disabled")
            self.atualizar_log("Logs limpos", "info")
    
    def confirmar_reinicio(self, nome):
        # Cria uma janela de confirmação
        dialog = ctk.CTkToplevel(self.janela)
        dialog.title("Confirmação")
        dialog.geometry("400x150")
        dialog.transient(self.janela)
        dialog.grab_set()
        
        # Centraliza a janela
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
        
        # Mensagem
        msg = ctk.CTkLabel(
            dialog,
            text=f"O bot {nome} já está em execução.\nDeseja reiniciá-lo?",
            font=("Arial", 12),
            justify="center"
        )
        msg.pack(pady=20)
        
        # Frame para botões
        btn_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        btn_frame.pack(pady=10)
        
        # Variável para armazenar a resposta
        resposta = [False]
        
        # Função para confirmar
        def confirmar():
            resposta[0] = True
            dialog.destroy()
        
        # Botões
        btn_sim = ctk.CTkButton(
            btn_frame,
            text="Sim",
            width=80,
            command=confirmar
        )
        btn_sim.pack(side="left", padx=10)
        
        btn_nao = ctk.CTkButton(
            btn_frame,
            text="Não",
            width=80,
            command=dialog.destroy
        )
        btn_nao.pack(side="left", padx=10)
        
        # Espera a janela fechar
        self.janela.wait_window(dialog)
        return resposta[0]
    
    def mostrar_inicio(self):
        # Limpa a área de conteúdo
        for widget in self.conteudo_frame.winfo_children():
            widget.destroy()
        
        # Título
        titulo = ctk.CTkLabel(
            self.conteudo_frame,
            text="Painel de Controle dos Bots",
            font=("Arial", 24, "bold")
        )
        titulo.pack(pady=20)
        
        # Mensagem de boas-vindas
        welcome_label = ctk.CTkLabel(
            self.conteudo_frame,
            text="👋 Bem-vindo ao Painel de Controle!\n\nSelecione um bot no menu à esquerda para começar.",
            font=("Arial", 16),
            justify="center"
        )
        welcome_label.pack(expand=True)
        
        # Status dos bots
        status_frame = ctk.CTkFrame(self.conteudo_frame, fg_color="transparent")
        status_frame.pack(pady=20, fill="x")
        
        status_titulo = ctk.CTkLabel(
            status_frame,
            text="Status dos Bots:",
            font=("Arial", 14, "bold")
        )
        status_titulo.pack(pady=5)
        
        for nome in self.BOTS:
            bot_status = ctk.CTkFrame(status_frame, fg_color="transparent")
            bot_status.pack(fill="x", pady=2)
            
            # Nome do bot
            nome_label = ctk.CTkLabel(
                bot_status,
                text=nome,
                font=("Arial", 12),
                width=200,
                anchor="w"
            )
            nome_label.pack(side="left", padx=10)
            
            # Indicador de status
            indicador = ctk.CTkLabel(
                bot_status, 
                text="", 
                width=15, 
                height=15, 
                fg_color="red", 
                corner_radius=7
            )
            indicador.pack(side="left", padx=5)
            
            # Texto de status
            status_text = "Parado"
            if nome in self.processos and self.processos[nome] and self.processos[nome].poll() is None:
                status_text = "Em execução"
                indicador.configure(fg_color="green")
            
            texto_status = ctk.CTkLabel(
                bot_status,
                text=status_text,
                font=("Arial", 12)
            )
            texto_status.pack(side="left", padx=5)
    
    def mostrar_erro(self, mensagem):
        # Limpa a área de conteúdo
        for widget in self.conteudo_frame.winfo_children():
            widget.destroy()
        
        # Título
        titulo = ctk.CTkLabel(
            self.conteudo_frame,
            text="❌ Erro",
            font=("Arial", 24, "bold"),
            text_color="#ff6b6b"
        )
        titulo.pack(pady=20)
        
        # Mensagem de erro
        erro_label = ctk.CTkLabel(
            self.conteudo_frame,
            text=mensagem,
            font=("Arial", 14),
            justify="center"
        )
        erro_label.pack(expand=True)
        
        # Botão para voltar
        btn_voltar = ctk.CTkButton(
            self.conteudo_frame,
            text="Voltar ao Início",
            command=self.mostrar_inicio
        )
        btn_voltar.pack(pady=20)
    
    def run(self):
        self.janela.mainloop()

# Inicia a aplicação
if __name__ == "__main__":
    app = BotController()
    app.run()