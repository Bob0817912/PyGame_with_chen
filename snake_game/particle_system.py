"""
粒子效果系统
"""

import pygame
import random
import math
from typing import List, Tuple

class ParticleEffect:
    """粒子效果系统"""
    
    def __init__(self):
        self.particles = []
    
    def add_explosion(self, x: int, y: int, color: Tuple[int, int, int], count: int = 15):
        """添加爆炸效果"""
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(50, 150)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            
            self.particles.append({
                'x': x, 'y': y, 'vx': vx, 'vy': vy,
                'color': color, 'life': 1.0, 'size': random.uniform(2, 6)
            })
    
    def add_trail(self, x: int, y: int, color: Tuple[int, int, int]):
        """添加尾迹效果"""
        for _ in range(3):
            vx = random.uniform(-20, 20)
            vy = random.uniform(-20, 20)
            
            self.particles.append({
                'x': x + random.uniform(-5, 5), 
                'y': y + random.uniform(-5, 5),
                'vx': vx, 'vy': vy,
                'color': color, 'life': 0.5, 'size': random.uniform(1, 3)
            })
    
    def update(self, dt: float):
        """更新粒子"""
        for particle in self.particles[:]:
            particle['x'] += particle['vx'] * dt
            particle['y'] += particle['vy'] * dt
            particle['life'] -= dt * 2
            particle['size'] *= 0.98
            
            if particle['life'] <= 0:
                self.particles.remove(particle)
    
    def render(self, screen: pygame.Surface):
        """渲染粒子"""
        for particle in self.particles:
            alpha = max(0, min(255, int(particle['life'] * 255)))
            color = (*particle['color'], alpha)
            
            if alpha > 0:
                size = max(1, int(particle['size']))
                pos = (int(particle['x']), int(particle['y']))
                
                # 使用临时表面来实现透明度
                temp_surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
                pygame.draw.circle(temp_surface, color, (size, size), size)
                screen.blit(temp_surface, (pos[0] - size, pos[1] - size))
