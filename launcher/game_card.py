"""
游戏卡片系统
"""

import pygame
import math
import time
import random
import subprocess
import sys
import os
from typing import Tuple

class GameCard:
    """游戏卡片类"""
    def __init__(self, x: int, y: int, width: int, height: int, 
                 title: str, description: str, icon_color: Tuple[int, int, int],
                 game_file: str, colors: dict):
        self.rect = pygame.Rect(x, y, width, height)
        self.title = title
        self.description = description
        self.icon_color = icon_color
        self.game_file = game_file
        self.colors = colors
        self.hover = False
        self.hover_scale = 1.0
        self.target_scale = 1.0
        self.glow_intensity = 0.0
        
    def update(self, dt: float, mouse_pos: Tuple[int, int]):
        # 检测鼠标悬停
        self.hover = self.rect.collidepoint(mouse_pos)
        self.target_scale = 1.05 if self.hover else 1.0
        
        # 平滑缩放动画
        self.hover_scale += (self.target_scale - self.hover_scale) * dt * 8
        
        # 发光效果
        if self.hover:
            self.glow_intensity = min(1.0, self.glow_intensity + dt * 4)
        else:
            self.glow_intensity = max(0.0, self.glow_intensity - dt * 4)
    
    def draw(self, screen: pygame.Surface, font_title: pygame.font.Font, 
             font_desc: pygame.font.Font):
        # 计算缩放后的矩形
        scaled_width = int(self.rect.width * self.hover_scale)
        scaled_height = int(self.rect.height * self.hover_scale)
        scaled_x = self.rect.centerx - scaled_width // 2
        scaled_y = self.rect.centery - scaled_height // 2
        scaled_rect = pygame.Rect(scaled_x, scaled_y, scaled_width, scaled_height)
        
        # 发光效果
        if self.glow_intensity > 0:
            glow_size = 10
            glow_alpha = int(self.glow_intensity * 50)
            for i in range(glow_size):
                glow_rect = scaled_rect.inflate(i * 4, i * 4)
                glow_surface = pygame.Surface(glow_rect.size, pygame.SRCALPHA)
                glow_color = (*self.colors['accent'], max(0, glow_alpha - i * 5))
                pygame.draw.rect(glow_surface, glow_color, 
                               (0, 0, glow_rect.width, glow_rect.height), 
                               border_radius=15)
                screen.blit(glow_surface, glow_rect.topleft)
        
        # 卡片背景
        card_color = self.colors['card_hover'] if self.hover else self.colors['card_bg']
        pygame.draw.rect(screen, card_color, scaled_rect, border_radius=15)
        
        # 卡片边框
        border_color = self.colors['accent'] if self.hover else self.colors['card_border']
        pygame.draw.rect(screen, border_color, scaled_rect, width=2, border_radius=15)
        
        # 绘制图标
        self.draw_icon(screen, scaled_rect)
        
        # 标题
        title_surface = font_title.render(self.title, True, self.colors['text_primary'])
        title_rect = title_surface.get_rect()
        title_rect.centerx = scaled_rect.centerx
        title_rect.y = scaled_rect.y + scaled_rect.height * 0.6
        screen.blit(title_surface, title_rect)
        
        # 描述
        desc_surface = font_desc.render(self.description, True, self.colors['text_secondary'])
        desc_rect = desc_surface.get_rect()
        desc_rect.centerx = scaled_rect.centerx
        desc_rect.y = title_rect.bottom + 10
        screen.blit(desc_surface, desc_rect)
        
        # 悬停时显示启动提示
        if self.hover:
            hint_surface = font_desc.render("点击启动游戏", True, self.colors['accent_hover'])
            hint_rect = hint_surface.get_rect()
            hint_rect.centerx = scaled_rect.centerx
            hint_rect.y = desc_rect.bottom + 15
            screen.blit(hint_surface, hint_rect)
    
    def draw_icon(self, screen: pygame.Surface, rect: pygame.Rect):
        """绘制游戏图标"""
        icon_size = min(rect.width, rect.height) // 3
        icon_center = (rect.centerx, rect.y + rect.height * 0.3)
        
        if "snake" in self.game_file.lower() or "first" in self.game_file:
            # 绘制蛇形图标
            self.draw_snake_icon(screen, icon_center, icon_size)
        else:
            # 绘制火柴人图标
            self.draw_stickman_icon(screen, icon_center, icon_size)
    
    def draw_snake_icon(self, screen: pygame.Surface, center: Tuple[int, int], size: int):
        """绘制蛇形图标"""
        # 蛇身
        segments = 6
        for i in range(segments):
            angle = (time.time() * 2 + i * 0.5) % (2 * math.pi)
            x = center[0] + math.cos(angle) * (size // 4) * (1 - i * 0.1)
            y = center[1] + math.sin(angle) * (size // 6) + i * (size // 8)
            
            segment_size = max(3, size // 8 - i)
            color_intensity = 255 - i * 30
            segment_color = (0, max(100, color_intensity), 0)
            
            pygame.draw.circle(screen, segment_color, (int(x), int(y)), segment_size)
        
        # 蛇头
        head_x = center[0] + math.cos(time.time() * 2) * (size // 4)
        head_y = center[1] + math.sin(time.time() * 2) * (size // 6)
        pygame.draw.circle(screen, self.colors['snake_green'], (int(head_x), int(head_y)), size // 6)
        
        # 眼睛
        eye_size = 2
        pygame.draw.circle(screen, (255, 255, 255), 
                         (int(head_x - 3), int(head_y - 2)), eye_size)
        pygame.draw.circle(screen, (255, 255, 255), 
                         (int(head_x + 3), int(head_y - 2)), eye_size)
    
    def draw_stickman_icon(self, screen: pygame.Surface, center: Tuple[int, int], size: int):
        """绘制火柴人图标"""
        # 动画偏移
        bounce = math.sin(time.time() * 4) * 3
        
        # 头部
        head_y = center[1] - size // 3 + bounce
        pygame.draw.circle(screen, self.icon_color, (center[0], int(head_y)), size // 8)
        
        # 身体
        body_start = (center[0], int(head_y + size // 8))
        body_end = (center[0], int(center[1] + size // 6 + bounce))
        pygame.draw.line(screen, self.icon_color, body_start, body_end, 3)
        
        # 手臂 (带动画)
        arm_angle = math.sin(time.time() * 3) * 0.3
        arm_length = size // 4
        left_arm_end = (center[0] - int(arm_length * math.cos(arm_angle)), 
                       int(center[1] - size // 8 + arm_length * math.sin(arm_angle) + bounce))
        right_arm_end = (center[0] + int(arm_length * math.cos(arm_angle)), 
                        int(center[1] - size // 8 - arm_length * math.sin(arm_angle) + bounce))
        
        pygame.draw.line(screen, self.icon_color, 
                        (center[0], int(center[1] - size // 8 + bounce)), left_arm_end, 3)
        pygame.draw.line(screen, self.icon_color, 
                        (center[0], int(center[1] - size // 8 + bounce)), right_arm_end, 3)
        
        # 腿部
        leg_length = size // 4
        left_leg_end = (center[0] - leg_length // 2, int(center[1] + size // 3 + bounce))
        right_leg_end = (center[0] + leg_length // 2, int(center[1] + size // 3 + bounce))
        
        pygame.draw.line(screen, self.icon_color, body_end, left_leg_end, 3)
        pygame.draw.line(screen, self.icon_color, body_end, right_leg_end, 3)
    
    def is_clicked(self, mouse_pos: Tuple[int, int]) -> bool:
        """检查是否被点击"""
        return self.rect.collidepoint(mouse_pos)
    
    def launch_game(self):
        """启动游戏"""
        try:
            if os.path.exists(self.game_file):
                subprocess.Popen([sys.executable, self.game_file])
                return True
            else:
                print(f"游戏文件不存在: {self.game_file}")
                return False
        except Exception as e:
            print(f"启动游戏失败: {e}")
            return False
