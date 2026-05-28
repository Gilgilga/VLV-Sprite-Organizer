import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk, ImageSequence
from spritesheet import SpriteSheet
from animation import AnimationPlayer
from project_manager import ProjectManager
from utils import scale_image
from database import UserDB
from auth_ui import LoginRegisterWindow

class SpriteApp:
    def __init__(self, root, user_data):
        self.root = root
        self.user_data = user_data
        self.db = UserDB()
        
        self.root.title("VLV Sprite Organizer")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f8f9fa")

        # Gerenciador de Projeto
        self.project_manager = ProjectManager(workspace_dir="workspace")

        # Estado da Aplicação
        self.sprite_sheet = None
        self.animation_player = AnimationPlayer([])
        self.frames_pil = []
        self.current_tk_image = None
        self.scale_factor = 2.0  # Fator de Zoom para o preview

        self._apply_styles()
        self._build_gui()

        # Inicia o loop de renderização da animação
        self.update_canvas()
        
        self.log_event(f"App Iniciado por {self.user_data['username']}")
        
        self.is_dark_mode = self.user_data.get('is_dark_mode', False)
        if self.is_dark_mode:
            self.is_dark_mode = False
            self.toggle_theme()

    def _apply_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Estilo para os LabelFrames (Cards)
        style.configure("Card.TLabelframe", background="white", relief="flat", borderwidth=1)
        style.configure("Card.TLabelframe.Label", background="white", font=("Segoe UI", 10, "bold"), foreground="#333")
        
        # Botões Modernos
        style.configure("Primary.TButton", font=("Segoe UI", 10, "bold"), background="#7dc29a", foreground="white")
        style.map("Primary.TButton", background=[('active', '#6ab289')])

    def log_event(self, action):
        """Registra ação no banco de dados."""
        self.db.log_action(self.user_data['id'], action)

    def _build_gui(self):
        # Header (Top Bar)
        header = tk.Frame(self.root, bg="white", height=60, padx=20)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        tk.Label(header, text="Sprite Splitter and Viewer", font=("Segoe UI", 14, "bold"), bg="white", fg="#333").pack(side=tk.LEFT)
        
        self.btn_theme = tk.Button(header, text="Modo Escuro", font=("Segoe UI", 9), bg="white", fg="#333", bd=0, cursor="hand2", command=self.toggle_theme)
        self.btn_theme.pack(side=tk.RIGHT, padx=15)
        
        tk.Label(header, text=f"Usuário: {self.user_data['username']}", font=("Segoe UI", 9), bg="white", fg="#666").pack(side=tk.RIGHT)

        # Container Principal
        main_frame = tk.Frame(self.root, padx=20, pady=20, bg="#f8f9fa")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # -- Topo: Carregamento de Arquivo --
        top_frame = tk.Frame(main_frame, bg="#f8f9fa")
        top_frame.pack(fill=tk.X, pady=(0, 20))

        btn_load = tk.Button(
            top_frame, text="↑ Carregar Sprite Sheet", 
            font=("Segoe UI", 9, "bold"), bg="white", fg="#495057", 
            bd=1, relief="groove", cursor="hand2", padx=10, 
            command=self.load_image
        )
        btn_load.pack(side=tk.LEFT)
        
        self.lbl_filepath = tk.Label(top_frame, text="Nenhuma imagem carregada.", font=("Segoe UI", 9), bg="#f8f9fa", fg="#adb5bd")
        self.lbl_filepath.pack(side=tk.LEFT, padx=15)

        # -- Centro: Colunas --
        center_frame = tk.Frame(main_frame, bg="#f8f9fa")
        center_frame.pack(fill=tk.BOTH, expand=True)

        # Painel Esquerdo: Configurações
        left_panel = tk.LabelFrame(center_frame, text=" Configurações de Corte ", font=("Segoe UI", 10, "bold"), padx=15, pady=15, bg="white", fg="#333", bd=1, relief="flat")
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 15))

        def create_entry(parent, label, row, default=""):
            tk.Label(parent, text=label, font=("Segoe UI", 9), bg="white", fg="#495057").grid(row=row, column=0, sticky="w", pady=(5, 0))
            entry = tk.Entry(parent, font=("Segoe UI", 10), bg="#f1f3f5", bd=0)
            entry.insert(0, default)
            entry.grid(row=row+1, column=0, columnspan=2, sticky="ew", pady=(2, 10), ipady=5)
            return entry

        self.entry_width = create_entry(left_panel, "Largura do Frame:", 0, "32")
        self.entry_height = create_entry(left_panel, "Altura do Frame:", 2, "32")
        self.entry_cols = create_entry(left_panel, "Colunas (Opc):", 4)
        self.entry_rows = create_entry(left_panel, "Linhas (Opc):", 6)

        btn_generate = tk.Button(
            left_panel, text="Gerar Preview", font=("Segoe UI", 10, "bold"), 
            bg="white", fg="#333", bd=1, relief="groove", cursor="hand2",
            command=self.generate_preview
        )
        btn_generate.grid(row=8, column=0, columnspan=2, pady=(10, 20), sticky="ew", ipady=8)

        # Painel de Animação
        anim_panel = tk.Frame(left_panel, bg="white")
        anim_panel.grid(row=9, column=0, columnspan=2, sticky="ew")
        
        tk.Label(anim_panel, text="Controles de Animação", font=("Segoe UI", 10, "bold"), bg="white", fg="#333").pack(anchor="w")
        
        fps_frame = tk.Frame(anim_panel, bg="white")
        fps_frame.pack(fill=tk.X, pady=5)
        tk.Label(fps_frame, text="FPS:", font=("Segoe UI", 9), bg="white").pack(side=tk.LEFT)
        self.entry_fps = tk.Entry(fps_frame, width=8, bg="#f1f3f5", bd=0)
        self.entry_fps.insert(0, "12")
        self.entry_fps.pack(side=tk.LEFT, padx=5, ipady=3)
        
        btn_anim_frame = tk.Frame(anim_panel, bg="white")
        btn_anim_frame.pack(fill=tk.X, pady=5)
        tk.Button(btn_anim_frame, text="Play", font=("Segoe UI", 9), bg="white", command=self.play_anim).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0,2))
        tk.Button(btn_anim_frame, text="Pause", font=("Segoe UI", 9), bg="white", command=self.pause_anim).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(2,0))

        tk.Label(left_panel, text="Zoom Preview:", font=("Segoe UI", 9), bg="white").grid(row=10, column=0, sticky="w", pady=(20,0))
        self.scale_zoom = tk.Scale(left_panel, from_=1, to=10, orient=tk.HORIZONTAL, bg="white", bd=0, highlightthickness=0, command=self.change_zoom)
        self.scale_zoom.set(2)
        self.scale_zoom.grid(row=11, column=0, columnspan=2, sticky="ew")

        # Painel Central: Preview
        preview_panel = tk.LabelFrame(center_frame, text=" Preview da Animação ", font=("Segoe UI", 10, "bold"), padx=15, pady=15, bg="white", fg="#333", bd=1, relief="flat")
        preview_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(preview_panel, bg="#4a5568", bd=0, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas_image_id = self.canvas.create_image(150, 150, anchor=tk.CENTER)
        self.canvas_text_id = self.canvas.create_text(150, 150, text="Carregue uma sprite sheet e gere o preview", fill="#cbd5e0", font=("Segoe UI", 10))

        # Painel Direito: Exportação
        right_panel = tk.LabelFrame(center_frame, text=" Exportação e Catálogo ", font=("Segoe UI", 10, "bold"), padx=15, pady=15, bg="white", fg="#333", bd=1, relief="flat")
        right_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=(15, 0))

        self.entry_project = create_entry(right_panel, "Nome do Projeto:", 0, "MyGame")
        self.entry_group = create_entry(right_panel, "Grupo/Personagem:", 2, "Hero")
        self.entry_tags = create_entry(right_panel, "Tags (vírgula):", 4, "idle, loop")

        tk.Label(right_panel, text="Modo de Exportação:", font=("Segoe UI", 9), bg="white").grid(row=6, column=0, sticky="w")
        self.combo_export_mode = ttk.Combobox(right_panel, values=["Frames Cortados", "Sprite Sheet Inteira"], state="readonly")
        self.combo_export_mode.current(0)
        self.combo_export_mode.grid(row=7, column=0, sticky="ew", pady=(2, 20))

        btn_export = tk.Button(
            right_panel, text="Exportar e Catalogar", font=("Segoe UI", 10, "bold"), 
            bg="#7dc29a", fg="white", activebackground="#6ab289", activeforeground="white",
            bd=0, cursor="hand2", command=self.export_sprites
        )
        btn_export.grid(row=8, column=0, sticky="ew", ipady=10)

        # Histórico de Itens Salvos
        tk.Label(right_panel, text="Últimos itens salvos:", font=("Segoe UI", 9, "bold"), bg="white", fg="#666").grid(row=9, column=0, sticky="w", pady=(20, 5))
        self.history_listbox = tk.Listbox(right_panel, font=("Segoe UI", 9), bg="#f1f3f5", bd=0, highlightthickness=0, height=5)
        self.history_listbox.grid(row=10, column=0, sticky="ew")
        
        self.update_history()

    def load_image(self):
        filepath = filedialog.askopenfilename(
            title="Selecione uma Sprite Sheet",
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")]
        )
        if not filepath:
            return

        try:
            img = Image.open(filepath)
            if getattr(img, "is_animated", False):
                self.sprite_sheet = None
                self.frames_pil = [frame.copy().convert("RGBA") for frame in ImageSequence.Iterator(img)]
                
                fps = int(self.entry_fps.get()) if self.entry_fps.get().isdigit() else 12
                self.animation_player = AnimationPlayer(self.frames_pil, fps)
                self.animation_player.play()
                
                self.lbl_filepath.config(text=os.path.basename(filepath) + " (GIF)", fg="#333")
                messagebox.showinfo("Sucesso", f"GIF Animado carregado com {len(self.frames_pil)} frames!")
                self.log_event(f"GIF Carregado: {os.path.basename(filepath)}")
            else:
                self.sprite_sheet = SpriteSheet(filepath)
                self.frames_pil = []
                self.animation_player = AnimationPlayer([])
                self.lbl_filepath.config(text=os.path.basename(filepath), fg="#333")
                messagebox.showinfo("Sucesso", "Imagem carregada com sucesso!")
                self.log_event(f"Imagem Carregada: {os.path.basename(filepath)}")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def generate_preview(self):
        if not self.sprite_sheet:
            messagebox.showwarning("Aviso", "Por favor, carregue uma imagem primeiro.")
            return

        try:
            fw = int(self.entry_width.get())
            fh = int(self.entry_height.get())
            
            # Colunas e linhas são opcionais
            cols_str = self.entry_cols.get()
            rows_str = self.entry_rows.get()
            cols = int(cols_str) if cols_str.isdigit() else None
            rows = int(rows_str) if rows_str.isdigit() else None

            self.frames_pil = self.sprite_sheet.slice_sprites(fw, fh, cols, rows)
            
            if not self.frames_pil:
                messagebox.showerror("Erro", "O tamanho informado não gerou nenhum frame válido.")
                return

            # Atualizar os frames do Player e aplicar FPS
            fps = int(self.entry_fps.get())
            self.animation_player = AnimationPlayer(self.frames_pil, fps)
            self.animation_player.play()
            
            self.log_event(f"Preview Gerado: {fw}x{fh} ({len(self.frames_pil)} frames)")
            messagebox.showinfo("Sucesso", f"{len(self.frames_pil)} frames gerados cortados em {fw}x{fh}.")

        except ValueError:
            messagebox.showerror("Erro", "Valores numéricos inválidos nas configurações de corte.")

    def play_anim(self):
        try:
            fps = int(self.entry_fps.get())
            self.animation_player.set_fps(fps)
            self.animation_player.play()
        except ValueError:
            messagebox.showerror("Erro de FPS", "O valor de FPS deve ser um número inteiro.")

    def pause_anim(self):
        self.animation_player.pause()

    def change_zoom(self, val):
        self.scale_factor = float(val)

    def update_canvas(self):
        # Verifica se há animação tocando
        if self.animation_player.is_playing:
            self.animation_player.update()

        # Atualiza a imagem na tela se tivermos frames
        current_frame = self.animation_player.get_current_frame()
        if current_frame:
            # Aplica zoom (efeito de pixel art)
            scaled_frame = scale_image(current_frame, self.scale_factor)
            self.current_tk_image = ImageTk.PhotoImage(scaled_frame)

            # Centraliza no Canvas
            cw = self.canvas.winfo_width() / 2
            ch = self.canvas.winfo_height() / 2
            
            # Previne que o canvas acuse width/height como 1 no início
            if cw < 5: cw = 150
            if ch < 5: ch = 150

            self.canvas.coords(self.canvas_image_id, cw, ch)
            self.canvas.itemconfig(self.canvas_image_id, image=self.current_tk_image)

        # Chama novamente essa função daqui a ~16ms (aprox 60 quadros/s de atualização de interface)
        self.root.after(16, self.update_canvas)

    def apply_theme(self, to_dark):
        color_map = {
            "#f8f9fa": "#1e1e2e", "white": "#282a36", "#ffffff": "#282a36",
            "#333": "#f8f8f2", "#333333": "#f8f8f2", "#666": "#bfbfbf", "#666666": "#bfbfbf",
            "#495057": "#f8f8f2", "#adb5bd": "#6272a4", "#f1f3f5": "#44475a", 
            "#4a5568": "#191a21", "black": "white"
        }
        if not to_dark:
            color_map = {
                "#1e1e2e": "#f8f9fa", "#282a36": "white", "#f8f8f2": "#333", 
                "#bfbfbf": "#666", "#6272a4": "#adb5bd", "#44475a": "#f1f3f5", 
                "#191a21": "#4a5568", "white": "black"
            }

        def update_widget(w):
            try:
                keys = w.keys()
                if "bg" in keys and w.cget("bg") in color_map:
                    w.configure(bg=color_map[w.cget("bg")])
                if "fg" in keys and w.cget("fg") in color_map:
                    w.configure(fg=color_map[w.cget("fg")])
                if "insertbackground" in keys and w.cget("insertbackground") in color_map:
                    w.configure(insertbackground=color_map[w.cget("insertbackground")])
            except: pass
            
            for child in w.winfo_children(): update_widget(child)

        update_widget(self.root)
        
        # O ttk.Combobox usa o estilo do root em alguns temas, e bg do Canvas
        if to_dark:
            self.canvas.itemconfig(self.canvas_text_id, fill="#6272a4")
        else:
            self.canvas.itemconfig(self.canvas_text_id, fill="#cbd5e0")

    def toggle_theme(self):
        self.is_dark_mode = not getattr(self, 'is_dark_mode', False)
        self.apply_theme(self.is_dark_mode)
        
        if self.is_dark_mode:
            self.btn_theme.config(text="Modo Claro")
        else:
            self.btn_theme.config(text="Modo Escuro")

    def update_history(self):
        self.history_listbox.delete(0, tk.END)
        logs = self.db.get_user_logs(self.user_data['id'], limit=50)
        count = 0
        for log in logs:
            action = log[0]
            if "Exportação Concluída" in action:
                display_text = action.replace("Exportação Concluída: ", "• ")
                self.history_listbox.insert(tk.END, display_text)
                count += 1
                if count >= 5:
                    break
        if count == 0:
            self.history_listbox.insert(tk.END, "Nenhum item salvo.")

    def export_sprites(self):
        export_mode = self.combo_export_mode.get()
        
        if export_mode == "Frames Cortados":
            if not self.frames_pil:
                messagebox.showwarning("Aviso", "Ainda não há frames para exportar.")
                return
            export_data = self.frames_pil
        elif export_mode == "Sprite Sheet Inteira":
            if self.sprite_sheet:
                export_data = self.sprite_sheet.sheet
            elif self.frames_pil:
                # Caso seja um GIF animado e o usuário queira converter para Sprite Sheet (uma linha)
                total_w = sum(f.width for f in self.frames_pil)
                max_h = max(f.height for f in self.frames_pil)
                sheet = Image.new("RGBA", (total_w, max_h))
                
                offset_x = 0
                for f in self.frames_pil:
                    sheet.paste(f, (offset_x, 0))
                    offset_x += f.width
                export_data = sheet
            else:
                messagebox.showwarning("Aviso", "Nenhuma imagem para exportar.")
                return
        else:
            return

        project = self.entry_project.get()
        group = self.entry_group.get()
        tags_raw = self.entry_tags.get()
        
        # Formata tags para lista limpa ("idle, loop" -> ["idle", "loop"])
        tags = [t.strip() for t in tags_raw.split(",") if t.strip()]

        fps = int(self.entry_fps.get()) if self.entry_fps.get().isdigit() else 12

        try:
            entry = self.project_manager.register_and_export_sprite(
                project_name=project,
                group_name=group,
                tags=tags,
                export_data=export_data,
                fps=fps,
                export_mode="frames" if export_mode == "Frames Cortados" else "spritesheet"
            )
            
            path = entry["export_path"]
            version = entry["version"]
            self.log_event(f"Exportação Concluída: {project} ({version})")
            self.update_history()
            messagebox.showinfo("Sucesso", f"Exportação concluída!\nVersão gerada: {version}\nSalvo em: {path}")

        except Exception as e:
            messagebox.showerror("Erro de Exportação", str(e))

if __name__ == "__main__":
    def start_app(user_data):
        # Destruir a janela de login e iniciar a principal
        for widget in root.winfo_children():
            widget.destroy()
        app = SpriteApp(root, user_data)

    root = tk.Tk()
    root.title("VLV Sprite Organizer - Acesso")
    auth = LoginRegisterWindow(root, start_app)
    root.mainloop()
