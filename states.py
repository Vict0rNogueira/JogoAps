"""
Gerenciador de estados do jogo
"""
import pygame
import random
from config import WIDTH, HEIGHT, PLAYER_BATTLE_X, PLAYER_BATTLE_Y
from assets import background, world_bg, dialogue_img, spell_img, spell_sound, hit_sound
from ui import WorldUI, DialogueUI, EndGameUI, BattleUI, draw_text
from config import BLACK, WHITE, RED, BLUE, YELLOW


class GameStateManager:
    """Gerencia os estados do jogo"""
    
    def __init__(self, game_objects):
        self.current_state = "world"
        self.game_objects = game_objects
        self.battle_ui = BattleUI()
        self.dialogue_index = 0
        self.game_over = False
        self.victory_played = False
        self.boss_hit_timer = 0
        self.player_hit_timer = 0
    
    def transition_to(self, new_state):
        """Transiciona para novo estado"""
        self.current_state = new_state
        
        if new_state == "dialogue":
            self.dialogue_index = 0
        elif new_state == "battle":
            self.game_over = False
            self.victory_played = False
    
    def next_dialogue(self):
        """Avança diálogo"""
        npc = self.game_objects["npc"]
        if self.dialogue_index < len(npc.dialogues):
            self.dialogue_index += 1
    
    def handle_battle_input(self, mouse_pos):
        """Processa clique na batalha"""
        player_choice = self.battle_ui.get_button_at_pos(mouse_pos)
        
        game_round = self.game_objects["round"]
        player = self.game_objects["player"]
        boss = self.game_objects["boss"]
        
        player_spell = self.game_objects["player_spell"]
        boss_spell = self.game_objects["boss_spell"]
        
        if (
            player_choice is not None
            and not player_spell.active
            and not boss_spell.active
            and not self.game_over
        ):
            # Verifica resposta
            is_correct = game_round.check(player_choice)
            
            if is_correct:
                player_spell.active = True
                spell_sound.play()
                self.battle_ui.update_message("Magia lançada!")
            else:
                boss_spell.active = True
                spell_sound.play()
                self.battle_ui.update_message("O boss lançou magia!")
    
    def update_battle(self):
        """Atualiza lógica da batalha"""
        player = self.game_objects["player"]
        boss = self.game_objects["boss"]
        player_spell = self.game_objects["player_spell"]
        boss_spell = self.game_objects["boss_spell"]
        game_round = self.game_objects["round"]
        
        # Magia do player
        if player_spell.active:
            player_spell.update()
            
            if not player_spell.active:  # Acertou
                boss.take_damage(player_spell.damage)
                hit_sound.play()
                self.boss_hit_timer = 10
                self.battle_ui.update_message("Ataque super efetivo!")
                game_round.generate_new()
        
        # Magia do boss
        if boss_spell.active:
            boss_spell.update()
            
            if not boss_spell.active:  # Acertou
                player.take_damage(boss_spell.damage)
                hit_sound.play()
                self.player_hit_timer = 10
                self.battle_ui.update_message("Você recebeu dano!")
                game_round.generate_new()
        
        # Atualiza UI com HP
        self.battle_ui.set_player_hp(player.hp)
        self.battle_ui.set_boss_hp(boss.hp)
        
        # Verifica fim de jogo
        if boss.hp <= 0 and not self.game_over:
            self.game_over = True
            from assets import victory_sound
            victory_sound.play()
            self.victory_played = True
        
        if player.hp <= 0 and not self.game_over:
            self.game_over = True
    
    def draw_world(self, screen, player):
        """Desenha tela de mundo"""
        screen.blit(world_bg, (0, 0))
        
        # Sombra do player
        pygame.draw.ellipse(
            screen,
            (0, 0, 0),
            (
                player.x + 10,
                player.y + 60,
                60,
                20
            )
        )
        
        npc = self.game_objects["npc"]
        npc.draw(screen)
        player.draw(screen, player.x, player.y)
        
        WorldUI.draw_controls(screen)
    
    def draw_dialogue(self, screen):
        """Desenha tela de diálogo"""
        screen.blit(dialogue_img, (0, 0))
        
        npc = self.game_objects["npc"]
        dialogue_text = npc.get_dialogue(self.dialogue_index)
        
        DialogueUI.draw_dialogue(screen, npc.name, dialogue_text)
    
    def draw_battle(self, screen, player, boss):
        """Desenha tela de batalha"""
        screen.blit(background, (0, 0))
        
        # Efeito de tremor
        player_draw_x = PLAYER_BATTLE_X
        boss_draw_x = boss.x
        
        if self.boss_hit_timer > 0:
            boss_draw_x += random.randint(-8, 8)
            self.boss_hit_timer -= 1
        
        if self.player_hit_timer > 0:
            player_draw_x += random.randint(-8, 8)
            self.player_hit_timer -= 1
        
        # Personagens
        player.draw(screen, player_draw_x, player.y)
        boss.draw(screen, boss_draw_x, boss.y)
        
        # Spells
        player_spell = self.game_objects["player_spell"]
        boss_spell = self.game_objects["boss_spell"]
        
        if player_spell.active:
            screen.blit(spell_img, (player_spell.x, player_spell.y))
        
        if boss_spell.active:
            pygame.draw.circle(screen, RED, (int(boss_spell.x), int(boss_spell.y)), 28)
            pygame.draw.circle(screen, YELLOW, (int(boss_spell.x), int(boss_spell.y)), 12)
        
        # UI
        self.battle_ui.draw_health(screen)
        self.battle_ui.draw_logic_puzzle(
            screen,
            *self.game_objects["round"].get_values()
        )
        self.battle_ui.draw_buttons(screen)
        self.battle_ui.draw_turn_message(screen)
        
        # Fim de jogo
        if self.game_over:
            if boss.hp <= 0:
                EndGameUI.draw_victory(screen)
            else:
                EndGameUI.draw_defeat(screen)
