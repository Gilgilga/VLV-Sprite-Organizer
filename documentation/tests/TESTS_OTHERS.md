| Informação | Resultados |
| :--- | :--- |
| **Identificação única** | TST-003 Importar Imagem/SpriteSheet |
| **Caso de uso em que se baseia** | UC02 - Carregar Ativos de Imagem |
| **Cenário** | Fluxo principal de sucesso |
| **Preparação** | O sistema está na janela principal após o login. |
| **Passos para a execução do teste** | (1) Clicar em "Carregar Sprite Sheet"; <br> (2) Selecionar um arquivo PNG válido; <br> (3) Confirmar seleção. |
| **Resultado esperado** | O sistema carrega a imagem e exibe mensagem de Confirmação. |
| **Resultado do teste** | ( ) NÃO EXECUTADO (x) SUCESSO ( ) FALHA ( ) CANCELADO |
| **Descrição do resultado obtido** | A imagem PNG foi carregada correntemente no sistema. |
| **Data da última execução do teste** | 06/04/2026 |
<!-- slide -->
| Informação | Resultados |
| :--- | :--- |
| **Identificação única** | TST-004 Gerar Preview da Animação |
| **Caso de uso em que se baseia** | UC03 - Fatiar e Visualizar Sprites |
| **Cenário** | Fluxo principal de sucesso |
| **Preparação** | Uma Sprite Sheet PNG válida já foi carregada. |
| **Passos para a execução do teste** | (1) Preencher largura e altura do frame (ex: 32x32); <br> (2) Clicar em "Gerar Preview". |
| **Resultado esperado** | O sistema gera os frames fatiados e inicia a animação no Canvas. |
| **Resultado do teste** | ( ) NÃO EXECUTADO (x) SUCESSO ( ) FALHA ( ) CANCELADO |
| **Descrição do resultado obtido** | Frames foram extraídos corretamente e o player de animação funcionou. |
| **Data da última execução do teste** | 06/04/2026 |
<!-- slide -->
| Informação | Resultados |
| :--- | :--- |
| **Identificação única** | TST-005 Exportar e Catalogar Sprites |
| **Caso de uso em que se baseia** | UC04 - Organização e Versionamento |
| **Cenário** | Fluxo principal de sucesso |
| **Preparação** | Um preview funcional já foi gerado. |
| **Passos para a execução do teste** | (1) Preencher nome do projeto e grupo; <br> (2) Clicar em "Exportar e Catalogar". |
| **Resultado esperado** | Os arquivos PNG são salvos na pasta 'workspace' e o catálogo é atualizado. |
| **Resultado do teste** | ( ) NÃO EXECUTADO (x) SUCESSO ( ) FALHA ( ) CANCELADO |
| **Descrição do resultado obtido** | Exportação realizada com sucesso. Gerada pasta de versão (ex: v1). |
| **Data da última execução do teste** | 06/04/2026 |
<!-- slide -->
| Informação | Resultados |
| :--- | :--- |
| **Identificação única** | TST-006 Tentativa de arquivo incorreto |
| **Caso de uso em que se baseia** | UC02 - Carregar Ativos de Imagem |
| **Cenário** | Fluxo de exceção |
| **Preparação** | O sistema está na janela principal pronto para importar. |
| **Passos para a execução do teste** | (1) Selecionar um arquivo de texto (.txt) renomeado para .png; <br> (2) Tentar importar. |
| **Resultado esperado** | O sistema captura a exceção de abertura de imagem e exibe mensagem de erro. |
| **Resultado do teste** | ( ) NÃO EXECUTADO (x) SUCESSO ( ) FALHA ( ) CANCELADO |
| **Descrição do resultado obtido** | Mensagem de erro adequada exibida: "cannot identify image file". |
| **Data da última execução do teste** | 06/04/2026 |
