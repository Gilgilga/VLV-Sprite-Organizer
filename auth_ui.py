import tkinter as tk
from tkinter import messagebox, ttk
from database import UserDB

class LoginRegisterWindow:
    def __init__(self, root, on_success_callback):
        self.root = root
        self.root.title("Acesso - VLV Sprite Organizer")
        self.root.geometry("400x500")
        self.root.configure(bg="#f8f9fa") # Fundo cinza suave tipo moderno
        
        self.db = UserDB()
        self.on_success = on_success_callback
        
        self.show_login = True  # Alterna entre Login e Registro
        self._build_ui()

    def _build_ui(self):
        # Limpa o root se já tiver algo (para alternar entre login/registro)
        for widget in self.root.winfo_children():
            widget.destroy()

        # Frame Central (Card)
        card = tk.Frame(self.root, bg="white", padx=30, pady=30, highlightbackground="#e0e0e0", highlightthickness=1)
        card.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=340, height=420)

        # Título
        title_text = "Login" if self.show_login else "Criar Conta"
        tk.Label(card, text=title_text, font=("Segoe UI", 18, "bold"), bg="white", fg="#333").pack(pady=(0, 20))

        # Campos
        tk.Label(card, text="Usuário", font=("Segoe UI", 10), bg="white", fg="#666").pack(anchor="w")
        self.entry_user = tk.Entry(card, font=("Segoe UI", 11), bg="#f1f3f5", bd=0, insertbackground="black")
        self.entry_user.pack(fill=tk.X, pady=(5, 15), ipady=8)
        
        # Simula borda no entry
        # self.entry_user.config(highlightbackground="#dee2e6", highlightthickness=1)

        tk.Label(card, text="Senha", font=("Segoe UI", 10), bg="white", fg="#666").pack(anchor="w")
        self.entry_pass = tk.Entry(card, font=("Segoe UI", 11), bg="#f1f3f5", bd=0, show="*", insertbackground="black")
        self.entry_pass.pack(fill=tk.X, pady=(5, 20), ipady=8)

        # Botão Principal (Estilo Inspirado)
        btn_text = "Entrar" if self.show_login else "Cadastrar"
        btn_cmd = self._handle_login if self.show_login else self._handle_register
        
        # Cor verde baseada na inspiração (#7dc29a ou similar)
        main_btn = tk.Button(
            card, text=btn_text, font=("Segoe UI", 11, "bold"), 
            bg="#7dc29a", fg="white", activebackground="#6ab289", 
            activeforeground="white", bd=0, cursor="hand2",
            command=btn_cmd
        )
        main_btn.pack(fill=tk.X, ipady=10, pady=(10, 5))

        # Link de troca
        toggle_text = "Não tem conta? Registre-se" if self.show_login else "Já tem conta? Faça Login"
        toggle_btn = tk.Button(
            card, text=toggle_text, font=("Segoe UI", 9), 
            bg="white", fg="#007bff", bd=0, cursor="hand2",
            activebackground="white", activeforeground="#0056b3",
            command=self._toggle_mode
        )
        toggle_btn.pack(pady=10)

    def _toggle_mode(self):
        self.show_login = not self.show_login
        self._build_ui()

    def _handle_login(self):
        user = self.entry_user.get()
        pwd = self.entry_pass.get()
        
        if not user or not pwd:
            messagebox.showwarning("Aviso", "Preencha todos os campos.")
            return
            
        user_data = self.db.authenticate_user(user, pwd)
        if user_data:
            self.on_success(user_data)
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos.")

    def _handle_register(self):
        user = self.entry_user.get()
        pwd = self.entry_pass.get()
        
        if not user or not pwd:
            messagebox.showwarning("Aviso", "Preencha todos os campos.")
            return
            
        success, msg = self.db.register_user(user, pwd)
        if success:
            messagebox.showinfo("Sucesso", msg)
            self.show_login = True
            self._build_ui()
        else:
            messagebox.showerror("Erro", msg)

if __name__ == "__main__":
    def login_success(user):
        print(f"Sucesso: {user}")
        root.destroy()

    root = tk.Tk()
    app = LoginRegisterWindow(root, login_success)
    root.mainloop()
