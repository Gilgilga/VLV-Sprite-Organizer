from PIL import Image

class SpriteSheet:
    """
    Classe responsável por carregar a imagem da sprite sheet e 
    realizar o corte em frames individuais com base na configuração.
    """
    def __init__(self, filename):
        """
        Carrega a sprite sheet a partir de um arquivo.
        """
        try:
            self.sheet = Image.open(filename).convert("RGBA")
        except Exception as e:
            raise FileNotFoundError(f"Não foi possível carregar a imagem: {filename}. Erro: {e}")

    def get_image_size(self):
        """
        Retorna as dimensões (largura, altura) da sprite sheet.
        """
        return self.sheet.size

    def slice_sprites(self, frame_width, frame_height, cols=None, rows=None):
        """
        Corta a sprite sheet em frames de tamanho específico (frame_width x frame_height).
        Opcionalmente, o usuário pode definir colunas (cols) e linhas (rows) máximas.
        Retorna uma lista de objetos Image (frames).
        """
        sheet_width, sheet_height = self.sheet.size
        
        # Se cols ou rows não forem fornecidos, calculamos baseados no tamanho do frame
        if not cols:
            cols = sheet_width // frame_width
        if not rows:
            rows = sheet_height // frame_height
            
        frames = []
        for row in range(rows):
            for col in range(cols):
                # Calcular as coordenadas do retângulo de corte (bounding box)
                left = col * frame_width
                top = row * frame_height
                right = left + frame_width
                bottom = top + frame_height
                
                # Checar se o bounding box ultrapassa o limite da imagem
                if right > sheet_width or bottom > sheet_height:
                    continue
                
                # Realizar o slicing da região da imagem
                box = (left, top, right, bottom)
                frame = self.sheet.crop(box)
                frames.append(frame)
                
        return frames
#.