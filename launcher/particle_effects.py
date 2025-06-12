"""
启动器粒子效果系统
"""

import pygame
import random
from typing import Tuple

class Particle:
    """粒子效果类"""
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)
        self.life = random.uniform(2, 4)
        self.max_life = self.life
        self.size = random.uniform(1, 3)
        
    def update(self, dt: float):
        self.x += self.vx * dt * 50
        self.y += self.vy * dt * 50
        self.life -= dt
        
    def draw(self, screen: pygame.Surface, particle_color: Tuple[int, int, int]):
        if self.life > 0:
            alpha = int((self.life / self.max_life) * 100)
            color = (*particle_color, alpha)
            size = max(1, int(self.size * (self.life / self.max_life)))
            
            # 创建临时表面用于透明度
            temp_surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            pygame.draw.circle(temp_surface, color, (size, size), size)
            screen.blit(temp_surface, (int(self.x - size), int(self.y - size)))
