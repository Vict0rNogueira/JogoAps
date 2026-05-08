# Boolean Battle RPG

Um jogo em Python desenvolvido com Pygame, onde o jogador enfrenta um boss em um sistema de batalha baseado em lógica booleana.

## Descrição

Em `Boolean Battle RPG`, o jogador explora um mapa simples, encontra um NPC e entra em uma batalha onde precisa responder corretamente a expressões lógicas para atacar o inimigo.

O objetivo é derrotar o boss antes que o jogador fique sem vida.

## Como jogar

1. Execute `main.py`.
2. Na tela do mundo, mova o personagem com as teclas `W`, `A`, `S` e `D`.
3. Aproxime-se do NPC e pressione `E` para iniciar o diálogo e começar a batalha.
4. Na batalha, responda à expressão lógica escolhendo `TRUE` ou `FALSE`.
5. Respostas corretas lançam um ataque mágico contra o boss.
6. Respostas erradas fazem o boss atacar você.
7. O jogo termina quando o boss ou o jogador perde toda a vida.

## Controles

- `W`, `A`, `S`, `D`: mover o personagem no mundo.
- `E`: interagir com o NPC.
- `SPACE`: avançar nos diálogos.
- Clique do mouse: escolher `TRUE` ou `FALSE` durante a batalha.
- `ESC`: sair do jogo.

## Requisitos

- Python 3.x
- Pygame

## Instalação

1. Instale Python:

   ```bash
   python --version
   ```

2. Instale o Pygame:

   ```bash
   pip install pygame
   ```

3. Execute o jogo:

   ```bash
   python main.py
   ```

## Estrutura do projeto

- `main.py`: código principal do jogo.
- `assets/`: imagens e sons usados no jogo.
- `assets/sounds/`: arquivos de áudio para efeitos e música.

## Recursos

- Exploração simples em tela cheia.
- Sistema de batalha com lógica booleana.
- Perguntas de lógica geradas aleatoriamente.
- Sons de ataque, diálogo e vitória.
- Feedback visual de HP e efeitos de acerto.

## Observações

- O jogo carrega vários arquivos de imagem e áudio da pasta `assets`.
- Verifique se o diretório `assets` está presente e contém as imagens e sons necessários.

---

Desenvolvido como um pequeno RPG educativo de lógica booleana usando `pygame`.