import customtkinter as ctk
import socket
import threading

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = "10.111.9.169"
port = 3030
addr = (ip, port)
s.bind(addr)
s.listen(10)

class ChatCliente(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Nexo")
        self.geometry("500x500")

        self.chat_box = ctk.CTkTextbox(self, width=480, height=400, corner_radius=10)
        self.chat_box.pack(padx=10, pady=(10, 5))
        self.chat_box.configure(state="disabled")

        self.entry = ctk.CTkEntry(self, placeholder_text="Digite sua mensagem...", width=400)
        self.entry.pack(side="left", padx=(10, 0), pady=10)
        self.entry.bind("<Return>", self.enviar_mensagem)

        self.send_button = ctk.CTkButton(self, text="Enviar", command=self.enviar_mensagem)
        self.send_button.pack(side="left", padx=10, pady=10)

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect((ip, port))
            threading.Thread(target=self.receber_mensagens, daemon=True).start()
        except Exception as e:
            self.adicionar_mensagem(f"[Erro ao conectar]: {e}")

    def enviar_mensagem(self, event=None):
        msg = self.entry.get().strip()
        if msg:
            try:
                self.sock.send(msg.encode())
                self.adicionar_mensagem(f"[Você]: {msg}")
                self.entry.delete(0, "end")
            except:
                self.adicionar_mensagem("[Erro ao enviar mensagem]")

    def receber_mensagens(self):
        while True:
            try:
                msg = self.sock.recv(1024).decode()
                self.adicionar_mensagem(msg)
            except:
                self.adicionar_mensagem("[Desconectado do servidor]")
                break

    def adicionar_mensagem(self, mensagem):
        self.chat_box.configure(state="normal")
        self.chat_box.insert("end", f"{mensagem}\n")
        self.chat_box.configure(state="disabled")
        self.chat_box.see("end")

if __name__ == "__main__":
    app = ChatCliente()
    app.mainloop()