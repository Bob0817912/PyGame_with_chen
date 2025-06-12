import pygame
import sys
import math
import random
import subprocess
import os
from typing import List, Tuple
import time

# 初始化pygame
pygame.init()

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
        
    def draw(self, screen: pygame.Surface):
        if self.life > 0:
            alpha = int((self.life / self.max_life) * 100)
            color = (*COLORS['particle'], alpha)
            size = max(1, int(self.size * (self.life / self.max_life)))
            
            # 创建临时表面用于透明度
            temp_surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            pygame.draw.circle(temp_surface, color, (size, size), size)
            screen.blit(temp_surface, (int(self.x - size), int(self.y - size)))

class GameCard:
    """游戏卡片类"""
    def __init__(self, x: int, y: int, width: int, height: int, 
                 title: str, description: str, icon_color: Tuple[int, int, int],
                 game_file: str):
        self.rect = pygame.Rect(x, y, width, height)
        self.title = title
        self.description = description
        self.icon_color = icon_color
        self.game_file = game_file
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
                glow_color = (*COLORS['accent'], max(0, glow_alpha - i * 5))
                pygame.draw.rect(glow_surface, glow_color, 
                               (0, 0, glow_rect.width, glow_rect.height), 
                               border_radius=15)
                screen.blit(glow_surface, glow_rect.topleft)
        
        # 卡片背景
        card_color = COLORS['card_hover'] if self.hover else COLORS['card_bg']
        pygame.draw.rect(screen, card_color, scaled_rect, border_radius=15)
        
        # 卡片边框
        border_color = COLORS['accent'] if self.hover else COLORS['card_border']
        pygame.draw.rect(screen, border_color, scaled_rect, width=2, border_radius=15)
        
        # 绘制图标
        self.draw_icon(screen, scaled_rect)
        
        # 标题
        title_surface = font_title.render(self.title, True, COLORS['text_primary'])
        title_rect = title_surface.get_rect()
        title_rect.centerx = scaled_rect.centerx
        title_rect.y = scaled_rect.y + scaled_rect.height * 0.6
        screen.blit(title_surface, title_rect)
        
        # 描述
        desc_surface = font_desc.render(self.description, True, COLORS['text_secondary'])
        desc_rect = desc_surface.get_rect()
        desc_rect.centerx = scaled_rect.centerx
        desc_rect.y = title_rect.bottom + 10
        screen.blit(desc_surface, desc_rect)
        
        # 悬停时显示启动提示
        if self.hover:
            hint_surface = font_desc.render("点击启动游戏", True, COLORS['accent_hover'])
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
        pygame.draw.circle(screen, COLORS['snake_green'], (int(head_x), int(head_y)), size // 6)
        
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

class GameLauncher:
    """游戏启动器主类"""
    def __init__(self):
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
                game_file="first.py"
            ),
            GameCard(
                x=start_x + card_width + spacing,
                y=card_y,
                width=card_width,
                height=card_height,
                title="火柴人快打",
                description="激烈的格斗对战游戏",
                icon_color=COLORS['fighter_red'],
                game_file="second.py"
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
            particle.draw(self.screen)

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

def main():
    """主函数"""
    try:
        launcher = GameLauncher()
        launcher.run()
    except Exception as e:
        print(f"启动器运行错误: {e}")
        pygame.quit()
        sys.exit(1)

if __name__ == "__main__":
    main()
