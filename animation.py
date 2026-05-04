import time
#.
class AnimationPlayer:
    """
    Controla o estado e reprodução de uma animação baseada em frames.
    Independente de biblioteca gráfica, fornece apenas o estado atual.
    """
    def __init__(self, frames, fps=12):
        """
        Inicializa o player com uma lista de frames gerados pelo SpriteSheet.
        """
        self.frames = frames if frames else []
        self.fps = fps
        self.current_frame_index = 0
        self.is_playing = False
        self._last_update_time = time.time()

    def get_current_frame(self):
        """
        Retorna a imagem do frame atual. Retorna None se não houver frames.
        """
        if not self.frames:
            return None
        return self.frames[self.current_frame_index]

    def set_fps(self, fps):
        """
        Ajusta a velocidade da animação em quadros por segundo.
        """
        # Limita para valores razoáveis
        self.fps = max(1, min(fps, 120))

    def play(self):
        self.is_playing = True
        self._last_update_time = time.time()

    def pause(self):
        self.is_playing = False

    def stop(self):
        self.is_playing = False
        self.current_frame_index = 0

    def update(self):
        """
        Deve ser chamado em loop (pelo UI). Atualiza o current_frame_index
        se tiver passado tempo suficiente baseado no FPS.
        """
        if not self.is_playing or not self.frames:
            return

        current_time = time.time()
        time_elapsed = current_time - self._last_update_time
        time_per_frame = 1.0 / self.fps

        # Enquanto o tempo decorrido for maior que o tempo de um frame,
        # avançamos os frames e subtraímos do acumulador.
        if time_elapsed >= time_per_frame:
            # Quantos frames devemos avançar? 
            # (geralmente 1, mas caso haja travamento no PC, podem ser mais)
            frames_to_advance = int(time_elapsed / time_per_frame)
            
            self.current_frame_index = (self.current_frame_index + frames_to_advance) % len(self.frames)
            
            # Mantemos o "resto" do tempo para não perdermos sincronia
            self._last_update_time = current_time - (time_elapsed % time_per_frame)
