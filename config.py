"""
Configurações globais do jogo
"""
import pygame

# ================= DISPLAY =================
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()

pygame.display.set_caption("Boolean Battle RPG")
clock = pygame.time.Clock()

# ================= FONTES =================
font = pygame.font.SysFont("Arial", 28)
big_font = pygame.font.SysFont("Arial", 42)

# ================= CORES =================
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
RED = (220, 60, 60)
GREEN = (60, 220, 120)
BLUE = (60, 120, 255)
YELLOW = (255, 220, 0)

# ================= POSIÇÕES BATALHA =================
PLAYER_BATTLE_X = 120
PLAYER_BATTLE_Y = HEIGHT - 440

BOSS_BATTLE_X = WIDTH - 420
BOSS_BATTLE_Y = HEIGHT - 470

# ================= NPC =================
NPC_X = WIDTH // 2 + 300
NPC_Y = HEIGHT // 2 - 50
NPC_WIDTH = 100
NPC_HEIGHT = 140

# ================= MOVIMENTO =================
PLAYER_SPEED = 7

# ================= SPELLS =================
SPELL_SPEED = 18
PLAYER_SPELL_DAMAGE = 25
BOSS_SPELL_DAMAGE = 15

# ================= HP =================
PLAYER_MAX_HP = 100
BOSS_MAX_HP = 100

# ================= BOTÕES =================
TRUE_BUTTON_WIDTH = 200
TRUE_BUTTON_HEIGHT = 70
FALSE_BUTTON_WIDTH = 200
FALSE_BUTTON_HEIGHT = 70
