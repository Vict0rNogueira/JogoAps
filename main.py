import pygame
import random
import sys

pygame.init()
pygame.mixer.init()

# ================= CONFIG =================
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

# ================= GAME STATE =================
game_state = "world"

# ================= CARREGAR IMAGENS =================
background = pygame.image.load(
    "assets/parallax-mountain-bg.png"
).convert()

background = pygame.transform.scale(background, (WIDTH, HEIGHT))

world_bg = pygame.image.load(
    "assets/world.png"
).convert()

world_bg = pygame.transform.scale(world_bg, (WIDTH, HEIGHT))

player_img = pygame.image.load(
    "assets/download.jpeg"
).convert_alpha()

player_img = pygame.transform.scale(player_img, (220, 220))

boss_img = pygame.image.load(
    "assets/boss-preview.png"
).convert_alpha()

boss_img = pygame.transform.scale(boss_img, (280, 280))

spell_img = pygame.image.load(
    "assets/spell.jpg"
).convert_alpha()

spell_img = pygame.transform.scale(spell_img, (64, 64))

npc_img = pygame.image.load(
    "assets/npc.jpeg"
).convert_alpha()

npc_img = pygame.transform.scale(npc_img, (200, 200))

dialogue_img = pygame.image.load(
    "assets/dialogue.png"
).convert_alpha()

dialogue_img = pygame.transform.scale(
    dialogue_img,
    (WIDTH, HEIGHT)
)

# ================= PLAYER WORLD IMG =================
try:

    player_world_img = pygame.image.load(
        "assets/player.png"
    ).convert_alpha()

    player_world_img = pygame.transform.scale(
        player_world_img,
        (80, 80)
    )

except:

    print("ERRO AO CARREGAR PLAYER.PNG")

    player_world_img = pygame.Surface((80, 80))
    player_world_img.fill(BLUE)

# ================= SONS =================
spell_sound = pygame.mixer.Sound(
    "assets/sounds/spell.wav"
)

hit_sound = pygame.mixer.Sound(
    "assets/sounds/hit.wav"
)

dialogue_sound = pygame.mixer.Sound(
    "assets/sounds/dialogue.wav"
)

victory_sound = pygame.mixer.Sound(
    "assets/sounds/victory.wav"
)

pygame.mixer.music.load(
    "assets/sounds/battle.wav"
)

pygame.mixer.music.set_volume(0.15)
pygame.mixer.music.play(-1)

# ================= PLAYER WORLD =================
player_world_x = WIDTH // 2
player_world_y = HEIGHT // 2

player_speed = 7

# ================= NPC =================
npc_rect = pygame.Rect(
    WIDTH // 2 + 300,
    HEIGHT // 2 - 50,
    100,
    140
)

# ================= POSIÇÕES BATALHA =================
player_x = 120
player_y = HEIGHT - 440

boss_x = WIDTH - 420
boss_y = HEIGHT - 470

# ================= SPELL PLAYER =================
spell_active = False

spell_x = player_x + 120
spell_y = player_y + 50

spell_speed = 18

# ================= SPELL BOSS =================
boss_spell_active = False

boss_spell_x = boss_x - 40
boss_spell_y = boss_y + 100

boss_spell_speed = 18

# ================= HP =================
player_hp = 100
boss_hp = 100

# ================= FLAGS =================
victory_played = False
game_over = False

# ================= SISTEMA LÓGICO =================
def generate_logic():

    p = random.choice([True, False])
    q = random.choice([True, False])
    r = random.choice([True, False])

    answer = (p and q) or r

    return p, q, r, answer

p, q, r, correct_answer = generate_logic()

# ================= BOTÕES =================
true_button = pygame.Rect(
    WIDTH // 2 - 260,
    HEIGHT - 120,
    200,
    70
)

false_button = pygame.Rect(
    WIDTH // 2 + 60,
    HEIGHT - 120,
    200,
    70
)

# ================= MENSAGENS =================
message = "Resolva a expressão lógica!"
turn_message = ""

# ================= DIÁLOGOS =================
npc_dialogue = [
    "Então voce chegou...",
    "Vamos ver se você é outro burro...",
    "Ou se prestou atenção na merda da aula.",
    "Agora faz essa porra ai!!!!!!"
]

dialogue_index = 0

# ================= EFEITOS =================
boss_hit_timer = 0
player_hit_timer = 0

# ================= FUNÇÃO TEXTO =================
def draw_text(text, font, color, x, y):

    render = font.render(text, True, color)
    screen.blit(render, (x, y))

