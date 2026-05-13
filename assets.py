"""
Carregamento de recursos (imagens e sons)
"""
import pygame
from config import WIDTH, HEIGHT

# ================= IMAGENS =================
def load_image(path, size=None):
    """Carrega e redimensiona uma imagem"""
    img = pygame.image.load(path).convert_alpha()
    if size:
        img = pygame.transform.scale(img, size)
    return img


def load_image_convert(path, size=None):
    """Carrega imagem com convert() para melhor performance"""
    img = pygame.image.load(path).convert()
    if size:
        img = pygame.transform.scale(img, size)
    return img


# Backgrounds
background = load_image_convert("assets/parallax-mountain-bg.png", (WIDTH, HEIGHT))
world_bg = load_image_convert("assets/world.png", (WIDTH, HEIGHT))
dialogue_img = load_image("assets/dialogue.png", (WIDTH, HEIGHT))

# Personagens
player_img = load_image("assets/download.jpeg", (220, 220))
boss_img = load_image("assets/boss-preview.png", (280, 280))
npc_img = load_image("assets/npc.jpeg", (200, 200))

# Player no mundo
try:
    player_world_img = load_image("assets/player.png", (80, 80))
except:
    print("ERRO AO CARREGAR PLAYER.PNG")
    player_world_img = pygame.Surface((80, 80))
    from config import BLUE
    player_world_img.fill(BLUE)

# Spells
spell_img = load_image("assets/spell.jpg", (64, 64))

# ================= SONS =================
def load_sound(path):
    """Carrega um efeito sonoro"""
    return pygame.mixer.Sound(path)


spell_sound = load_sound("assets/sounds/spell.wav")
hit_sound = load_sound("assets/sounds/hit.wav")
dialogue_sound = load_sound("assets/sounds/dialogue.wav")
victory_sound = load_sound("assets/sounds/victory.wav")

# Música de fundo
pygame.mixer.music.load("assets/sounds/battle.wav")
pygame.mixer.music.set_volume(0.15)
pygame.mixer.music.play(-1)
