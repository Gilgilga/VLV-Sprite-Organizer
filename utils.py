import os
from PIL import Image

def scale_image(pil_image, scale_factor):
    """
    Redimensiona uma imagem PIL mantendo o estilo pixel art (NEAREST)
    baseado em um fator de escala. Útil para pré-visualização (zoom).
    """
    if not pil_image:
        return None
    width, height = pil_image.size
    new_size = (int(width * scale_factor), int(height * scale_factor))
    return pil_image.resize(new_size, Image.Resampling.NEAREST)
#.