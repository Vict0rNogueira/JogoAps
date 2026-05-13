"""
Sistema de UI (desenho de elementos visuais)
"""
import pygame
from config import (
    WIDTH, HEIGHT, font, big_font, WHITE, BLACK, RED, GREEN,
    BLUE, YELLOW, TRUE_BUTTON_WIDTH, TRUE_BUTTON_HEIGHT,
    FALSE_BUTTON_WIDTH, FALSE_BUTTON_HEIGHT, PLAYER_BATTLE_X,
    PLAYER_BATTLE_Y, BOSS_BATTLE_X, BOSS_BATTLE_Y
)


class UIButton:
    """Classe para botões de UI"""
    
    def __init__(self, x, y, width, height, text, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
    
    def draw(self, screen):
        """Desenha o botão"""
        pygame.draw.rect(screen, self.color, self.rect, border_radius=12)
        text_surface = font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
    
    def is_clicked(self, pos):
        """Verifica se foi clicado"""
        return self.rect.collidepoint(pos)


class HealthBar:
    """Classe para barras de vida"""
    
    def __init__(self, x, y, max_hp):
        self.x = x
        self.y = y
        self.max_hp = max_hp
        self.current_hp = max_hp
        self.width = 400
        self.height = 35
    
    def update_hp(self, hp):
        """Atualiza HP"""
        self.current_hp = max(0, hp)
    
    def draw(self, screen, label):
        """Desenha barra de vida"""
        # Fundo vermelho
        pygame.draw.rect(screen, RED, (self.x, self.y, self.width, self.height))
        
        # Barra verde
        health_width = (self.current_hp / self.max_hp) * self.width
        pygame.draw.rect(screen, GREEN, (self.x, self.y, health_width, self.height))
        
        # Texto
        text = f"{label} HP: {self.current_hp}"
        draw_text(text, font, WHITE, self.x, self.y + 8)


def draw_text(text, font_obj, color, x, y):
    """Renderiza texto na tela"""
    render = font_obj.render(text, True, color)
    from config import screen
    screen.blit(render, (x, y))


class BattleUI:
    """Gerenciador de UI da batalha"""
    
    def __init__(self):
        self.true_button = UIButton(
            WIDTH // 2 - 260,
            HEIGHT - 120,
            TRUE_BUTTON_WIDTH,
            TRUE_BUTTON_HEIGHT,
            "TRUE",
            GREEN
        )
        
        self.false_button = UIButton(
            WIDTH // 2 + 60,
            HEIGHT - 120,
            FALSE_BUTTON_WIDTH,
            FALSE_BUTTON_HEIGHT,
            "FALSE",
            RED
        )
        
        self.player_health = HealthBar(60, 40, 100)
        self.boss_health = HealthBar(WIDTH - 460, 40, 100)
        
        self.turn_message = ""
        self.restart_button = UIButton(
            WIDTH // 2 - 260,
            HEIGHT // 2 + 80,
            200,
            70,
            "Reiniciar",
            GREEN
        )
        self.quit_button = UIButton(
            WIDTH // 2 + 60,
            HEIGHT // 2 + 80,
            200,
            70,
            "Sair",
            RED
        )
    
    def update_message(self, message):
        """Atualiza mensagem de turno"""
        self.turn_message = message
    
    def set_player_hp(self, hp):
        """Define HP do player"""
        self.player_health.update_hp(hp)
    
    def set_boss_hp(self, hp):
        """Define HP do boss"""
        self.boss_health.update_hp(hp)
    
    def draw_buttons(self, screen):
        """Desenha botões"""
        self.true_button.draw(screen)
        self.false_button.draw(screen)
    
    def draw_health(self, screen):
        """Desenha barras de vida"""
        self.player_health.draw(screen, "Player")
        self.boss_health.draw(screen, "Boss")
    
    def draw_logic_puzzle(self, screen, p, q, r):
        """Desenha expressão lógica"""
        expression = "(P AND Q) OR R"
        
        expression_surface = big_font.render(expression, True, YELLOW)
        expression_rect = expression_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40))
        screen.blit(expression_surface, expression_rect)
        
        # Valores
        draw_text(f"P = {p}", font, BLACK, WIDTH // 2 - 180, HEIGHT // 2 + 20)
        draw_text(f"Q = {q}", font, BLACK, WIDTH // 2 - 20, HEIGHT // 2 + 20)
        draw_text(f"R = {r}", font, BLACK, WIDTH // 2 + 140, HEIGHT // 2 + 20)
    
    def draw_turn_message(self, screen):
        """Desenha mensagem de turno"""
        draw_text(
            self.turn_message,
            font,
            YELLOW,
            WIDTH // 2 - 150,
            HEIGHT // 2 + 130
        )
    
    def get_button_at_pos(self, pos):
        """Retorna qual botão foi clicado"""
        if self.true_button.is_clicked(pos):
            return True
        if self.false_button.is_clicked(pos):
            return False
        return None

    def draw_defeat_buttons(self, screen):
        """Desenha botões de derrota"""
        self.restart_button.draw(screen)
        self.quit_button.draw(screen)

    def get_defeat_button_at_pos(self, pos):
        """Retorna qual botão de derrota foi clicado"""
        if self.restart_button.is_clicked(pos):
            return "restart"
        if self.quit_button.is_clicked(pos):
            return "quit"
        return None


class WorldUI:
    """UI do mundo"""
    
    @staticmethod
    def draw_controls(screen):
        """Desenha controles"""
        draw_text("Use WASD para mover", font, WHITE, 40, 40)
        draw_text("Aproxime-se do NPC e aperte E", font, WHITE, 40, 80)


class DialogueUI:
    """UI de diálogo"""
    
    @staticmethod
    def draw_dialogue(screen, npc_name, dialogue_text):
        """Desenha interface de diálogo"""
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
        
        draw_text(npc_name, font, YELLOW, 120, HEIGHT - 135)
        draw_text(dialogue_text, font, WHITE, 120, HEIGHT - 95)
        draw_text("SPACE para continuar", font, GREEN, WIDTH - 380, HEIGHT - 70)


class EndGameUI:
    """UI de fim de jogo"""
    
    @staticmethod
    def draw_victory(screen):
        """Desenha tela de vitória"""
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        
        victory = big_font.render("VOCÊ DERROTOU O BOSS!", True, GREEN)
        rect = victory.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(victory, rect)
    
    @staticmethod
    def draw_defeat(screen):
        """Desenha tela de derrota"""
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        
        defeat = big_font.render("VOCÊ FOI DERROTADO!", True, RED)
        rect = defeat.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(defeat, rect)