# ================= LOOP PRINCIPAL =================
running = True

while running:

    dt = clock.tick(120)

    # ================= EVENTOS =================
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            # SAIR
            if event.key == pygame.K_ESCAPE:
                running = False

            # ================= DIÁLOGO =================
            if game_state == "dialogue":

                if event.key == pygame.K_SPACE:

                    dialogue_sound.play()

                    dialogue_index += 1

                    if dialogue_index >= len(npc_dialogue):

                        pygame.time.delay(300)

                        game_state = "battle"

            # ================= INTERAÇÃO NPC =================
            if event.key == pygame.K_e:

                if game_state == "world":

                    player_rect = pygame.Rect(
                        player_world_x,
                        player_world_y,
                        80,
                        80
                    )

                    interaction_rect = npc_rect.inflate(80, 80)

                    if player_rect.colliderect(interaction_rect):

                        game_state = "dialogue"
                        dialogue_index = 0

        # ================= CLIQUE BATALHA =================
        if event.type == pygame.MOUSEBUTTONDOWN:

            if game_state == "battle":

                mouse_pos = pygame.mouse.get_pos()

                player_choice = None

                if true_button.collidepoint(mouse_pos):
                    player_choice = True

                if false_button.collidepoint(mouse_pos):
                    player_choice = False

                if (
                    player_choice is not None
                    and not spell_active
                    and not boss_spell_active
                    and not game_over
                ):

                    if player_choice == correct_answer:

                        spell_active = True
                        spell_sound.play()

                        turn_message = "Magia lançada!"

                    else:

                        boss_spell_active = True
                        spell_sound.play()

                        turn_message = "O boss lançou magia!"

    # ================= MOVIMENTO =================
    keys = pygame.key.get_pressed()

    if game_state == "world":

        if keys[pygame.K_w]:
            player_world_y -= player_speed

        if keys[pygame.K_s]:
            player_world_y += player_speed

        if keys[pygame.K_a]:
            player_world_x -= player_speed

        if keys[pygame.K_d]:
            player_world_x += player_speed

        # LIMITES DO MAPA
        player_world_x = max(
            0,
            min(player_world_x, WIDTH - 80)
        )

        player_world_y = max(
            0,
            min(player_world_y, HEIGHT - 80)
        )

    # ================= BATALHA =================
    if game_state == "battle":

        # ================= MAGIA PLAYER =================
        if spell_active:

            spell_x += spell_speed

            if spell_x >= boss_x:

                boss_hp -= 25

                hit_sound.play()

                boss_hit_timer = 10

                spell_active = False

                spell_x = player_x + 120

                turn_message = "Ataque super efetivo!"

                p, q, r, correct_answer = generate_logic()

        # ================= MAGIA BOSS =================
        if boss_spell_active:

            boss_spell_x -= boss_spell_speed

            if boss_spell_x <= player_x + 120:

                player_hp -= 15

                hit_sound.play()

                player_hit_timer = 10

                boss_spell_active = False

                boss_spell_x = boss_x - 40

                turn_message = "Você recebeu dano!"

                p, q, r, correct_answer = generate_logic()

    # ================= EFEITOS =================
    boss_draw_x = boss_x
    player_draw_x = player_x

    if boss_hit_timer > 0:

        boss_draw_x += random.randint(-8, 8)

        boss_hit_timer -= 1

    if player_hit_timer > 0:

        player_draw_x += random.randint(-8, 8)

        player_hit_timer -= 1

    # ================= TELA MUNDO =================
    if game_state == "world":

        screen.blit(world_bg, (0, 0))

        # SOMBRA PLAYER
        pygame.draw.ellipse(
            screen,
            (0, 0, 0),
            (
                player_world_x + 10,
                player_world_y + 60,
                60,
                20
            )
        )

        # NPC
        screen.blit(
            npc_img,
            (npc_rect.x, npc_rect.y)
        )

        # PLAYER
        screen.blit(
            player_world_img,
            (player_world_x, player_world_y)
        )

        draw_text(
            "Use WASD para mover",
            font,
            WHITE,
            40,
            40
        )

        draw_text(
            "Aproxime-se do NPC e aperte E",
            font,
            WHITE,
            40,
            80
        )

    # ================= TELA DIÁLOGO =================
    if game_state == "dialogue":

        screen.blit(dialogue_img, (0, 0))

        pygame.draw.rect(
            screen,
            BLACK,
            (80, HEIGHT - 150, WIDTH - 160, 120),
            border_radius=16
        )

        pygame.draw.rect(
            screen,
            YELLOW,
            (80, HEIGHT - 150, WIDTH - 160, 120),
            4,
            border_radius=16
        )

        draw_text(
            "Professor Silvio",
            font,
            YELLOW,
            120,
            HEIGHT - 135
        )

        draw_text(
            npc_dialogue[dialogue_index],
            font,
            WHITE,
            120,
            HEIGHT - 95
        )

        draw_text(
            "SPACE para continuar",
            font,
            GREEN,
            WIDTH - 380,
            HEIGHT - 70
        )

    # ================= TELA BATALHA =================
    if game_state == "battle":

        screen.blit(background, (0, 0))

        # PERSONAGENS
        screen.blit(
            player_img,
            (player_draw_x, player_y)
        )

        screen.blit(
            boss_img,
            (boss_draw_x, boss_y)
        )

        # MAGIA PLAYER
        if spell_active:

            screen.blit(
                spell_img,
                (spell_x, spell_y)
            )

        # MAGIA BOSS
        if boss_spell_active:

            pygame.draw.circle(
                screen,
                RED,
                (boss_spell_x, boss_spell_y),
                28
            )

            pygame.draw.circle(
                screen,
                YELLOW,
                (boss_spell_x, boss_spell_y),
                12
            )

        # ================= HP =================
        pygame.draw.rect(
            screen,
            RED,
            (60, 40, 400, 35)
        )

        pygame.draw.rect(
            screen,
            GREEN,
            (60, 40, player_hp * 4, 35)
        )

        pygame.draw.rect(
            screen,
            RED,
            (WIDTH - 460, 40, 400, 35)
        )

        pygame.draw.rect(
            screen,
            GREEN,
            (WIDTH - 460, 40, boss_hp * 4, 35)
        )

        draw_text(
            f"Player HP: {player_hp}",
            font,
            WHITE,
            60,
            85
        )

        draw_text(
            f"Boss HP: {boss_hp}",
            font,
            WHITE,
            WIDTH - 460,
            85
        )

        # ================= EXPRESSÃO =================
        expression = "(P AND Q) OR R"

        expression_surface = big_font.render(
            expression,
            True,
            YELLOW
        )

        expression_rect = expression_surface.get_rect(
            center=(WIDTH // 2, HEIGHT // 2 - 40)
        )

        screen.blit(
            expression_surface,
            expression_rect
        )

        draw_text(
            f"P = {p}",
            font,
            BLACK,
            WIDTH // 2 - 180,
            HEIGHT // 2 + 20
        )

        draw_text(
            f"Q = {q}",
            font,
            BLACK,
            WIDTH // 2 - 20,
            HEIGHT // 2 + 20
        )

        draw_text(
            f"R = {r}",
            font,
            BLACK,
            WIDTH // 2 + 140,
            HEIGHT // 2 + 20
        )

        # ================= BOTÕES =================
        pygame.draw.rect(
            screen,
            GREEN,
            true_button,
            border_radius=12
        )

        pygame.draw.rect(
            screen,
            RED,
            false_button,
            border_radius=12
        )

        draw_text(
            "TRUE",
            font,
            BLACK,
            true_button.x + 60,
            true_button.y + 18
        )

        draw_text(
            "FALSE",
            font,
            BLACK,
            false_button.x + 55,
            false_button.y + 18
        )

        draw_text(
            turn_message,
            font,
            YELLOW,
            WIDTH // 2 - 150,
            HEIGHT // 2 + 130
        )

        # ================= VITÓRIA =================
        if boss_hp <= 0:

            game_over = True

            if not victory_played:

                victory_sound.play()
                victory_played = True

            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(180)
            overlay.fill(BLACK)

            screen.blit(overlay, (0, 0))

            victory = big_font.render(
                "VOCÊ DERROTOU O BOSS!",
                True,
                GREEN
            )

            rect = victory.get_rect(
                center=(WIDTH // 2, HEIGHT // 2)
            )

            screen.blit(victory, rect)

        # ================= DERROTA =================
        if player_hp <= 0:

            game_over = True

            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(180)
            overlay.fill(BLACK)

            screen.blit(overlay, (0, 0))

            defeat = big_font.render(
                "VOCÊ FOI DERROTADO!",
                True,
                RED
            )

            rect = defeat.get_rect(
                center=(WIDTH // 2, HEIGHT // 2)
            )

            screen.blit(defeat, rect)

    pygame.display.flip()

pygame.quit()
sys.exit()