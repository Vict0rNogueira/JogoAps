"""
Lógica de jogo (geradores, sistema de regras)
"""
import random


class LogicPuzzle:
    """Sistema de expressões lógicas"""
    
    @staticmethod
    def generate():
        """Gera uma nova expressão lógica (P AND Q) OR R"""
        p = random.choice([True, False])
        q = random.choice([True, False])
        r = random.choice([True, False])
        
        # (P AND Q) OR R
        answer = (p and q) or r
        
        return p, q, r, answer
    
    @staticmethod
    def get_expression():
        """Retorna a expressão em formato de string"""
        return "(P AND Q) OR R"
    
    @staticmethod
    def check_answer(player_answer, correct_answer):
        """Verifica se resposta está correta"""
        return player_answer == correct_answer


class GameRound:
    """Gerencia uma rodada de jogo"""
    
    def __init__(self):
        self.p = False
        self.q = False
        self.r = False
        self.correct_answer = False
        self.generate_new()
    
    def generate_new(self):
        """Gera nova rodada"""
        self.p, self.q, self.r, self.correct_answer = LogicPuzzle.generate()
    
    def check(self, answer):
        """Verifica resposta do jogador"""
        return LogicPuzzle.check_answer(answer, self.correct_answer)
    
    def get_values(self):
        """Retorna valores P, Q, R"""
        return self.p, self.q, self.r
    
    def get_correct_answer(self):
        """Retorna resposta correta"""
        return self.correct_answer
