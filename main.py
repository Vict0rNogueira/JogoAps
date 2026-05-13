"""
Main - Loop principal do jogo Boolean Battle RPG
"""
import pygame
import sys

# Inicializar Pygame
pygame.init()
pygame.mixer.init()

# Importar configurações
from config import screen, clock, WIDTH, HEIGHT

# Importar assets
import assets

# Importar entidades
from entities import Player, Boss, NPC, Spell, VictoryDialogue

# Importar lógica de jogo
from game_logic import GameRound

# Importar estados
from states import GameStateManager

# Importar UI
from ui import draw_text
from config import font, WHITE

# ================= INICIALIZAR OBJETOS =================
game_objects = {
    "player": Player(120, HEIGHT - 440, assets.player_img),
    "boss": Boss(WIDTH - 420, HEIGHT - 470, assets.boss_img),
    "npc": NPC(
        WIDTH // 2 + 300,
        HEIGHT // 2 - 50,
        assets.npc_img
    ),
    "victory_dialogue": VictoryDialogue(assets.npc_img),
    "round": GameRound(),
    "player_spell": Spell(120 + 120, HEIGHT - 440 + 50, WIDTH - 420, is_player_spell=True),
    "boss_spell": Spell(WIDTH - 420 - 40, HEIGHT - 470 + 100, 120 + 120, is_player_spell=False),
}

# Gerenciador de estados
state_manager = GameStateManager(game_objects)

# ================= LOOP PRINCIPAL =================
running = True

while running:
    dt = clock.tick(120)
    
    # ================= EVENTOS =================
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            # Sair com ESC
            if event.key == pygame.K_ESCAPE:
                running = False
            
            # ================= DIÁLOGO INICIAL =================
            if state_manager.current_state == "dialogue":
                if event.key == pygame.K_SPACE:
                    assets.dialogue_sound.play()
                    state_manager.next_dialogue()
                    
                    npc = game_objects["npc"]
                    if not npc.has_more_dialogue(state_manager.dialogue_index):
                        import pygame
                        pygame.time.delay(300)
                        state_manager.transition_to("battle")
            
            # ================= DIÁLOGO DE VITÓRIA =================
            if state_manager.current_state == "victory_dialogue":
                if event.key == pygame.K_SPACE:
                    assets.dialogue_sound.play()
                    state_manager.next_victory_dialogue()
                    
                    victory_dialogue = game_objects["victory_dialogue"]
                    if not victory_dialogue.has_more_dialogue(state_manager.victory_dialogue_index):
                        pygame.time.delay(300)
                        running = False
            
            # ================= INTERAÇÃO NPC =================
            if event.key == pygame.K_e:
                if state_manager.current_state == "world":
                    player = game_objects["player"]
                    npc = game_objects["npc"]
                    
                    if npc.is_nearby(player.rect):
                        state_manager.transition_to("dialogue")
                elif state_manager.current_state == "battle" and state_manager.game_over and game_objects["player"].hp <= 0:
                    assets.loss_sound.play()
                    running = False
        
        # ================= CLIQUE NA BATALHA =================
        if event.type == pygame.MOUSEBUTTONDOWN:
            if state_manager.current_state == "battle":
                mouse_pos = pygame.mouse.get_pos()
                if state_manager.game_over and game_objects["player"].hp <= 0:
                    action = state_manager.handle_defeat_input(mouse_pos)
                    if action == "quit":
                        running = False
                else:
                    state_manager.handle_battle_input(mouse_pos)
    
    # ================= MOVIMENTO MUNDO =================
    if state_manager.current_state == "world":
        keys = pygame.key.get_pressed()
        player = game_objects["player"]
        player.update_position(keys)
    
    # ================= ATUALIZAR BATALHA =================
    if state_manager.current_state == "battle":
        state_manager.update_battle()
    
    # ================= DESENHAR =================
    if state_manager.current_state == "world":
        state_manager.draw_world(screen, game_objects["player"])
    
    elif state_manager.current_state == "dialogue":
        screen.blit(assets.dialogue_img, (0, 0))
        state_manager.draw_dialogue(screen)
    
    elif state_manager.current_state == "victory_dialogue":
        screen.blit(assets.dialogue_img, (0, 0))
        state_manager.draw_victory_dialogue(screen)
    
    elif state_manager.current_state == "battle":
        state_manager.draw_battle(screen, game_objects["player"], game_objects["boss"])
    
    pygame.display.flip()

pygame.quit()
sys.exit()