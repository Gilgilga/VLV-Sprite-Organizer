# 🖼️ VLV Sprite Organizer

> [!TIP]
> **Consulte o [Guia do Usuário](file:///c:/Users/Victor/Proj/SpriteManager/GUIA_DO_USUARIO.md) para instruções detalhadas de uso.**


Uma aplicação Desktop simples em Python (usando Tkinter e Pillow) para carregar, fatiar e pré-visualizar *Sprite Sheets* de Pixel Art, organizar por projeto e tag, e exportar com versionamento automático. Ideal para estudantes ou devs de jogos (Unity, GameMaker) que querem visualizar a animação sem precisar importar todos os assets manualmente para a engine primeiro.

## Como Executar

1. **Requisitos:**
   - Python 3.8+ instalado.
   - Instalar as bibliotecas listadas em `requirements.txt`.
   
   Abra o terminal na pasta do projeto e instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

2. **Iniciando a Aplicação:**
   Execute o arquivo principal:
   ```bash
   python main.py
   ```

## Fluxo de Uso

1. **Carregar Sprite:** Clique em "Carregar Sprite Sheet" e escolha uma imagem `.png`.
2. **Configuração de Corte:** Informe a Largura e Altura do frame (ex: `32`x`32`). Se a sprite possuir colunas e linhas exatas, deixe os campos "Colunas" e "Linhas" vazios para cálculo automático.
3. **Preview:** Clique em "Gerar Preview". A aplicação fatiará os frames e exibirá a animação no Canvas central.
4. **Controles:** Use os botões *Play/Pause*, altere o *FPS* e ajuste o *Zoom Preview* livremente.
5. **Organização:** Na lateral direita, preencha o Nome do Projeto, Grupo/Personagem e adicione Tags separadas por vírgula (a primeira Tag será considerada a principal).
6. **Exportar:** Clique em "Exportar e Catalogar". Uma pasta `workspace` será criada localmente estruturando os arquivos e criando as versões (ex: `v1`, `v2`) baseando-se no arquivo local gerado `sprites_catalog.json`.

## Estrutura do Código (Padrão MVC Simplificado)

- `main.py`: **(View e Controller)** Contém a interface em Tkinter, eventos de UI e linkagem entre models.
- `spritesheet.py`: **(Model)** Contém as estruturas que lidam com a imagem base e matemática do fatiamento.
- `animation.py`: **(Model)** Controle de reprodução e lógica do Player agnóstico à interface gráfica.
- `project_manager.py`: **(Model)** Abstração da manipulação do sistema de arquivos e do banco JSON de tags/versionamento.
- `utils.py`: Funções utilitárias desacopladas (como o resizer para Zoom Pixel Art).

## Diferenciais Técnicos
- O Tkinter foi escolhido pois é leve e nativo. A lógica não se mistura, mantendo fácil manutenção se houver desejo de refazer a UI em PyQt ou Flask.
- Versionamento Automático baseado em arquivo JSON, sem necessitar de banco de dados robusto.
