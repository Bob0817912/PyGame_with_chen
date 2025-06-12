"""
蛇皮肤系统
"""

import pygame
import random
import math
from typing import Tuple

class SnakeSkin:
    """蛇皮肤系统"""
    
    def __init__(self):
        self.skins = {
            'classic': {
                'head': (0, 255, 0),
                'body': (0, 200, 0),
                'pattern': None
            },
            'rainbow': {
                'head': (255, 0, 0),
                'body': None,  # 动态彩虹色
                'pattern': 'rainbow'
            },
            'neon': {
                'head': (0, 255, 255),
                'body': (0, 150, 255),
                'pattern': 'glow'
            },
            'fire': {
                'head': (255, 100, 0),
                'body': (255, 50, 0),
                'pattern': 'fire'
            },
            'ice': {
                'head': (150, 200, 255),
                'body': (100, 150, 255),
                'pattern': 'ice'
            },
            'galaxy': {
                'head': (100, 0, 200),
                'body': (50, 0, 150),
                'pattern': 'stars'
            }
        }
        self.current_skin = 'classic'
    
    def get_body_color(self, segment_index: int, total_segments: int, time: float) -> Tuple[int, int, int]:
        """获取身体段的颜色"""
        skin = self.skins[self.current_skin]
        
        if skin['pattern'] == 'rainbow':
            # 彩虹效果
            hue = (segment_index / max(1, total_segments) + time * 0.5) % 1.0
            rgb = pygame.Color(0, 0, 0)
            rgb.hsva = (hue * 360, 100, 100, 100)
            return (rgb.r, rgb.g, rgb.b)
        
        elif skin['pattern'] == 'fire':
            # 火焰效果
            intensity = 1.0 - (segment_index / max(1, total_segments))
            r = int(255 * intensity)
            g = int(100 * intensity * (0.5 + 0.5 * math.sin(time * 5 + segment_index)))
            b = 0
            return (r, g, b)
        
        elif skin['pattern'] == 'ice':
            # 冰霜效果
            base_color = skin['body']
            flicker = 0.8 + 0.2 * math.sin(time * 3 + segment_index * 0.5)
            return tuple(int(c * flicker) for c in base_color)
        
        else:
            return skin['body'] or (0, 200, 0)
    
    def render_segment(self, screen: pygame.Surface, rect: pygame.Rect, 
                      is_head: bool, segment_index: int, total_segments: int, time: float):
        """渲染蛇的一段"""
        skin = self.skins[self.current_skin]
        
        if is_head:
            color = skin['head']
            # 头部特效
            if skin['pattern'] == 'glow':
                # 发光效果
                for i in range(3):
                    glow_rect = rect.inflate(i * 4, i * 4)
                    alpha = 100 - i * 30
                    temp_surface = pygame.Surface(glow_rect.size, pygame.SRCALPHA)
                    pygame.draw.rect(temp_surface, (*color, alpha), 
                                   (0, 0, glow_rect.width, glow_rect.height), border_radius=5)
                    screen.blit(temp_surface, glow_rect.topleft)
            
            pygame.draw.rect(screen, color, rect, border_radius=8)
            
            # 眼睛
            eye_size = rect.width // 6
            eye_y = rect.centery - eye_size // 2
            left_eye = (rect.centerx - rect.width // 4, eye_y)
            right_eye = (rect.centerx + rect.width // 4, eye_y)
            
            pygame.draw.circle(screen, (255, 255, 255), left_eye, eye_size)
            pygame.draw.circle(screen, (255, 255, 255), right_eye, eye_size)
            pygame.draw.circle(screen, (0, 0, 0), left_eye, eye_size // 2)
            pygame.draw.circle(screen, (0, 0, 0), right_eye, eye_size // 2)
            
        else:
            color = self.get_body_color(segment_index, total_segments, time)
            
            # 身体特效
            if skin['pattern'] == 'glow':
                # 发光效果
                glow_rect = rect.inflate(2, 2)
                temp_surface = pygame.Surface(glow_rect.size, pygame.SRCALPHA)
                pygame.draw.rect(temp_surface, (*color, 80), 
                               (0, 0, glow_rect.width, glow_rect.height), border_radius=5)
                screen.blit(temp_surface, glow_rect.topleft)
            
            pygame.draw.rect(screen, color, rect, border_radius=5)
            
            # 纹理效果
            if skin['pattern'] == 'stars':
                if random.random() < 0.1:  # 10%概率显示星星
                    star_x = rect.centerx + random.randint(-rect.width//4, rect.width//4)
                    star_y = rect.centery + random.randint(-rect.height//4, rect.height//4)
                    pygame.draw.circle(screen, (255, 255, 255), (star_x, star_y), 1)
