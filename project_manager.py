import os
import json
import glob

class ProjectManager:
    """
    Gerencia os arquivos físicos (sprites) e o banco de dados local (JSON).
    """
    def __init__(self, workspace_dir="workspace"):
        """
        Inicializa o gerenciador garantindo a estrutura inicial de pastas e o JSON.
        """
        self.workspace_dir = workspace_dir
        self.catalog_path = os.path.join(self.workspace_dir, "sprites_catalog.json")
        self.sprites_dir = os.path.join(self.workspace_dir, "sprites")
        
        # Garante que as pastas base existem
        os.makedirs(self.sprites_dir, exist_ok=True)
        
        # Carrega o catálogo ou cria um novo
        self.catalog = self._load_catalog()

    def _load_catalog(self):
        """Carrega o arquivo JSON do catálogo, se existir."""
        if os.path.exists(self.catalog_path):
            with open(self.catalog_path, 'r', encoding='utf-8') as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return {"projects": {}, "sprites": []}
        return {"projects": {}, "sprites": []}

    def _save_catalog(self):
        """Salva as informações no catálogo JSON."""
        with open(self.catalog_path, 'w', encoding='utf-8') as f:
            json.dump(self.catalog, f, indent=4, ensure_ascii=False)

    def register_and_export_sprite(self, project_name, group_name, tags, export_data, fps, export_mode="frames"):
        """
        Registra uma nova sprite no catálogo com versionamento automático
        e exporta conforme o modo escolhido ("frames" para frames separados, "spritesheet" para a folha inteira).
        
        Estrutura: workspace/sprites/[project_name]/[group_name]/[primary_tag]/exports/
        """
        # Limpar e preparar os dados básicos
        project_name = project_name.strip() or "DefaultProject"
        group_name = group_name.strip() or "DefaultCharacter"
        
        if not tags:
            tags = ["general"]
        
        # A tag principal define a subpasta. Ex: "idle", "attack"
        primary_tag = tags[0]
        
        # Gerar o nome base identificador: project_group_primaryTag
        base_id = f"{project_name}_{group_name}_{primary_tag}"
        
        # Lógica de versionamento automático baseado no histórico do catálogo
        # Filtra todas as sprites que tem o mesmo project_name, group_name e primary_tag
        matching_sprites = [
            s for s in self.catalog["sprites"] 
            if s.get("project_name") == project_name 
            and s.get("group_name") == group_name
            and s.get("primary_tag") == primary_tag
        ]
        
        version_num = len(matching_sprites) + 1
        version_str = f"v{version_num}"
        
        # Criar a estrutura de diretórios final para exportação
        export_path = os.path.join(self.sprites_dir, project_name, group_name, primary_tag, "exports", version_str)
        os.makedirs(export_path, exist_ok=True)
        
        # Salvar as imagens usando Pillow
        saved_paths = []
        if export_mode == "frames":
            for i, frame in enumerate(export_data):
                filename = f"frame_{str(i).zfill(3)}.png"
                filepath = os.path.join(export_path, filename)
                frame.save(filepath, "PNG")
                saved_paths.append(filepath)
            frame_count = len(export_data)
        elif export_mode == "spritesheet":
            # export_data é uma única instância de PIL.Image
            filename = f"{base_id}_spritesheet.png"
            filepath = os.path.join(export_path, filename)
            export_data.save(filepath, "PNG")
            saved_paths.append(filepath)
            frame_count = 1
            
        # Adicionar os dados no JSON
        sprite_entry = {
            "id": f"{base_id}_{version_str}",
            "project_name": project_name,
            "group_name": group_name,
            "primary_tag": primary_tag,
            "tags": tags,
            "version": version_str,
            "export_mode": export_mode,
            "fps_preview": fps,
            "frame_count": frame_count,
            "export_path": export_path
        }
        
        self.catalog["sprites"].append(sprite_entry)
        self._save_catalog()
        
        return sprite_entry

    def search_by_tag(self, tag):
        """Busca todas as sprites catalogadas que possuam a tag."""
        return [s for s in self.catalog["sprites"] if tag in s.get("tags", [])]
        
    def scan_for_unregistered(self, scan_folder):
        """
        Um diferencial opcional: escaneia uma pasta preexistente em busca
        de imagens PNG/JPG que não estão no projeto atual.
        Útil para jogos feitos na Unity/GameMaker onde temos dump de imagens.
        Retorna lista de caminhos de arquivos.
        """
        unregistered = []
        if not os.path.exists(scan_folder):
            return unregistered
            
        image_files = glob.glob(os.path.join(scan_folder, "*.png"))
        
        # Consideramos registradas apenas as que estão no nosso workspace 'exports'
        # Isso atende à necessidade da "função que detecta novas imagens adicionadas à pasta"
        for img_path in image_files:
            if "exports" not in img_path:
                unregistered.append(img_path)
                
        return unregistered
#.