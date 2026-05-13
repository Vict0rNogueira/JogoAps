"""
Entidades do jogo (Player, Boss, NPC)
"""
import pygame
from config import (
    WIDTH, HEIGHT, PLAYER_SPEED, PLAYER_BATTLE_X, PLAYER_BATTLE_Y,
    BOSS_BATTLE_X, BOSS_BATTLE_Y, PLAYER_MAX_HP, BOSS_MAX_HP,
    SPELL_SPEED, PLAYER_SPELL_DAMAGE, BOSS_SPELL_DAMAGE
)


class Player:
    """Classe do jogador"""
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.hp = PLAYER_MAX_HP
        self.max_hp = PLAYER_MAX_HP
        self.speed = PLAYER_SPEED
        self.rect = pygame.Rect(x, y, 80, 80)
        
    def update_position(self, keys):
        """Atualiza posição baseado em teclas"""
        if keys[pygame.K_w]:
            self.y -= self.speed
        if keys[pygame.K_s]:
            self.y += self.speed
        if keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_d]:
            self.x += self.speed
        
        # Limites do mapa
        self.x = max(0, min(self.x, WIDTH - 80))
        self.y = max(0, min(self.y, HEIGHT - 80))
        
        self.rect.x = self.x
        self.rect.y = self.y
    
    def draw(self, screen, x, y):
        """Desenha o jogador"""
        screen.blit(self.img, (x, y))
    
    def take_damage(self, damage):
        """Reduz HP do jogador"""
        self.hp -= damage
        self.hp = max(0, self.hp)
    
    def heal(self, amount):
        """Recupera HP"""
        self.hp += amount
        self.hp = min(self.max_hp, self.hp)
    
    def is_alive(self):
        """Verifica se está vivo"""
        return self.hp > 0


class Boss:
    """Classe do chefe"""
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.hp = BOSS_MAX_HP
        self.max_hp = BOSS_MAX_HP
        self.rect = pygame.Rect(x, y, 280, 280)
    
    def draw(self, screen, x, y):
        """Desenha o chefe"""
        screen.blit(self.img, (x, y))
    
    def take_damage(self, damage):
        """Reduz HP do chefe"""
        self.hp -= damage
        self.hp = max(0, self.hp)
    
    def is_alive(self):
        """Verifica se está vivo"""
        return self.hp > 0


class Spell:
    """Classe de magia/projétil"""
    def __init__(self, x, y, target_x, is_player_spell=True):
        self.start_x = x
        self.start_y = y
        self.x = x
        self.y = y
        self.target_x = target_x
        self.is_player_spell = is_player_spell
        self.speed = SPELL_SPEED
        self.damage = PLAYER_SPELL_DAMAGE if is_player_spell else BOSS_SPELL_DAMAGE
        self.active = False
    
    def launch(self):
        """Ativa a magia e posiciona no ponto inicial"""
        self.x = self.start_x
        self.y = self.start_y
        self.active = True
    
    def reset(self):
        """Desativa a magia e retorna ao ponto inicial"""
        self.x = self.start_x
        self.y = self.start_y
        self.active = False
    
    def update(self):
        """Atualiza posição da magia"""
        if self.is_player_spell:
            self.x += self.speed
            if self.x >= self.target_x:
                self.active = False
        else:
            self.x -= self.speed
            if self.x <= self.target_x:
                self.active = False
    
    def is_hit(self):
        """Verifica se acertou o alvo"""
        return not self.active


class NPC:
    """Classe de NPC"""
    def __init__(self, x, y, img, width=100, height=140):
        self.x = x
        self.y = y
        self.img = img
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.dialogues = [
            "Então voce chegou...",
            "Vamos ver se você é outro burro...",
            "Ou se prestou atenção na merda da aula.",
            "Agora faz essa porra ai!!!!!!",
        ]
        self.name = "Professor Silvio"
    
    def draw(self, screen):
        """Desenha o NPC"""
        screen.blit(self.img, (self.x, self.y))
    
    def is_nearby(self, player_rect):
        """Verifica se jogador está próximo"""
        interaction_rect = self.rect.inflate(80, 80)
        return player_rect.colliderect(interaction_rect)
    
    def get_dialogue(self, index):
        """Retorna diálogo específico"""
        if index < len(self.dialogues):
            return self.dialogues[index]
        return ""
    
    def has_more_dialogue(self, index):
        """Verifica se há mais diálogos"""
        return index < len(self.dialogues)


class VictoryDialogue:
    """Gerencia diálogos de vitória após vencer a batalha"""
    def __init__(self, npc_img):
        self.img = npc_img
        self.name = "Professor Silvio"
        
        # =================Adicione novas falas de vitória =================
        self.victory_dialogues = [
            "Parabéns, você conseguiu!",
            "Finalmente alguém que presta atenção!",
            "E não vai repetir 3 vezes a mesma cadeira.",
            "Agora vaza daqui seu bosta.",
        ]
        # =================================================================================
    
    def get_dialogue(self, index):
        """Retorna diálogo específico"""
        if index < len(self.victory_dialogues):
            return self.victory_dialogues[index]
        return ""
    
    def has_more_dialogue(self, index):
        """Verifica se há mais diálogos"""
        return index < len(self.victory_dialogues)
    def draw(self, screen):
        """Desenha o NPC"""
        screen.blit(self.img, (WIDTH // 2 - 100, HEIGHT // 2 - 300))
