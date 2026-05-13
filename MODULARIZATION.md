# Boolean Battle RPG - Estrutura Modular

## Arquitetura do Projeto

O código foi reorganizado em uma estrutura modular bem definida para melhor manutenção, reutilização e escalabilidade.

### 📁 Estrutura de Arquivos

```
APSLM/
├── main.py                 # Loop principal do jogo
├── config.py              # Configurações globais (cores, tamanhos, constantes)
├── assets.py              # Carregamento de imagens e sons
├── entities.py            # Classes de entidades (Player, Boss, NPC, Spell)
├── game_logic.py          # Lógica de jogo (expressões booleanas)
├── ui.py                  # Sistema de UI (botões, barras, diálogos)
├── states.py              # Gerenciador de estados do jogo
├── assets/                # Recursos do jogo
│   ├── sounds/
│   │   ├── spell.wav
│   │   ├── hit.wav
│   │   ├── dialogue.wav
│   │   ├── victory.wav
│   │   └── battle.wav
│   └── *.png, *.jpg       # Imagens
└── README.md              # Este arquivo
```

## 📋 Descrição dos Módulos

### `config.py`
Centraliza todas as configurações globais do jogo:
- **Display**: Resolução, clock, caption
- **Fontes**: Estilos de texto
- **Cores**: Paleta de cores
- **Constantes**: Velocidades, danos, HP máximo, posições

**Benefícios**: Mudança fácil de valores sem procurar no código inteiro.

### `assets.py`
Gerencia carregamento de recursos:
- Funções helper para carregar imagens e sons
- Cache de imagens e sons já carregados
- Suporte a redimensionamento automático

**Benefícios**: Separação entre lógica e recursos; fácil adicionar novos assets.

### `entities.py`
Define as classes principais do jogo:
- **`Player`**: Jogador com movimento, HP, dano
- **`Boss`**: Chefe do jogo
- **`Spell`**: Projéteis/magias
- **`NPC`**: Personagem não-jogável com diálogos

**Benefícios**: Encapsulamento de comportamento; reutilização de lógica.

### `game_logic.py`
Implementa a lógica específica do jogo:
- **`LogicPuzzle`**: Gerador de expressões booleanas
- **`GameRound`**: Gerencia uma rodada de jogo

**Benefícios**: Fácil alterar regras/expressões; testável isoladamente.

### `ui.py`
Sistema de renderização de interface:
- **`UIButton`**: Botões interativos
- **`HealthBar`**: Barras de vida
- **`BattleUI`**: UI completa da batalha
- **`WorldUI`**, **`DialogueUI`**, **`EndGameUI`**: UIs específicas

**Benefícios**: Centralização de desenho; fácil reestilizar.

### `states.py`
Gerenciador de estados e transições:
- **`GameStateManager`**: Controla estados (world, dialogue, battle)
- Transições entre estados
- Lógica de atualização por estado

**Benefícios**: Máquina de estados clara; fácil adicionar novos estados.

### `main.py`
Loop principal simplificado:
- Inicialização do Pygame
- Instanciação de objetos
- Loop de eventos e renderização

**Benefícios**: Código simples e legível; fácil de entender o fluxo.

## 🎮 Como Usar

### Adicionar novo NPC
```python
# Em entities.py, adicionar ao __init__:
self.dialogues = [
    "Novo diálogo...",
    "Outro diálogo..."
]

# Em main.py:
new_npc = NPC(x, y, assets.npc_img_2)
game_objects["new_npc"] = new_npc
```

### Mudar expressão lógica
```python
# Em game_logic.py, alterar LogicPuzzle.generate():
answer = (p or q) and r  # Mudou de (P AND Q) OR R
```

### Adicionar novo efeito sonoro
```python
# Em assets.py:
new_sound = load_sound("assets/sounds/new_effect.wav")

# Em main.py:
new_sound.play()
```

### Adicionar novo estado
```python
# 1. Em states.py, adicionar em draw_* e update_*
# 2. Em main.py, adicionar na lógica de estados
state_manager.transition_to("novo_estado")
```

## 🔧 Vantagens da Modularização

✅ **Manutenção**: Cada módulo tem responsabilidade única
✅ **Reutilização**: Classes podem ser usadas em outros projetos
✅ **Testes**: Fácil testar lógica isoladamente
✅ **Escalabilidade**: Adicionar features sem quebrar código existente
✅ **Legibilidade**: main.py é claro e fácil de entender
✅ **Debugging**: Erros localizados rapidamente

## 📝 Próximas Melhorias Sugeridas

- [ ] Sistema de áudio em classe separada
- [ ] Loader de dados (NPCs, inimigos) de arquivo
- [ ] Sistema de efeitos de partículas
- [ ] Save/Load de progresso
- [ ] Menu principal
- [ ] Testes unitários para game_logic.py
