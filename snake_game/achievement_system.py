"""
成就系统
"""

import pygame
import time

class AchievementSystem:
    """成就系统"""
    
    def __init__(self):
        self.achievements = {
            'first_food': {'name': '初尝甜头', 'description': '吃到第一个食物', 'unlocked': False},
            'speed_demon': {'name': '速度恶魔', 'description': '达到最高速度', 'unlocked': False},
            'century': {'name': '百食之王', 'description': '吃掉100个食物', 'unlocked': False},
            'survivor': {'name': '生存专家', 'description': '存活5分钟', 'unlocked': False},
            'shapeshifter': {'name': '变形大师', 'description': '尝试所有皮肤', 'unlocked': False},
            'powerup_master': {'name': '道具大师', 'description': '使用所有类型的道具', 'unlocked': False}
        }
        self.used_skins = set()
        self.used_powerups = set()
        self.start_time = time.time()
        self.notifications = []
    
    def check_achievement(self, achievement_id: str, condition: bool = True):
        """检查成就"""
        if condition and not self.achievements[achievement_id]['unlocked']:
            self.achievements[achievement_id]['unlocked'] = True
            self.notifications.append({
                'text': f"🏆 成就解锁: {self.achievements[achievement_id]['name']}",
                'time': time.time(),
                'duration': 3.0
            })
    
    def update_notifications(self, current_time: float):
        """更新通知"""
        self.notifications = [n for n in self.notifications 
                            if current_time - n['time'] < n['duration']]
    
    def render_notifications(self, screen: pygame.Surface, font: pygame.font.Font):
        """渲染通知"""
        for i, notification in enumerate(self.notifications):
            alpha = max(0, min(255, int((notification['duration'] - 
                                       (time.time() - notification['time'])) * 255)))
            
            text_surface = font.render(notification['text'], True, (255, 215, 0))
            text_rect = text_surface.get_rect()
            text_rect.centerx = screen.get_width() // 2
            text_rect.y = 100 + i * 40
            
            # 半透明背景
            bg_surface = pygame.Surface((text_rect.width + 20, text_rect.height + 10))
            bg_surface.set_alpha(alpha // 2)
            bg_surface.fill((0, 0, 0))
            screen.blit(bg_surface, (text_rect.x - 10, text_rect.y - 5))
            
            # 文本
            text_surface.set_alpha(alpha)
            screen.blit(text_surface, text_rect)
