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
        self.is_dark_mode = False
        self._build_ui()

    def _build_ui(self):
        # Limpa o root se já tiver algo (para alternar entre login/registro)
        for widget in self.root.winfo_children():
            widget.destroy()

        # Botão de Tema no topo
        bg_root = "#1e1e2e" if self.is_dark_mode else "#f8f9fa"
        fg_btn = "#f8f8f2" if self.is_dark_mode else "#333"
        btn_text = "Modo Claro" if self.is_dark_mode else "Modo Escuro"
        
        self.btn_theme = tk.Button(self.root, text=btn_text, font=("Segoe UI", 9), bg=bg_root, fg=fg_btn, bd=0, cursor="hand2", command=self.toggle_theme)
        self.btn_theme.place(relx=0.95, rely=0.05, anchor=tk.NE)

        # Frame Central (Card)
        card = tk.Frame(self.root, bg="white", padx=30, pady=30, highlightbackground="#e0e0e0", highlightthickness=1)
        card.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=340, height=420)

        # Título
        title_text = "Login" if self.show_login else "Criar Conta"
        tk.Label(card, text=title_text, font=("Segoe UI", 18, "bold"), bg="white", fg="#333").pack(pady=(0, 20))

        # Campos
        tk.Label(card, text="Usuário", font=("Segoe UI", 10), bg="white", fg="#666").pack(anchor="w")
        
        if self.show_login:
            users = self.db.get_all_users()
            self.entry_user = ttk.Combobox(card, values=users, font=("Segoe UI", 11), state="readonly")
            if users:
                self.entry_user.current(0)
            self.entry_user.pack(fill=tk.X, pady=(5, 15))
        else:
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
        if self.is_dark_mode:
            self.apply_theme(True)

    def apply_theme(self, to_dark):
        color_map = {
            "#f8f9fa": "#1e1e2e", "white": "#282a36", "#ffffff": "#282a36",
            "#333": "#f8f8f2", "#333333": "#f8f8f2", "#666": "#bfbfbf", "#666666": "#bfbfbf",
            "#e0e0e0": "#44475a", "#f1f3f5": "#44475a", "black": "white", "#007bff": "#66b2ff", "#0056b3": "#99ccff"
        }
        if not to_dark:
            color_map = {"#1e1e2e": "#f8f9fa", "#282a36": "white", "#f8f8f2": "#333", "#bfbfbf": "#666",
                         "#44475a": "#f1f3f5", "white": "black", "#66b2ff": "#007bff", "#99ccff": "#0056b3"}

        def update_widget(w):
            try:
                keys = w.keys()
                if "bg" in keys and w.cget("bg") in color_map:
                    w.configure(bg=color_map[w.cget("bg")])
                if "fg" in keys and w.cget("fg") in color_map:
                    w.configure(fg=color_map[w.cget("fg")])
                if "insertbackground" in keys and w.cget("insertbackground") in color_map:
                    w.configure(insertbackground=color_map[w.cget("insertbackground")])
                if "highlightbackground" in keys and w.cget("highlightbackground") in color_map:
                    w.configure(highlightbackground=color_map[w.cget("highlightbackground")])
                if "activebackground" in keys and w.cget("activebackground") in color_map:
                    w.configure(activebackground=color_map[w.cget("activebackground")])
                if "activeforeground" in keys and w.cget("activeforeground") in color_map:
                    w.configure(activeforeground=color_map[w.cget("activeforeground")])
            except: pass
            for child in w.winfo_children(): update_widget(child)

        update_widget(self.root)

    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        self.apply_theme(self.is_dark_mode)
        if self.is_dark_mode:
            self.btn_theme.config(text="Modo Claro", bg="#1e1e2e", fg="#f8f8f2")
        else:
            self.btn_theme.config(text="Modo Escuro", bg="#f8f9fa", fg="#333")

    def _handle_login(self):
        user = self.entry_user.get()
        pwd = self.entry_pass.get()
        
        if not user or not pwd:
            messagebox.showwarning("Aviso", "Preencha todos os campos.")
            return
            
        user_data = self.db.authenticate_user(user, pwd)
        if user_data:
            user_data['is_dark_mode'] = self.is_dark_mode
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
