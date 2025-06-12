"""
游戏启动器核心逻辑
"""

import pygame
import sys
import random
from typing import List

from .particle_effects import Particle
from .game_card import GameCard

# 常量定义
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
FPS = 60

# 颜色定义
COLORS = {
    'bg_start': (15, 15, 35),
    'bg_end': (45, 45, 85),
    'card_bg': (25, 25, 45),
    'card_hover': (35, 35, 65),
    'card_border': (100, 100, 150),
    'text_primary': (255, 255, 255),
    'text_secondary': (180, 180, 220),
    'accent': (100, 200, 255),
    'accent_hover': (120, 220, 255),
    'snake_green': (50, 255, 50),
    'fighter_red': (128, 50, 50),
    'particle': (150, 150, 255)
}

class GameLauncher:
    """游戏启动器主类"""
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("🎮 游戏盒子 - Game Launcher")
        self.clock = pygame.time.Clock()

        # 字体设置
        try:
            # 尝试加载中文字体
            font_path = "C:\\Windows\\Fonts\\simhei.ttf"
            self.font_title = pygame.font.Font(font_path, 48)
            self.font_large = pygame.font.Font(font_path, 36)
            self.font_medium = pygame.font.Font(font_path, 24)
            self.font_small = pygame.font.Font(font_path, 18)
        except:
            print("无法加载中文字体，使用默认字体")
            self.font_title = pygame.font.Font(None, 48)
            self.font_large = pygame.font.Font(None, 36)
            self.font_medium = pygame.font.Font(None, 24)
            self.font_small = pygame.font.Font(None, 18)

        # 粒子系统
        self.particles: List[Particle] = []
        self.particle_spawn_timer = 0

        # 创建游戏卡片
        self.create_game_cards()

        # 动画时间
        self.time = 0

    def create_game_cards(self):
        """创建游戏卡片"""
        card_width = 350
        card_height = 400
        spacing = 100

        # 计算卡片位置
        total_width = 2 * card_width + spacing
        start_x = (WINDOW_WIDTH - total_width) // 2
        card_y = (WINDOW_HEIGHT - card_height) // 2

        self.game_cards = [
            GameCard(
                x=start_x,
                y=card_y,
                width=card_width,
                height=card_height,
                title="无敌蛇王",
                description="经典贪吃蛇游戏升级版",
                icon_color=COLORS['snake_green'],
                game_file="first.py",
                colors=COLORS
            ),
            GameCard(
                x=start_x + card_width + spacing,
                y=card_y,
                width=card_width,
                height=card_height,
                title="火柴人快打",
                description="激烈的格斗对战游戏",
                icon_color=COLORS['fighter_red'],
                game_file="second.py",
                colors=COLORS
            )
        ]

    def spawn_particles(self, dt: float):
        """生成粒子"""
        self.particle_spawn_timer += dt
        if self.particle_spawn_timer > 0.1:  # 每0.1秒生成粒子
            self.particle_spawn_timer = 0
            # 随机位置生成粒子
            x = random.uniform(0, WINDOW_WIDTH)
            y = random.uniform(0, WINDOW_HEIGHT)
            self.particles.append(Particle(x, y))

        # 限制粒子数量
        if len(self.particles) > 50:
            self.particles = self.particles[-50:]

    def update_particles(self, dt: float):
        """更新粒子"""
        for particle in self.particles[:]:
            particle.update(dt)
            if particle.life <= 0:
                self.particles.remove(particle)

    def draw_background(self):
        """绘制渐变背景"""
        for y in range(WINDOW_HEIGHT):
            ratio = y / WINDOW_HEIGHT
            r = int(COLORS['bg_start'][0] * (1 - ratio) + COLORS['bg_end'][0] * ratio)
            g = int(COLORS['bg_start'][1] * (1 - ratio) + COLORS['bg_end'][1] * ratio)
            b = int(COLORS['bg_start'][2] * (1 - ratio) + COLORS['bg_end'][2] * ratio)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (WINDOW_WIDTH, y))

    def draw_title(self):
        """绘制标题"""
        # 主标题
        title_text = "游戏盒子"
        title_surface = self.font_title.render(title_text, True, COLORS['text_primary'])
        title_rect = title_surface.get_rect()
        title_rect.centerx = WINDOW_WIDTH // 2
        title_rect.y = 50

        # 标题发光效果
        for i in range(3):
            glow_surface = self.font_title.render(title_text, True,
                                                (*COLORS['accent'], 100 - i * 30))
            glow_rect = title_rect.copy()
            glow_rect.x += i - 1
            glow_rect.y += i - 1
            self.screen.blit(glow_surface, glow_rect)

        self.screen.blit(title_surface, title_rect)

        # 副标题
        subtitle_text = "选择你想要游玩的游戏"
        subtitle_surface = self.font_medium.render(subtitle_text, True, COLORS['text_secondary'])
        subtitle_rect = subtitle_surface.get_rect()
        subtitle_rect.centerx = WINDOW_WIDTH // 2
        subtitle_rect.y = title_rect.bottom + 20
        self.screen.blit(subtitle_surface, subtitle_rect)

    def draw_footer(self):
        """绘制页脚信息"""
        footer_texts = [
            "按 ESC 退出",
            "点击游戏卡片启动对应游戏"
        ]

        y_offset = WINDOW_HEIGHT - 80
        for text in footer_texts:
            surface = self.font_small.render(text, True, COLORS['text_secondary'])
            rect = surface.get_rect()
            rect.centerx = WINDOW_WIDTH // 2
            rect.y = y_offset
            self.screen.blit(surface, rect)
            y_offset += 25

    def handle_events(self) -> bool:
        """处理事件"""
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 左键点击
                    for card in self.game_cards:
                        if card.is_clicked(mouse_pos):
                            print(f"启动游戏: {card.title}")
                            if card.launch_game():
                                print(f"成功启动 {card.title}")
                            else:
                                print(f"启动 {card.title} 失败")

        return True

    def update(self, dt: float):
        """更新游戏状态"""
        self.time += dt
        mouse_pos = pygame.mouse.get_pos()

        # 更新游戏卡片
        for card in self.game_cards:
            card.update(dt, mouse_pos)

        # 更新粒子系统
        self.spawn_particles(dt)
        self.update_particles(dt)

    def draw(self):
        """绘制所有内容"""
        # 背景
        self.draw_background()

        # 粒子效果
        for particle in self.particles:
            particle.draw(self.screen, COLORS['particle'])

        # 标题
        self.draw_title()

        # 游戏卡片
        for card in self.game_cards:
            card.draw(self.screen, self.font_large, self.font_medium)

        # 页脚
        self.draw_footer()

        pygame.display.flip()

    def run(self):
        """运行游戏启动器"""
        running = True

        while running:
            dt = self.clock.tick(FPS) / 1000.0  # 转换为秒

            running = self.handle_events()
            self.update(dt)
            self.draw()

        pygame.quit()
        sys.exit()
