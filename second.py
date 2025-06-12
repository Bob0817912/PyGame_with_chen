# -*- coding: utf-8 -*-
import pygame
import random
import numpy as np 
import emoji

# 游戏常量
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# 颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)
PINK = (255, 192, 203)
BROWN = (139, 69, 19)
GOLD = (255, 215, 0)
SILVER = (192, 192, 192)
DARK_RED = (139, 0, 0)
DARK_GREEN = (0, 100, 0)
DARK_BLUE = (0, 0, 139)
LIGHT_GRAY = (211, 211, 211)
DARK_GRAY = (64, 64, 64)

# 金币和装备系统
import json
import os
from datetime import datetime, date

# 游戏数据文件
SAVE_FILE = "game_data.json"

# 装备配置
EQUIPMENT_CONFIGS = {
    "power_gloves": {
        "name": "力量手套",
        "description": "增加攻击力",
        "price": 100,
        "effects": {"attack_bonus": 1.2},
        "icon": "拳套"
    },
    "speed_boots": {
        "name": "疾风靴",
        "description": "增加移动速度",
        "price": 150,
        "effects": {"speed_bonus": 1.3},
        "icon": "靴子"
    },
    "armor_vest": {
        "name": "护甲背心",
        "description": "增加防御力",
        "price": 200,
        "effects": {"defense_bonus": 1.4},
        "icon": "护甲"
    },
    "energy_ring": {
        "name": "能量戒指",
        "description": "增加能量恢复",
        "price": 120,
        "effects": {"energy_bonus": 1.5},
        "icon": "戒指"
    },
    "health_amulet": {
        "name": "生命护符",
        "description": "增加最大生命值",
        "price": 180,
        "effects": {"health_bonus": 1.25},
        "icon": "护符"
    },
    "critical_sword": {
        "name": "暴击之剑",
        "description": "增加暴击率",
        "price": 250,
        "effects": {"critical_bonus": 0.15},
        "icon": "宝剑"
    }
}

# Boss配置
BOSS_CONFIGS = {
    "fire_demon": {
        "name": "烈焰恶魔",
        "color": (200, 50, 50),
        "max_health": 300,
        "speed": 4,
        "energy_regen": 0.8,
        "attack_damage": {"punch": 15, "kick": 20, "special": 35, "ultimate": 60},
        "attack_range": {"punch": 60, "kick": 80, "special": 120, "ultimate": 150},
        "attack_cooldown": {"punch": 15, "kick": 25, "special": 50, "ultimate": 120},
        "damage_reduction": 0.4,
        "reward": 50,
        "description": "强大的烈焰恶魔，拥有火焰攻击",
        "special_abilities": ["fire_breath", "flame_shield"]
    },
    "ice_giant": {
        "name": "冰霜巨人",
        "color": (100, 150, 255),
        "max_health": 400,
        "speed": 3,
        "energy_regen": 0.6,
        "attack_damage": {"punch": 18, "kick": 25, "special": 40, "ultimate": 70},
        "attack_range": {"punch": 70, "kick": 90, "special": 130, "ultimate": 160},
        "attack_cooldown": {"punch": 20, "kick": 30, "special": 60, "ultimate": 150},
        "damage_reduction": 0.5,
        "reward": 75,
        "description": "巨大的冰霜巨人，攻击带有冰冻效果",
        "special_abilities": ["ice_storm", "freeze_attack"]
    },
    "shadow_lord": {
        "name": "暗影领主",
        "color": (80, 80, 120),
        "max_health": 350,
        "speed": 6,
        "energy_regen": 1.0,
        "attack_damage": {"punch": 20, "kick": 28, "special": 45, "ultimate": 80},
        "attack_range": {"punch": 65, "kick": 85, "special": 140, "ultimate": 180},
        "attack_cooldown": {"punch": 12, "kick": 20, "special": 45, "ultimate": 100},
        "damage_reduction": 0.3,
        "reward": 100,
        "description": "神秘的暗影领主，拥有瞬移和分身能力",
        "special_abilities": ["shadow_clone", "teleport_strike"]
    }
}

# 角色配置
CHARACTER_CONFIGS = {
    "warrior": {
        "name": "战士",
        "color": (255, 140, 0),  # 橙色
        "max_health": 120,
        "speed": 5,
        "energy_regen": 0.4,
        "attack_damage": {"punch": 10, "kick": 15, "special": 25, "ultimate": 40},
        "attack_range": {"punch": 50, "kick": 65, "special": 85, "ultimate": 110},
        "attack_cooldown": {"punch": 18, "kick": 30, "special": 70, "ultimate": 180},
        "damage_reduction": 0.3,
        "description": "平衡型战士，攻防兼备",
        "skills": {
            "punch": "重拳：基础攻击，伤害适中",
            "kick": "战斧踢：中等伤害的踢击",
            "special": "旋风斩：范围攻击，消耗30能量",
            "ultimate": "狂战士之怒：超强攻击，消耗70能量"
        }
    },
    "assassin": {
        "name": "刺客",
        "color": (75, 0, 130),  # 靛青色
        "max_health": 80,
        "speed": 8,
        "energy_regen": 0.6,
        "attack_damage": {"punch": 12, "kick": 18, "special": 30, "ultimate": 55},
        "attack_range": {"punch": 45, "kick": 60, "special": 75, "ultimate": 90},
        "attack_cooldown": {"punch": 12, "kick": 20, "special": 50, "ultimate": 120},
        "damage_reduction": 0.1,
        "description": "高速高攻击，血量较低",
        "skills": {
            "punch": "毒刃：快速攻击，冷却短",
            "kick": "影踢：高伤害踢击",
            "special": "暗影突袭：瞬移攻击，消耗30能量",
            "ultimate": "千刃风暴：连续攻击，消耗70能量"
        }
    },
    "tank": {
        "name": "坦克",
        "color": (105, 105, 105),  # 暗灰色
        "max_health": 180,
        "speed": 3,
        "energy_regen": 0.3,
        "attack_damage": {"punch": 8, "kick": 12, "special": 20, "ultimate": 35},
        "attack_range": {"punch": 55, "kick": 70, "special": 90, "ultimate": 120},
        "attack_cooldown": {"punch": 25, "kick": 40, "special": 90, "ultimate": 220},
        "damage_reduction": 0.6,
        "description": "超高血量和防御，移动缓慢",
        "skills": {
            "punch": "铁拳：重型攻击，伤害稳定",
            "kick": "震地踢：范围震击",
            "special": "钢铁壁垒：短暂无敌，消耗30能量",
            "ultimate": "地震冲击：大范围攻击，消耗70能量"
        }
    },
    "mage": {
        "name": "法师",
        "color": (138, 43, 226),  # 蓝紫色
        "max_health": 90,
        "speed": 4,
        "energy_regen": 0.8,
        "attack_damage": {"punch": 6, "kick": 10, "special": 35, "ultimate": 60},
        "attack_range": {"punch": 40, "kick": 55, "special": 130, "ultimate": 160},
        "attack_cooldown": {"punch": 20, "kick": 35, "special": 60, "ultimate": 150},
        "damage_reduction": 0.2,
        "description": "远程攻击专家，能量恢复快",
        "skills": {
            "punch": "魔法弹：远程魔法攻击",
            "kick": "法力冲击：中距离攻击",
            "special": "火球术：远程爆炸攻击，消耗30能量",
            "ultimate": "陨石术：超远程毁灭攻击，消耗70能量"
        }
    },
    "ninja": {
        "name": "忍者",
        "color": (25, 25, 112),  # 午夜蓝
        "max_health": 95,
        "speed": 7,
        "energy_regen": 0.5,
        "attack_damage": {"punch": 11, "kick": 16, "special": 28, "ultimate": 45},
        "attack_range": {"punch": 48, "kick": 63, "special": 80, "ultimate": 100},
        "attack_cooldown": {"punch": 15, "kick": 25, "special": 55, "ultimate": 140},
        "damage_reduction": 0.25,
        "description": "连击专家，擅长组合攻击",
        "skills": {
            "punch": "手里剑：快速投掷攻击",
            "kick": "飞踢：空中连击",
            "special": "分身术：创造分身攻击，消耗30能量",
            "ultimate": "忍法·千鸟：连续攻击，消耗70能量"
        }
    },
    "boxer": {
        "name": "拳击手",
        "color": (220, 20, 60),  # 深红色
        "max_health": 110,
        "speed": 6,
        "energy_regen": 0.45,
        "attack_damage": {"punch": 15, "kick": 8, "special": 32, "ultimate": 50},
        "attack_range": {"punch": 52, "kick": 45, "special": 70, "ultimate": 85},
        "attack_cooldown": {"punch": 10, "kick": 35, "special": 65, "ultimate": 160},
        "damage_reduction": 0.35,
        "description": "拳击专精，拳击攻击强化",
        "skills": {
            "punch": "直拳：超快拳击，冷却极短",
            "kick": "低扫：下盘攻击",
            "special": "组合拳：连续拳击，消耗30能量",
            "ultimate": "终极重拳：毁灭性拳击，消耗70能量"
        }
    }
}

# --- 音效配置 ---
# Sounds will be generated internally
LOADED_SOUNDS = {}

# Pygame 初始化
pygame.init()
pygame.mixer.init() # 初始化音频混合器

# 全屏相关变量
is_fullscreen = False
original_size = (SCREEN_WIDTH, SCREEN_HEIGHT)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("火柴人对打小游戏")
clock = pygame.time.Clock()

def get_screen_size():
    """获取当前屏幕尺寸"""
    global SCREEN_WIDTH, SCREEN_HEIGHT
    if is_fullscreen:
        # 全屏模式下获取实际屏幕尺寸
        info = pygame.display.Info()
        SCREEN_WIDTH = info.current_w
        SCREEN_HEIGHT = info.current_h
    else:
        # 窗口模式使用原始尺寸
        SCREEN_WIDTH, SCREEN_HEIGHT = original_size

# 游戏数据管理
class GameData:
    def __init__(self):
        self.coins = 0
        self.equipment = {}  # 拥有的装备
        self.equipped_items = {}  # 装备的物品
        self.last_signin_date = None
        self.total_wins = 0
        self.boss_defeats = 0
        self.load_data()

    def load_data(self):
        """加载游戏数据"""
        try:
            if os.path.exists(SAVE_FILE):
                with open(SAVE_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.coins = data.get('coins', 0)
                    self.equipment = data.get('equipment', {})
                    self.equipped_items = data.get('equipped_items', {})
                    self.last_signin_date = data.get('last_signin_date', None)
                    self.total_wins = data.get('total_wins', 0)
                    self.boss_defeats = data.get('boss_defeats', 0)
        except Exception as e:
            print(f"加载游戏数据失败: {e}")
            self.reset_data()

    def save_data(self):
        """保存游戏数据"""
        try:
            data = {
                'coins': self.coins,
                'equipment': self.equipment,
                'equipped_items': self.equipped_items,
                'last_signin_date': self.last_signin_date,
                'total_wins': self.total_wins,
                'boss_defeats': self.boss_defeats
            }
            with open(SAVE_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存游戏数据失败: {e}")

    def reset_data(self):
        """重置游戏数据"""
        self.coins = 100  # 初始金币
        self.equipment = {}
        self.equipped_items = {}
        self.last_signin_date = None
        self.total_wins = 0
        self.boss_defeats = 0

    def add_coins(self, amount):
        """添加金币"""
        self.coins += amount
        self.save_data()

    def spend_coins(self, amount):
        """花费金币"""
        if self.coins >= amount:
            self.coins -= amount
            self.save_data()
            return True
        return False

    def buy_equipment(self, equipment_id):
        """购买装备"""
        if equipment_id in EQUIPMENT_CONFIGS:
            config = EQUIPMENT_CONFIGS[equipment_id]
            if self.spend_coins(config["price"]):
                self.equipment[equipment_id] = True
                return True
        return False

    def equip_item(self, equipment_id):
        """装备物品"""
        if equipment_id in self.equipment:
            self.equipped_items[equipment_id] = True
            self.save_data()
            return True
        return False

    def unequip_item(self, equipment_id):
        """卸下装备"""
        if equipment_id in self.equipped_items:
            del self.equipped_items[equipment_id]
            self.save_data()
            return True
        return False

    def daily_signin(self):
        """每日签到"""
        today = date.today().isoformat()
        if self.last_signin_date != today:
            self.last_signin_date = today
            signin_reward = 20
            self.add_coins(signin_reward)
            return signin_reward
        return 0

# 全局游戏数据实例
game_data = GameData()

def toggle_fullscreen():
    """切换全屏/窗口模式"""
    global screen, is_fullscreen, SCREEN_WIDTH, SCREEN_HEIGHT

    if is_fullscreen:
        # 切换到窗口模式
        screen = pygame.display.set_mode(original_size)
        is_fullscreen = False
        SCREEN_WIDTH, SCREEN_HEIGHT = original_size
        print("切换到窗口模式")
    else:
        # 切换到全屏模式
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        is_fullscreen = True
        # 获取全屏尺寸
        info = pygame.display.Info()
        SCREEN_WIDTH = info.current_w
        SCREEN_HEIGHT = info.current_h
        print(f"切换到全屏模式 ({SCREEN_WIDTH}x{SCREEN_HEIGHT})")

    pygame.display.set_caption("火柴人对打小游戏")

# 生成音效
def generate_sound(frequency, duration_ms, shape='square', volume=0.3):
    """生成一个简单的音效并返回 pygame.mixer.Sound 对象"""
    sample_rate, format_bits, channels = pygame.mixer.get_init()
    if sample_rate == 0: # Mixer not initialized or failed
        print("警告: Pygame Mixer 未正确初始化，无法生成声音。")
        return None

    num_samples = int(sample_rate * duration_ms / 1000.0)
    arr = np.zeros(num_samples, dtype=np.int16)
    
    # Max amplitude for int16 is 32767. Apply volume.
    amplitude = int(32767 * volume) 

    if shape == 'square':
        period_samples = sample_rate / frequency
        for i in range(num_samples):
            if (i // (period_samples / 2)) % 2 == 0:
                arr[i] = amplitude
            else:
                arr[i] = -amplitude
    elif shape == 'sine': # Example for a sine wave
        for i in range(num_samples):
            arr[i] = int(amplitude * np.sin(2 * np.pi * frequency * i / sample_rate))
    # Can add other shapes like 'sawtooth', 'triangle' if needed

    if channels == 2: # Stereo
        stereo_arr = np.zeros((num_samples, 2), dtype=np.int16)
        stereo_arr[:,0] = arr
        stereo_arr[:,1] = arr
        sound_buffer = stereo_arr
    else: # Mono
        sound_buffer = arr
    
    try:
        sound = pygame.mixer.Sound(buffer=sound_buffer)
        return sound
    except pygame.error as e:
        print(f"警告: 创建Sound对象失败: {e}")
        return None

# 尝试在mixer初始化后立即生成声音
if pygame.mixer.get_init(): # Check if mixer was successfully initialized
    LOADED_SOUNDS["punch"] = generate_sound(660, 80, shape='square', volume=0.25)
    LOADED_SOUNDS["kick"]  = generate_sound(550, 100, shape='square', volume=0.3)
    LOADED_SOUNDS["hit"]   = generate_sound(330, 120, shape='square', volume=0.35)
    LOADED_SOUNDS["jump"]  = generate_sound(880, 70, shape='square', volume=0.2)
    LOADED_SOUNDS["special"] = generate_sound(440, 150, shape='sine', volume=0.4)
    LOADED_SOUNDS["block"] = generate_sound(200, 60, shape='square', volume=0.2)
    LOADED_SOUNDS["ultimate"] = generate_sound(800, 200, shape='sine', volume=0.5)
    
    # 打印加载成功的音效（如果生成成功）
    for name, sound_obj in LOADED_SOUNDS.items():
        if sound_obj:
            print(f"成功生成内置音效: {name}")
        else:
            print(f"警告: 未能生成内置音效: {name}")
else:
    print("警告: Pygame Mixer 初始化失败，将无声音运行。")


def play_sound(name):
    """播放音效 (如果已加载/生成)"""
    if name in LOADED_SOUNDS and LOADED_SOUNDS[name]:
        LOADED_SOUNDS[name].play()

# 字体
try:
    font_path_simhei = pygame.font.match_font("simhei") # 尝试查找SimHei
    if font_path_simhei:
        font = pygame.font.Font(font_path_simhei, 30)
        print(f"成功加载 SimHei 字体: {font_path_simhei}")
    else:
        raise pygame.error("SimHei not found by match_font")
except pygame.error:
    try:
        # 尝试其他常见中文字体 for Windows
        font_path_msyh = pygame.font.match_font("microsoftyahei")
        if font_path_msyh:
            font = pygame.font.Font(font_path_msyh, 30)
            print(f"成功加载 Microsoft YaHei 字体: {font_path_msyh}")
        else:
            raise pygame.error("Microsoft YaHei not found")
    except pygame.error:
        font = pygame.font.Font(None, 30) # 备用字体
        print("警告: 未找到 SimHei 或 Microsoft YaHei 字体，使用默认字体。中文字符可能无法正确显示。")


class Stickman(pygame.sprite.Sprite):
    def __init__(self, x, y, color=None, player_controls=None, facing_left=False, character_type="warrior"):
        super().__init__()
        self.base_image = pygame.Surface([60, 110]) # 增大画布
        self.base_image.set_colorkey(BLACK)
        self.image = self.base_image.copy()
        self.character_type = character_type  # 角色类型

        # 从配置中获取角色属性
        self.config = CHARACTER_CONFIGS.get(character_type, CHARACTER_CONFIGS["warrior"])
        self.color = color if color else self.config["color"]
        self.character_name = self.config["name"]

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = y

        # 基础属性 - 从配置中读取
        self.max_health = self.config["max_health"]
        self.health = self.max_health
        self.vel_x = 0
        self.vel_y = 0
        self.gravity = 0.8
        self.jump_strength = -18
        self.on_ground = False
        self.speed = self.config["speed"]

        # 攻击系统 - 从配置中读取
        self.is_attacking = False
        self.attack_type = None
        self.attack_frame = 0
        self.attack_duration = {"punch": 15, "kick": 20, "special": 25, "ultimate": 40}
        self.attack_damage = self.config["attack_damage"].copy()
        self.attack_range = self.config["attack_range"].copy()
        self.attack_hitbox = None

        # 冷却系统 - 从配置中读取
        self.attack_cooldown_time = self.config["attack_cooldown"].copy()
        self.current_cooldown = 0

        # 防御系统
        self.is_blocking = False
        self.block_duration = 0
        self.block_cooldown = 0
        self.damage_reduction = self.config["damage_reduction"]

        # 特殊能力
        self.energy = 100  # 能量系统
        self.max_energy = 100
        self.energy_regen = self.config["energy_regen"]
        self.combo_count = 0  # 连击数
        self.combo_timer = 0  # 连击计时器

        # 状态效果
        self.status_effects = {}  # 状态效果字典
        self.invulnerable_time = 0  # 无敌时间

        # 角色特殊效果
        self.special_effects = []  # 特效列表
        self.effect_timer = 0

        # 装备系统
        self.equipped_items = {}
        self.apply_equipment_effects()

        self.player_controls = player_controls
        self.facing_left = facing_left
        self.draw_stickman()

    def apply_equipment_effects(self):
        """应用装备效果"""
        # 重置为基础值
        base_config = CHARACTER_CONFIGS.get(self.character_type, CHARACTER_CONFIGS["warrior"])

        # 应用装备效果
        for equipment_id in game_data.equipped_items:
            if equipment_id in EQUIPMENT_CONFIGS:
                effects = EQUIPMENT_CONFIGS[equipment_id]["effects"]

                # 攻击力加成
                if "attack_bonus" in effects:
                    bonus = effects["attack_bonus"]
                    for attack_type in self.attack_damage:
                        self.attack_damage[attack_type] = int(base_config["attack_damage"][attack_type] * bonus)

                # 速度加成
                if "speed_bonus" in effects:
                    self.speed = int(base_config["speed"] * effects["speed_bonus"])

                # 防御加成
                if "defense_bonus" in effects:
                    self.damage_reduction = min(0.8, base_config["damage_reduction"] * effects["defense_bonus"])

                # 能量加成
                if "energy_bonus" in effects:
                    self.energy_regen = base_config["energy_regen"] * effects["energy_bonus"]

                # 生命值加成
                if "health_bonus" in effects:
                    old_ratio = self.health / self.max_health if self.max_health > 0 else 1
                    self.max_health = int(base_config["max_health"] * effects["health_bonus"])
                    self.health = int(self.max_health * old_ratio)

    def get_character_info(self):
        """获取角色信息"""
        return {
            "name": self.character_name,
            "type": self.character_type,
            "description": self.config["description"],
            "skills": self.config["skills"]
        }

    def draw_stickman(self):
        self.image.fill(BLACK)

        # 根据角色类型调整外观
        center_x = self.image.get_width() // 2

        # 角色特定的外观参数
        if self.character_type == "tank":
            head_radius = 14
            body_width = 5
            body_height = 40
        elif self.character_type == "assassin":
            head_radius = 9
            body_width = 2
            body_height = 38
        elif self.character_type == "mage":
            head_radius = 11
            body_width = 3
            body_height = 36
        elif self.character_type == "ninja":
            head_radius = 10
            body_width = 3
            body_height = 37
        elif self.character_type == "boxer":
            head_radius = 12
            body_width = 4
            body_height = 39
        else:  # warrior
            head_radius = 11
            body_width = 3
            body_height = 38

        body_start_y = head_radius * 2
        body_end_y = body_start_y + body_height
        arm_joint_y = body_start_y + 10
        leg_joint_y = body_end_y

        # 头部 - 根据角色类型有不同特征
        head_color = self.color
        pygame.draw.circle(self.image, head_color, (center_x, head_radius), head_radius)

        # 角色特定的头部装饰
        if self.character_type == "tank":
            # 头盔效果
            pygame.draw.circle(self.image, SILVER, (center_x, head_radius), head_radius + 2, 2)
        elif self.character_type == "mage":
            # 法师帽
            hat_points = [(center_x - 8, head_radius - 5), (center_x + 8, head_radius - 5), (center_x, head_radius - 15)]
            pygame.draw.polygon(self.image, PURPLE, hat_points)
        elif self.character_type == "ninja":
            # 面罩
            pygame.draw.rect(self.image, BLACK, (center_x - 6, head_radius - 3, 12, 6))
        elif self.character_type == "boxer":
            # 拳击头带
            pygame.draw.rect(self.image, RED, (center_x - 10, head_radius - 8, 20, 4))

        # 眼睛
        eye_size = 2
        if self.character_type != "ninja":  # 忍者被面罩遮住
            pygame.draw.circle(self.image, WHITE, (center_x - 4, head_radius - 2), eye_size)
            pygame.draw.circle(self.image, WHITE, (center_x + 4, head_radius - 2), eye_size)
        else:
            # 忍者发光的眼睛
            pygame.draw.circle(self.image, RED, (center_x - 4, head_radius - 2), eye_size)
            pygame.draw.circle(self.image, RED, (center_x + 4, head_radius - 2), eye_size)

        # 身体
        pygame.draw.line(self.image, self.color, (center_x, body_start_y), (center_x, body_end_y), body_width)

        # 角色特定的身体装饰
        if self.character_type == "tank":
            # 护甲
            pygame.draw.rect(self.image, SILVER, (center_x - 8, body_start_y + 5, 16, 20))
        elif self.character_type == "mage":
            # 法袍
            pygame.draw.rect(self.image, PURPLE, (center_x - 6, body_start_y + 10, 12, 25))
        elif self.character_type == "boxer":
            # 拳击背心
            pygame.draw.rect(self.image, RED, (center_x - 5, body_start_y + 8, 10, 18))

        # 根据状态显示特效
        if self.is_blocking:
            # 格挡时显示盾牌效果
            shield_color = (0, 150, 255)
            pygame.draw.circle(self.image, shield_color, (center_x, body_start_y + 20), 28, 3)

        if self.invulnerable_time > 0:
            # 无敌时闪烁效果
            if self.invulnerable_time % 10 < 5:
                glow_color = GOLD
                pygame.draw.circle(self.image, glow_color, (center_x, body_start_y + 20), 35, 2)

        direction_mod = -1 if self.facing_left else 1

        # 手臂动画 - 根据角色类型调整
        arm_width = 4 if self.character_type == "boxer" else 3

        if self.is_attacking and self.attack_type == "punch":
            if self.character_type == "boxer":
                # 拳击手特殊拳击动画
                pygame.draw.line(self.image, self.color, (center_x, arm_joint_y), (center_x + 30 * direction_mod, arm_joint_y), arm_width)
                pygame.draw.circle(self.image, RED, (center_x + 30 * direction_mod, arm_joint_y), 5)  # 拳套
            else:
                pygame.draw.line(self.image, self.color, (center_x, arm_joint_y), (center_x + 25 * direction_mod, arm_joint_y + 5), arm_width)
            pygame.draw.line(self.image, self.color, (center_x, arm_joint_y), (center_x - 10 * direction_mod, arm_joint_y - 5), arm_width)
        elif self.is_attacking and self.attack_type == "kick":
            pygame.draw.line(self.image, self.color, (center_x, arm_joint_y), (center_x + 10 * direction_mod, arm_joint_y - 10), arm_width)
            pygame.draw.line(self.image, self.color, (center_x, arm_joint_y), (center_x - 10 * direction_mod, arm_joint_y - 10), arm_width)
        elif self.is_attacking and self.attack_type == "special":
            # 特殊攻击 - 根据角色类型不同效果
            if self.character_type == "mage":
                # 法师魔法效果
                pygame.draw.line(self.image, PURPLE, (center_x, arm_joint_y), (center_x + 35 * direction_mod, arm_joint_y - 10), 5)
                pygame.draw.circle(self.image, PURPLE, (center_x + 35 * direction_mod, arm_joint_y - 10), 8)
            elif self.character_type == "ninja":
                # 忍者分身效果
                pygame.draw.line(self.image, CYAN, (center_x, arm_joint_y), (center_x + 25 * direction_mod, arm_joint_y), 4)
                pygame.draw.line(self.image, CYAN, (center_x, arm_joint_y), (center_x + 20 * direction_mod, arm_joint_y - 15), 4)
            else:
                pygame.draw.line(self.image, self.color, (center_x, arm_joint_y), (center_x + 20 * direction_mod, arm_joint_y - 5), 4)
                pygame.draw.line(self.image, self.color, (center_x, arm_joint_y), (center_x + 15 * direction_mod, arm_joint_y + 10), 4)
        elif self.is_attacking and self.attack_type == "ultimate":
            # 终极技能 - 全身发光，根据角色类型不同颜色
            ultimate_color = GOLD
            if self.character_type == "mage":
                ultimate_color = PURPLE
            elif self.character_type == "assassin":
                ultimate_color = DARK_RED
            elif self.character_type == "ninja":
                ultimate_color = CYAN

            pygame.draw.line(self.image, ultimate_color, (center_x, arm_joint_y), (center_x + 30 * direction_mod, arm_joint_y), 6)
            pygame.draw.line(self.image, ultimate_color, (center_x, arm_joint_y), (center_x - 15 * direction_mod, arm_joint_y - 15), 6)
            # 终极技能光环
            pygame.draw.circle(self.image, ultimate_color, (center_x, body_start_y + 20), 40, 3)
        else:
            pygame.draw.line(self.image, self.color, (center_x, arm_joint_y), (center_x + 10 * direction_mod, arm_joint_y + 15), arm_width)
            pygame.draw.line(self.image, self.color, (center_x, arm_joint_y), (center_x - 10 * direction_mod, arm_joint_y + 15), arm_width)

        # 腿部动画
        leg_width = 4 if self.character_type == "tank" else 3

        if self.is_attacking and self.attack_type == "kick":
            pygame.draw.line(self.image, self.color, (center_x, leg_joint_y), (center_x + 30 * direction_mod, leg_joint_y + 5), leg_width)
            pygame.draw.line(self.image, self.color, (center_x, leg_joint_y), (center_x - 5 * direction_mod, leg_joint_y + 20), leg_width)
        elif not self.on_ground:
            pygame.draw.line(self.image, self.color, (center_x, leg_joint_y), (center_x + 8 * direction_mod, leg_joint_y + 15), leg_width)
            pygame.draw.line(self.image, self.color, (center_x, leg_joint_y), (center_x - 8 * direction_mod, leg_joint_y + 15), leg_width)
        else:
            pygame.draw.line(self.image, self.color, (center_x, leg_joint_y), (center_x + 8 * direction_mod, leg_joint_y + 25), leg_width)
            pygame.draw.line(self.image, self.color, (center_x, leg_joint_y), (center_x - 8 * direction_mod, leg_joint_y + 25), leg_width)
    def update(self):
        self.vel_x = 0
        keys = pygame.key.get_pressed()

        # 能量恢复
        if self.energy < self.max_energy:
            self.energy = min(self.max_energy, self.energy + self.energy_regen)
        
        # 状态效果更新
        if self.invulnerable_time > 0:
            self.invulnerable_time -= 1
        
        if self.combo_timer > 0:
            self.combo_timer -= 1
        else:
            self.combo_count = 0
        
        if self.block_duration > 0:
            self.block_duration -= 1
            if self.block_duration <= 0:
                self.is_blocking = False
        
        if self.block_cooldown > 0:
            self.block_cooldown -= 1

        if self.player_controls and self.health > 0:
            # 移动控制
            if keys[self.player_controls['left']]:
                self.vel_x = -self.speed
                if not self.facing_left: self.facing_left = True
            if keys[self.player_controls['right']]:
                self.vel_x = self.speed
                if self.facing_left: self.facing_left = False
            
            # 跳跃
            if keys[self.player_controls['jump']] and self.on_ground:
                self.vel_y = self.jump_strength
                self.on_ground = False
                play_sound("jump")
            
            # 格挡
            if 'block' in self.player_controls and keys[self.player_controls['block']] and self.block_cooldown == 0:
                if not self.is_blocking:
                    self.is_blocking = True
                    self.block_duration = 30  # 持续0.5秒
                    self.block_cooldown = 60  # 冷却1秒
                    play_sound("block")
            
            # 攻击控制
            if self.current_cooldown == 0 and not self.is_attacking:
                if keys[self.player_controls['punch']]:
                    self.attack("punch")
                elif keys[self.player_controls['kick']]:
                    self.attack("kick")
                elif 'special' in self.player_controls and keys[self.player_controls['special']] and self.energy >= 30:
                    self.attack("special")
                elif 'ultimate' in self.player_controls and keys[self.player_controls['ultimate']] and self.energy >= 70:
                    self.attack("ultimate")
        
        # 应用重力
        self.vel_y += self.gravity
        if self.vel_y > 15:
            self.vel_y = 15
        
        # 格挡时减速
        if self.is_blocking:
            self.vel_x *= 0.3
        
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

        # 地面碰撞
        ground_level = SCREEN_HEIGHT - 50
        if self.rect.bottom >= ground_level:
            self.rect.bottom = ground_level
            self.on_ground = True
            self.vel_y = 0

        # 边界限制
        if self.rect.left < 0: self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH: self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0: self.rect.top = 0

        # 攻击逻辑
        if self.is_attacking:
            self.attack_frame += 1
            if self.attack_frame >= self.attack_duration[self.attack_type]:
                self.is_attacking = False
                self.attack_type = None
                self.attack_frame = 0
                self.attack_hitbox = None
            else:
                # 更新攻击框位置
                hitbox_y = self.rect.centery - 15 if self.attack_type == "punch" else self.rect.centery - 10
                hitbox_height = 30 if self.attack_type in ["special", "ultimate"] else 20
                
                attack_range = self.attack_range[self.attack_type]
                if self.facing_left:
                    self.attack_hitbox = pygame.Rect(self.rect.left - attack_range + 25, hitbox_y, attack_range, hitbox_height)
                else:
                    self.attack_hitbox = pygame.Rect(self.rect.right - 25, hitbox_y, attack_range, hitbox_height)

        # 冷却计时
        if self.current_cooldown > 0:
            self.current_cooldown -= 1

        self.draw_stickman()

    def attack(self, attack_type):
        if not self.is_attacking and self.current_cooldown == 0 and self.health > 0:
            # 检查能量消耗
            energy_cost = {"punch": 0, "kick": 5, "special": 30, "ultimate": 70}
            if self.energy >= energy_cost[attack_type]:
                self.is_attacking = True
                self.attack_type = attack_type
                self.attack_frame = 0
                self.current_cooldown = self.attack_cooldown_time[attack_type]
                self.energy -= energy_cost[attack_type]
                
                # 播放对应音效
                if attack_type in ["special", "ultimate"]:
                    play_sound(attack_type)
                else:
                    play_sound(attack_type)

    def take_damage(self, amount, attacker_facing_left, attack_type="punch"):
        if self.health > 0 and self.invulnerable_time <= 0:
            # 格挡减伤
            if self.is_blocking:
                amount = int(amount * (1 - self.damage_reduction))
                play_sound("block")
                # 格挡成功后短暂无敌
                self.invulnerable_time = 10
            else:
                play_sound("hit")
                # 被击中后的无敌时间
                self.invulnerable_time = 20
            
            self.health -= amount
            
            # 连击系统
            if hasattr(self, 'last_attacker') and self.last_attacker == attacker_facing_left:
                self.combo_count += 1
                self.combo_timer = 120  # 2秒内的连击
            else:
                self.combo_count = 1
            self.last_attacker = attacker_facing_left
            
            # 击退效果 - 根据攻击类型调整
            knockback_strength = {"punch": 8, "kick": 12, "special": 20, "ultimate": 30}
            kb = knockback_strength.get(attack_type, 10)
            
            if attacker_facing_left:
                self.rect.x -= kb
            else:
                self.rect.x += kb
            
            # 垂直击退（针对强力攻击）
            if attack_type in ["special", "ultimate"]:
                self.vel_y = -5
                self.on_ground = False

            if self.health <= 0:
                self.health = 0
                print(f"角色 {self.color} 被击败!")

    def heal(self, amount):
        """治疗方法"""
        self.health = min(self.max_health, self.health + amount)

    def restore_energy(self, amount):
        """恢复能量"""
        self.energy = min(self.max_energy, self.energy + amount)

class AIStickman(Stickman):
    def __init__(self, x, y, color, target_sprite, facing_left=True, difficulty="hard", character_type="warrior"):
        super().__init__(x, y, color, facing_left=facing_left, character_type=character_type)
        self.target = target_sprite
        self.action_timer = 0
        self.movement_direction = 0
        self.difficulty = difficulty  # "easy", "normal", "hard", "nightmare"

        # AI状态
        self.ai_state = "aggressive"  # "aggressive", "defensive", "combo"
        self.state_timer = 0
        self.last_distance = 0
        self.dodge_timer = 0
        self.combo_sequence = []
        self.combo_index = 0

        # 根据难度调整AI属性
        self.setup_ai_difficulty()
        
    def setup_ai_difficulty(self):
        """根据难度设置AI属性"""
        if self.difficulty == "easy":
            self.reaction_time = 35  # 反应时间（帧）
            self.accuracy = 0.7
            self.aggressiveness = 0.6  # 提高攻击性
            self.block_chance = 0.3
            self.combo_chance = 0.2
            self.attack_frequency = 0.4  # 攻击频率
        elif self.difficulty == "normal":
            self.reaction_time = 25
            self.accuracy = 0.8
            self.aggressiveness = 0.75
            self.block_chance = 0.45
            self.combo_chance = 0.4
            self.attack_frequency = 0.6
        elif self.difficulty == "hard":
            self.reaction_time = 15
            self.accuracy = 0.9
            self.aggressiveness = 0.85
            self.block_chance = 0.65
            self.combo_chance = 0.6
            self.attack_frequency = 0.8
            # 增强属性
            self.max_health = 120
            self.health = self.max_health
            self.speed = 6
        elif self.difficulty == "nightmare":
            self.reaction_time = 8
            self.accuracy = 0.95
            self.aggressiveness = 0.95
            self.block_chance = 0.8
            self.combo_chance = 0.8
            self.attack_frequency = 0.9
            # 大幅增强
            self.max_health = 150
            self.health = self.max_health
            self.speed = 7
            self.attack_damage = {"punch": 12, "kick": 18, "special": 25, "ultimate": 40}
            self.energy_regen = 0.6

        # AI行为控制
        self.action_timer = 0 # 用于控制AI行为间隔
        self.movement_direction = 0 # -1 left, 1 right, 0 stay
        self.attack_timer = 0  # 攻击计时器
        self.pursuit_timer = 0  # 追击计时器
        self.last_attack_time = 0  # 上次攻击时间
        self.consecutive_attacks = 0  # 连续攻击次数

    def update(self):
        if self.health <= 0 or not self.target or self.target.health <= 0:
            self.vel_x = 0
            super().update()
            return

        # 更新AI计时器
        self.state_timer -= 1
        self.attack_timer -= 1
        self.pursuit_timer -= 1
        if self.dodge_timer > 0:
            self.dodge_timer -= 1

        # 获取目标信息
        distance_to_target = self.rect.centerx - self.target.rect.centerx
        abs_distance = abs(distance_to_target)
        target_attacking = self.target.is_attacking
        target_health_ratio = self.target.health / self.target.max_health
        my_health_ratio = self.health / self.max_health

        # 朝向目标
        if distance_to_target > 0:
            self.facing_left = True
        else:
            self.facing_left = False

        # 高级AI反应系统
        self.advanced_reaction_system(target_attacking, abs_distance, target_health_ratio)

        # 主动攻击系统 - 让AI更加主动
        self.proactive_attack_system(abs_distance, target_health_ratio, my_health_ratio)

        # AI决策系统 - 更频繁的决策
        self.action_timer -= 1
        if self.action_timer <= 0:
            self.action_timer = random.randint(self.reaction_time // 2, self.reaction_time + 10)

            # 状态机决策
            if self.ai_state == "aggressive":
                self.aggressive_behavior(distance_to_target, abs_distance)
            elif self.ai_state == "defensive":
                self.defensive_behavior(distance_to_target, abs_distance)
            elif self.ai_state == "combo":
                self.combo_behavior(distance_to_target, abs_distance)

            # 状态转换
            if self.state_timer <= 0:
                self.change_ai_state()

        # 应用移动（更智能的移动）
        self.smart_movement(abs_distance, target_attacking)

        super().update()

    def advanced_reaction_system(self, target_attacking, abs_distance, target_health_ratio):
        """高级反应系统"""
        # 智能格挡 - 根据距离和攻击类型调整
        if target_attacking and abs_distance < 90:
            block_probability = self.block_chance
            # 如果目标血量低，更倾向于攻击而不是格挡
            if target_health_ratio < 0.3:
                block_probability *= 0.5

            if random.random() < block_probability and self.block_cooldown == 0 and not self.is_blocking:
                self.is_blocking = True
                self.block_duration = 25
                self.block_cooldown = 40
                play_sound("block")

        # 智能闪避 - 更精确的闪避时机
        if target_attacking and abs_distance < 70 and self.dodge_timer == 0:
            dodge_chance = 0.6 if self.difficulty in ["hard", "nightmare"] else 0.4
            if random.random() < dodge_chance:
                self.dodge_timer = 25
                # 智能闪避方向选择
                if self.on_ground and random.random() < 0.7:
                    self.vel_y = self.jump_strength * 0.8
                    self.on_ground = False
                # 侧向闪避 - 修复变量名
                distance_to_target = self.rect.centerx - self.target.rect.centerx
                self.movement_direction = 1 if distance_to_target > 0 else -1

    def proactive_attack_system(self, abs_distance, target_health_ratio, my_health_ratio):
        """主动攻击系统 - 让AI更主动"""
        # 攻击时机判断
        can_attack = (not self.is_attacking and self.current_cooldown == 0 and
                     not self.is_blocking and self.attack_timer <= 0)

        if can_attack:
            attack_urgency = 0

            # 根据距离增加攻击欲望
            if abs_distance <= self.attack_range["punch"]:
                attack_urgency += 0.8
            elif abs_distance <= self.attack_range["kick"]:
                attack_urgency += 0.6
            elif abs_distance <= self.attack_range["special"]:
                attack_urgency += 0.4

            # 根据目标血量增加攻击欲望
            if target_health_ratio < 0.5:
                attack_urgency += 0.3
            if target_health_ratio < 0.3:
                attack_urgency += 0.4

            # 根据自己血量调整策略
            if my_health_ratio < 0.4:
                attack_urgency += 0.2  # 血量低时更激进

            # 连续攻击奖励
            if self.consecutive_attacks > 0:
                attack_urgency += 0.2

            # 应用攻击频率和攻击性
            final_attack_chance = attack_urgency * self.attack_frequency * self.aggressiveness

            if random.random() < final_attack_chance:
                self.execute_smart_attack(abs_distance, target_health_ratio)
                self.attack_timer = random.randint(10, 25)  # 设置攻击间隔

    def execute_smart_attack(self, abs_distance, target_health_ratio):
        """执行智能攻击"""
        # 根据距离选择最佳攻击方式
        if abs_distance <= self.attack_range["punch"]:
            # 近距离攻击选择
            if target_health_ratio < 0.2 and self.energy >= 70:
                # 目标血量极低，使用终极技能
                self.attack("ultimate")
                self.consecutive_attacks += 1
            elif self.energy >= 30 and random.random() < 0.4:
                # 使用特殊技能
                self.attack("special")
                self.consecutive_attacks += 1
            elif random.random() < 0.7:
                # 拳击攻击
                self.attack("punch")
                self.consecutive_attacks += 1
            else:
                # 踢击攻击
                self.attack("kick")
                self.consecutive_attacks += 1
        elif abs_distance <= self.attack_range["kick"]:
            # 中距离攻击
            if random.random() < 0.8:
                self.attack("kick")
                self.consecutive_attacks += 1
            elif self.energy >= 30:
                self.attack("special")
                self.consecutive_attacks += 1
        elif abs_distance <= self.attack_range["special"] and self.energy >= 30:
            # 远距离特殊攻击
            self.attack("special")
            self.consecutive_attacks += 1

    def smart_movement(self, abs_distance, target_attacking):
        """智能移动系统"""
        if self.is_attacking or self.is_blocking:
            self.vel_x = 0
            return

        # 追击模式 - 主动靠近目标
        if abs_distance > self.attack_range["kick"] * 1.2:
            # 距离太远，主动追击
            distance_to_target = self.rect.centerx - self.target.rect.centerx
            self.movement_direction = -1 if distance_to_target > 0 else 1
            self.pursuit_timer = 60  # 设置追击时间
        elif abs_distance < self.attack_range["punch"] * 0.4 and not target_attacking:
            # 距离太近且目标没有攻击，稍微后退准备攻击
            distance_to_target = self.rect.centerx - self.target.rect.centerx
            self.movement_direction = 1 if distance_to_target > 0 else -1
        elif self.pursuit_timer > 0:
            # 继续追击
            distance_to_target = self.rect.centerx - self.target.rect.centerx
            self.movement_direction = -1 if distance_to_target > 0 else 1
        else:
            # 在攻击范围内，保持位置或微调
            if random.random() < 0.3:
                self.movement_direction = random.choice([-1, 1, 0])
            else:
                self.movement_direction = 0

        # 应用移动
        self.vel_x = self.movement_direction * self.speed

    def aggressive_behavior(self, distance_to_target, abs_distance):
        """激进行为模式 - 更主动攻击"""
        if abs_distance > self.attack_range["kick"] * 1.1:
            # 距离太远，快速靠近并准备攻击
            self.movement_direction = -1 if distance_to_target > 0 else 1
            # 在靠近过程中尝试跳跃攻击
            if self.on_ground and random.random() < 0.15:
                self.vel_y = self.jump_strength * 0.9
                self.on_ground = False
        elif abs_distance < self.attack_range["punch"] * 0.4:
            # 距离很近，准备连续攻击
            if random.random() < 0.6:
                self.movement_direction = 0  # 停下来攻击
            else:
                self.movement_direction = 1 if distance_to_target > 0 else -1
        else:
            # 在理想攻击距离，保持压迫感并寻找攻击机会
            if random.random() < 0.4:
                self.movement_direction = -1 if distance_to_target > 0 else 1  # 继续靠近
            else:
                self.movement_direction = random.choice([-1, 1, 0])

    def defensive_behavior(self, distance_to_target, abs_distance):
        """防御行为模式 - 但仍然寻找反击机会"""
        # 保持中等距离，但不完全被动
        if abs_distance < self.attack_range["punch"] * 0.8:
            # 距离太近，后退但准备反击
            self.movement_direction = 1 if distance_to_target > 0 else -1
            # 在后退时寻找反击机会
            if random.random() < 0.3 and not self.target.is_attacking:
                self.movement_direction = 0  # 停下来准备反击
        elif abs_distance > self.attack_range["kick"] * 1.5:
            # 距离太远，适度靠近
            self.movement_direction = -1 if distance_to_target > 0 else 1
        else:
            # 在合适距离，寻找攻击机会
            if random.random() < 0.4:
                self.movement_direction = 0  # 保持距离观察
            else:
                self.movement_direction = random.choice([-1, 1])

    def combo_behavior(self, distance_to_target, abs_distance):
        """连招模式 - 积极执行连击"""
        # 执行预设连招序列
        if not self.combo_sequence:
            # 根据能量和距离选择连招
            if self.energy >= 70:
                self.combo_sequence = ["punch", "kick", "special", "ultimate"]
            elif self.energy >= 30:
                self.combo_sequence = ["punch", "kick", "special"]
            else:
                self.combo_sequence = ["punch", "kick", "punch", "kick"]
            self.combo_index = 0

        # 积极靠近以执行连招
        ideal_distance = self.attack_range["punch"] * 0.7
        if abs_distance > ideal_distance:
            self.movement_direction = -1 if distance_to_target > 0 else 1
        elif abs_distance < ideal_distance * 0.5:
            self.movement_direction = 1 if distance_to_target > 0 else -1
        else:
            self.movement_direction = 0  # 在最佳距离，准备连击

    def change_ai_state(self):
        """改变AI状态 - 更动态的状态切换"""
        health_ratio = self.health / self.max_health
        target_health_ratio = self.target.health / self.target.max_health

        # 重置连续攻击计数
        if random.random() < 0.3:
            self.consecutive_attacks = max(0, self.consecutive_attacks - 1)

        if health_ratio < 0.25:  # 血量很低时防御
            self.ai_state = "defensive"
            self.state_timer = 120
        elif target_health_ratio < 0.3 and self.energy > 40:  # 目标血量低时连招
            self.ai_state = "combo"
            self.state_timer = 90
        elif health_ratio > 0.7 and target_health_ratio > 0.5:  # 双方血量都高时激进
            self.ai_state = "aggressive"
            self.state_timer = random.randint(90, 180)
        elif self.consecutive_attacks >= 3:  # 连续攻击成功后继续激进
            self.ai_state = "aggressive"
            self.state_timer = 120
        else:  # 默认根据血量比例决定
            if health_ratio > target_health_ratio:
                self.ai_state = "aggressive"
            else:
                self.ai_state = "defensive"
            self.state_timer = random.randint(60, 150)

    def smart_attack_decision(self, abs_distance):
        """智能攻击决策 - 更主动和智能"""
        if random.random() > self.accuracy:
            return  # 根据精度决定是否攻击

        target_health_ratio = self.target.health / self.target.max_health
        my_health_ratio = self.health / self.max_health

        # 根据距离和状态选择攻击方式
        if abs_distance <= self.attack_range["punch"]:
            if self.ai_state == "combo" and self.combo_sequence and self.combo_index < len(self.combo_sequence):
                # 执行连招
                next_attack = self.combo_sequence[self.combo_index]
                if next_attack == "special" and self.energy >= 30:
                    self.attack("special")
                    self.combo_index += 1
                elif next_attack == "ultimate" and self.energy >= 70:
                    self.attack("ultimate")
                    self.combo_index += 1
                elif next_attack in ["punch", "kick"]:
                    self.attack(next_attack)
                    self.combo_index += 1

                if self.combo_index >= len(self.combo_sequence):
                    self.combo_sequence = []
                    self.ai_state = "aggressive"
            else:
                # 智能攻击选择
                attack_chance = self.aggressiveness

                # 根据目标血量调整攻击倾向
                if target_health_ratio < 0.3:
                    attack_chance += 0.3  # 目标血量低时更激进
                if my_health_ratio < 0.4:
                    attack_chance += 0.2  # 自己血量低时孤注一掷

                if random.random() < attack_chance:
                    # 智能技能选择
                    if target_health_ratio < 0.15 and self.energy >= 70:
                        # 目标血量极低，使用终极技能
                        self.attack("ultimate")
                    elif self.energy >= 30 and random.random() < 0.5:
                        # 50%概率使用特殊技能
                        self.attack("special")
                    elif random.random() < 0.65:
                        # 优先使用拳击
                        self.attack("punch")
                    else:
                        # 使用踢击
                        self.attack("kick")
        elif abs_distance <= self.attack_range["kick"]:
            # 中距离攻击更积极
            kick_chance = self.aggressiveness * 0.9
            if target_health_ratio < 0.4:
                kick_chance += 0.2

            if random.random() < kick_chance:
                self.attack("kick")
        elif abs_distance <= self.attack_range["special"] and self.energy >= 30:
            # 远距离特殊攻击
            if random.random() < self.aggressiveness * 0.6:
                self.attack("special")

        # 跳跃攻击（高难度AI更频繁）
        jump_attack_chance = 0.15 if self.difficulty in ["hard", "nightmare"] else 0.08
        if self.on_ground and random.random() < jump_attack_chance:
            self.vel_y = self.jump_strength
            self.on_ground = False


class BossStickman(AIStickman):
    def __init__(self, x, y, boss_type, target_sprite, facing_left=True):
        # 获取Boss配置
        self.boss_config = BOSS_CONFIGS[boss_type]
        self.boss_type = boss_type

        # 使用Boss配置初始化
        super().__init__(x, y, self.boss_config["color"], target_sprite, facing_left, "nightmare", "warrior")

        # 应用Boss属性
        self.max_health = self.boss_config["max_health"]
        self.health = self.max_health
        self.speed = self.boss_config["speed"]
        self.energy_regen = self.boss_config["energy_regen"]
        self.attack_damage = self.boss_config["attack_damage"].copy()
        self.attack_range = self.boss_config["attack_range"].copy()
        self.attack_cooldown_time = self.boss_config["attack_cooldown"].copy()
        self.damage_reduction = self.boss_config["damage_reduction"]

        # Boss特殊属性
        self.special_abilities = self.boss_config["special_abilities"]
        self.special_attack_timer = 0
        self.rage_mode = False
        self.rage_threshold = 0.3  # 血量低于30%进入狂暴模式

        # 重新绘制
        self.draw_stickman()

    def update(self):
        # 检查是否进入狂暴模式
        if self.health / self.max_health <= self.rage_threshold and not self.rage_mode:
            self.enter_rage_mode()

        # 特殊攻击计时器
        self.special_attack_timer -= 1

        # 使用特殊能力
        if self.special_attack_timer <= 0 and random.random() < 0.3:
            self.use_special_ability()
            self.special_attack_timer = random.randint(180, 300)  # 3-5秒冷却

        super().update()

    def enter_rage_mode(self):
        """进入狂暴模式"""
        self.rage_mode = True
        # 狂暴模式下属性提升
        for attack_type in self.attack_damage:
            self.attack_damage[attack_type] = int(self.attack_damage[attack_type] * 1.3)
        self.speed = int(self.speed * 1.2)
        self.energy_regen *= 1.5
        print(f"{self.boss_config['name']} 进入狂暴模式！")

    def use_special_ability(self):
        """使用特殊能力"""
        if not self.special_abilities:
            return

        ability = random.choice(self.special_abilities)

        if ability == "fire_breath":
            # 火焰吐息 - 远程攻击
            if abs(self.rect.centerx - self.target.rect.centerx) <= 150:
                self.attack("special")
                # 添加火焰特效
                self.special_effects.append({"type": "fire", "timer": 30})

        elif ability == "flame_shield":
            # 火焰护盾 - 临时无敌
            self.invulnerable_time = 60
            self.special_effects.append({"type": "shield", "timer": 60})

        elif ability == "ice_storm":
            # 冰风暴 - 范围攻击
            if abs(self.rect.centerx - self.target.rect.centerx) <= 200:
                self.attack("ultimate")
                self.special_effects.append({"type": "ice", "timer": 45})

        elif ability == "freeze_attack":
            # 冰冻攻击 - 减速目标
            if abs(self.rect.centerx - self.target.rect.centerx) <= 100:
                self.attack("kick")
                # 这里可以添加冰冻效果到目标

        elif ability == "shadow_clone":
            # 暗影分身 - 增加攻击次数
            self.consecutive_attacks += 2
            self.special_effects.append({"type": "shadow", "timer": 90})

        elif ability == "teleport_strike":
            # 瞬移攻击 - 瞬间接近目标
            if abs(self.rect.centerx - self.target.rect.centerx) > 80:
                # 瞬移到目标附近
                if self.target.rect.centerx > self.rect.centerx:
                    self.rect.centerx = self.target.rect.centerx - 60
                else:
                    self.rect.centerx = self.target.rect.centerx + 60
                self.attack("punch")


def draw_health_bars(player1, player2, game_mode="vs_ai"):
    bar_width = 200
    bar_height = 20
    energy_bar_height = 10
    
    # 玩家1状态栏 (左上角)
    health_ratio_p1 = max(0, player1.health / player1.max_health)
    energy_ratio_p1 = max(0, player1.energy / player1.max_energy)
    
    # 血条
    pygame.draw.rect(screen, RED, (30, 30, bar_width, bar_height))
    pygame.draw.rect(screen, GREEN, (30, 30, bar_width * health_ratio_p1, bar_height))
    # 能量条
    pygame.draw.rect(screen, (50, 50, 50), (30, 55, bar_width, energy_bar_height))
    pygame.draw.rect(screen, BLUE, (30, 55, bar_width * energy_ratio_p1, energy_bar_height))
    
    p1_text = font.render(f"P1: {int(player1.health)}/{player1.max_health}", True, WHITE)
    screen.blit(p1_text, (30, 5))
    
    # 显示连击数
    if hasattr(player1, 'combo_count') and player1.combo_count > 1:
        combo_text = font.render(f"连击: {player1.combo_count}", True, YELLOW)
        screen.blit(combo_text, (30, 70))

    # 玩家2/AI状态栏 (右上角)
    health_ratio_p2 = max(0, player2.health / player2.max_health)
    energy_ratio_p2 = max(0, player2.energy / player2.max_energy)
    
    # 血条
    pygame.draw.rect(screen, RED, (SCREEN_WIDTH - bar_width - 30, 30, bar_width, bar_height))
    pygame.draw.rect(screen, GREEN, (SCREEN_WIDTH - bar_width - 30, 30, bar_width * health_ratio_p2, bar_height))
    # 能量条
    pygame.draw.rect(screen, (50, 50, 50), (SCREEN_WIDTH - bar_width - 30, 55, bar_width, energy_bar_height))
    pygame.draw.rect(screen, BLUE, (SCREEN_WIDTH - bar_width - 30, 55, bar_width * energy_ratio_p2, energy_bar_height))
    
    p2_label = "AI" if game_mode == "vs_ai" else "P2"
    p2_text = font.render(f"{p2_label}: {int(player2.health)}/{player2.max_health}", True, WHITE)
    screen.blit(p2_text, (SCREEN_WIDTH - bar_width - 30, 5))
    
    # 显示AI状态（仅AI模式）
    if game_mode == "vs_ai" and hasattr(player2, 'ai_state'):
        ai_state_text = font.render(f"AI: {player2.ai_state}", True, CYAN)
        screen.blit(ai_state_text, (SCREEN_WIDTH - bar_width - 30, 70))

def draw_controls_help():
    """显示控制帮助"""
    help_texts = [
        "P1控制: WASD移动, J拳击, K踢腿",
        "高级: U格挡, I特殊技(30能量), O终极技(70能量)",
        "P2控制: 方向键移动, 1拳击, 2踢腿, 3格挡, 4特殊技, 5终极技",
        "F11 - 全屏切换 | ESC - 返回菜单"
    ]

    # 创建小字体用于帮助信息
    try:
        font_path_simhei = pygame.font.match_font("simhei")
        if font_path_simhei:
            help_font = pygame.font.Font(font_path_simhei, 16)
        else:
            raise pygame.error("SimHei not found")
    except pygame.error:
        help_font = pygame.font.Font(None, 16)

    # 自适应位置，确保帮助信息在屏幕底部
    help_start_y = max(SCREEN_HEIGHT - 90, SCREEN_HEIGHT - len(help_texts) * 20 - 10)

    for i, text in enumerate(help_texts):
        help_surface = help_font.render(text, True, WHITE)
        screen.blit(help_surface, (10, help_start_y + i * 20))

def check_attack_collisions(attacker, defender):
    if attacker.is_attacking and attacker.attack_hitbox and attacker.health > 0:
        if attacker.attack_hitbox.colliderect(defender.rect) and defender.health > 0:
            # 传递攻击类型给受伤函数
            defender.take_damage(attacker.attack_damage[attacker.attack_type], attacker.facing_left, attacker.attack_type)
            attacker.is_attacking = False  # 一次攻击只造成一次伤害
            attacker.attack_hitbox = None  # 清除，防止连续判定

def display_message(message, size=60, y_offset=0): # Added y_offset
    """在屏幕中央显示消息"""
    local_font = None
    try:
        font_path_simhei = pygame.font.match_font("simhei")
        if font_path_simhei: local_font = pygame.font.Font(font_path_simhei, size)
        else: raise pygame.error("SimHei not found")
    except pygame.error:
        local_font = pygame.font.Font(None, size)

    text_surface = local_font.render(message, True, WHITE)
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + y_offset)) # Apply y_offset
    screen.blit(text_surface, text_rect)

def draw_character_preview(character_type, x, y, scale=1.0):
    """绘制角色预览"""
    config = CHARACTER_CONFIGS[character_type]
    preview_surface = pygame.Surface([60, 110])
    preview_surface.set_colorkey(BLACK)
    preview_surface.fill(BLACK)

    # 创建临时角色用于绘制
    temp_char = Stickman(0, 110, character_type=character_type)
    temp_char.draw_stickman()

    # 缩放预览图
    if scale != 1.0:
        new_size = (int(60 * scale), int(110 * scale))
        scaled_surface = pygame.transform.scale(temp_char.image, new_size)
        screen.blit(scaled_surface, (x - new_size[0]//2, y - new_size[1]//2))
    else:
        screen.blit(temp_char.image, (x - 30, y - 55))

    return pygame.Rect(x - 40, y - 70, 80, 140)

def draw_character_selection_screen(selected_p1=None, selected_p2=None, mouse_pos=None, game_mode="vs_ai"):
    """绘制角色选择界面"""
    screen.fill((15, 20, 35))  # 深蓝色背景

    # 绘制大的背景框包围整个角色选择区域
    frame_width = min(SCREEN_WIDTH - 40, 800)
    frame_height = min(SCREEN_HEIGHT - 40, 650)
    frame_x = (SCREEN_WIDTH - frame_width) // 2
    frame_y = (SCREEN_HEIGHT - frame_height) // 2

    pygame.draw.rect(screen, (25, 30, 45), (frame_x, frame_y, frame_width, frame_height))
    pygame.draw.rect(screen, GOLD, (frame_x, frame_y, frame_width, frame_height), 4)

    # 标题 - 在最上方居中，使用更小的字体
    title_y = frame_y + 35
    try:
        font_path_simhei = pygame.font.match_font("simhei")
        if font_path_simhei:
            title_font = pygame.font.Font(font_path_simhei, 36)
        else:
            raise pygame.error("SimHei not found")
    except pygame.error:
        title_font = pygame.font.Font(None, 36)

    title_text = title_font.render("选择角色", True, WHITE)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, title_y))
    screen.blit(title_text, title_rect)

    # 角色列表 - 自适应屏幕尺寸
    characters = list(CHARACTER_CONFIGS.keys())
    cols = 3
    rows = 2

    # 计算角色选择区域的位置，使其在框内居中
    total_width = cols * 200 - 50  # 总宽度
    total_height = rows * 180 - 50  # 总高度
    start_x = (SCREEN_WIDTH - total_width) // 2
    start_y = max(title_y + 80, frame_y + 100)
    spacing_x = 200
    spacing_y = 180

    character_rects = {}
    hovered_character = None

    # 绘制角色选择区域
    for i, char_type in enumerate(characters):
        row = i // cols
        col = i % cols
        x = start_x + col * spacing_x
        y = start_y + row * spacing_y

        # 检查鼠标悬停
        char_rect = draw_character_preview(char_type, x, y, scale=0.8)
        character_rects[char_type] = char_rect

        if mouse_pos and char_rect.collidepoint(mouse_pos):
            hovered_character = char_type
            # 悬停高亮
            pygame.draw.rect(screen, GOLD, char_rect, 3)

        # 选中状态
        if char_type == selected_p1:
            pygame.draw.rect(screen, GREEN, char_rect, 4)
            # 绘制P1标签
            p1_text = font.render("P1", True, GREEN)
            screen.blit(p1_text, (x - 15, y + 80))
        elif char_type == selected_p2 and game_mode == "vs_player":
            pygame.draw.rect(screen, BLUE, char_rect, 4)
            # 绘制P2标签
            p2_text = font.render("P2", True, BLUE)
            screen.blit(p2_text, (x - 15, y + 80))
        else:
            # 默认边框
            pygame.draw.rect(screen, WHITE, char_rect, 2)

        # 角色名称 - 使用更小的字体
        config = CHARACTER_CONFIGS[char_type]
        try:
            font_path_simhei = pygame.font.match_font("simhei")
            if font_path_simhei:
                name_font = pygame.font.Font(font_path_simhei, 22)
            else:
                raise pygame.error("SimHei not found")
        except pygame.error:
            name_font = pygame.font.Font(None, 22)

        name_text = name_font.render(config["name"], True, WHITE)
        name_rect = name_text.get_rect(center=(x, y + 100))
        screen.blit(name_text, name_rect)

    # 显示角色信息（鼠标悬停时）
    if hovered_character:
        draw_character_info_panel(hovered_character)

    # 操作提示 - 在框的底部，使用更小的字体
    tips_y = frame_y + frame_height - 80

    # 创建小字体
    try:
        font_path_simhei = pygame.font.match_font("simhei")
        if font_path_simhei:
            tip_font = pygame.font.Font(font_path_simhei, 20)
            tip_font_small = pygame.font.Font(font_path_simhei, 16)
        else:
            raise pygame.error("SimHei not found")
    except pygame.error:
        tip_font = pygame.font.Font(None, 20)
        tip_font_small = pygame.font.Font(None, 16)

    if game_mode == "vs_player":
        tip1_text = tip_font.render("P1: 点击选择角色 | P2: 右键选择角色", True, WHITE)
        tip1_rect = tip1_text.get_rect(center=(SCREEN_WIDTH // 2, tips_y))
        screen.blit(tip1_text, tip1_rect)

        tip2_text = tip_font_small.render("ENTER - 开始游戏 | ESC - 返回菜单 | F11 - 全屏", True, LIGHT_GRAY)
        tip2_rect = tip2_text.get_rect(center=(SCREEN_WIDTH // 2, tips_y + 30))
        screen.blit(tip2_text, tip2_rect)
    else:
        tip1_text = tip_font.render("点击选择角色", True, WHITE)
        tip1_rect = tip1_text.get_rect(center=(SCREEN_WIDTH // 2, tips_y))
        screen.blit(tip1_text, tip1_rect)

        tip2_text = tip_font_small.render("ENTER - 开始游戏 | ESC - 返回菜单 | F11 - 全屏", True, LIGHT_GRAY)
        tip2_rect = tip2_text.get_rect(center=(SCREEN_WIDTH // 2, tips_y + 30))
        screen.blit(tip2_text, tip2_rect)

    return character_rects

def draw_character_info_panel(character_type):
    """绘制角色信息面板"""
    config = CHARACTER_CONFIGS[character_type]

    # 自适应屏幕尺寸的信息面板背景
    panel_width = min(760, SCREEN_WIDTH - 40)
    panel_height = 180
    panel_x = (SCREEN_WIDTH - panel_width) // 2
    panel_y = max(400, SCREEN_HEIGHT - panel_height - 20)

    panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
    pygame.draw.rect(screen, (30, 30, 50), panel_rect)
    pygame.draw.rect(screen, WHITE, panel_rect, 2)

    # 创建不同大小的字体
    try:
        font_path_simhei = pygame.font.match_font("simhei")
        if font_path_simhei:
            info_font = pygame.font.Font(font_path_simhei, 20)
            stat_font = pygame.font.Font(font_path_simhei, 16)
            skill_font = pygame.font.Font(font_path_simhei, 14)
        else:
            raise pygame.error("SimHei not found")
    except pygame.error:
        info_font = pygame.font.Font(None, 20)
        stat_font = pygame.font.Font(None, 16)
        skill_font = pygame.font.Font(None, 14)

    # 角色名称和描述
    name_text = info_font.render(f"{config['name']} - {config['description']}", True, WHITE)
    screen.blit(name_text, (panel_x + 10, panel_y + 10))

    # 属性信息
    stats_y = panel_y + 40
    stats = [
        f"生命值: {config['max_health']}",
        f"速度: {config['speed']}",
        f"能量恢复: {config['energy_regen']:.1f}",
        f"减伤: {int(config['damage_reduction']*100)}%"
    ]

    for i, stat in enumerate(stats):
        stat_text = stat_font.render(stat, True, LIGHT_GRAY)
        screen.blit(stat_text, (panel_x + 10 + (i % 2) * 200, stats_y + (i // 2) * 22))

    # 技能信息
    skills_title = stat_font.render("技能说明:", True, YELLOW)
    screen.blit(skills_title, (panel_x + 10, panel_y + 90))

    skills_y = panel_y + 115
    for i, (_, skill_desc) in enumerate(config['skills'].items()):
        if i < 4:  # 只显示4个技能
            skill_text = skill_font.render(f"{skill_desc}", True, CYAN)
            screen.blit(skill_text, (panel_x + 10, skills_y + i * 18))

def game_loop():
    running = True
    game_state = "menu"  # "menu", "mode_select", "character_select", "shop", "boss_select", "playing", "game_over"
    game_mode = "vs_ai"  # "vs_ai", "vs_player", "training", "boss"
    ai_difficulty = "hard"  # "easy", "normal", "hard", "nightmare"
    selected_boss = "fire_demon"  # 选中的Boss

    # 控制方案
    player1_controls = {
        'left': pygame.K_a, 'right': pygame.K_d,
        'jump': pygame.K_w,
        'punch': pygame.K_j, 'kick': pygame.K_k,
        'block': pygame.K_u, 'special': pygame.K_i, 'ultimate': pygame.K_o
    }

    player2_controls = {
        'left': pygame.K_LEFT, 'right': pygame.K_RIGHT,
        'jump': pygame.K_UP,
        'punch': pygame.K_KP1, 'kick': pygame.K_KP2,
        'block': pygame.K_KP3, 'special': pygame.K_KP4, 'ultimate': pygame.K_KP5
    }

    # 角色选择
    player1_character = "warrior"
    player2_character = "warrior"
    character_rects = {}

    # 商店和Boss相关
    equipment_rects = {}
    signin_rect = None
    boss_rects = {}
    selected_boss = "fire_demon"

    player1 = None
    player2 = None
    all_sprites = pygame.sprite.Group()
    winner = None

    while running:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                # 全屏切换 - F11键
                if event.key == pygame.K_F11:
                    toggle_fullscreen()

                # ESC键处理
                elif event.key == pygame.K_ESCAPE:
                    if game_state == "playing":
                        game_state = "menu"
                    elif game_state in ["character_select", "mode_select", "shop", "boss_select"]:
                        game_state = "menu"
                    else:
                        running = False

                # 主菜单
                if game_state == "menu":
                    if event.key == pygame.K_1:
                        game_mode = "vs_ai"
                        game_state = "mode_select"
                    elif event.key == pygame.K_2:
                        game_mode = "vs_player"
                        game_state = "character_select"
                    elif event.key == pygame.K_3:
                        game_mode = "training"
                        game_state = "character_select"
                    elif event.key == pygame.K_4:
                        game_mode = "boss"
                        game_state = "boss_select"
                    elif event.key == pygame.K_5:
                        game_state = "shop"

                # 角色选择界面
                elif game_state == "character_select":
                    if event.key == pygame.K_RETURN:
                        # 开始游戏
                        game_state = "playing"
                        if game_mode == "vs_ai":
                            player1, player2 = create_players(player1_controls, None,
                                                            player1_character, "warrior", game_mode, ai_difficulty)
                        elif game_mode == "vs_player":
                            player1, player2 = create_players(player1_controls, player2_controls,
                                                            player1_character, player2_character, game_mode)
                        elif game_mode == "training":
                            player1, player2 = create_players(player1_controls, None,
                                                            player1_character, "warrior", game_mode, "easy")
                        elif game_mode == "boss":
                            player1, player2 = create_boss_battle(player1_controls, player1_character, selected_boss)
                        reset_game(all_sprites, player1, player2)

                # 模式选择（AI难度）
                elif game_state == "mode_select":
                    if event.key == pygame.K_1:
                        ai_difficulty = "easy"
                        game_state = "character_select"
                    elif event.key == pygame.K_2:
                        ai_difficulty = "normal"
                        game_state = "character_select"
                    elif event.key == pygame.K_3:
                        ai_difficulty = "hard"
                        game_state = "character_select"
                    elif event.key == pygame.K_4:
                        ai_difficulty = "nightmare"
                        game_state = "character_select"
                    elif event.key == pygame.K_BACKSPACE:
                        game_state = "menu"

                # 游戏结束
                elif game_state == "game_over":
                    if event.key == pygame.K_r:
                        game_state = "character_select"
                        winner = None
                    elif event.key == pygame.K_m:
                        game_state = "menu"

            # 鼠标点击事件
            if event.type == pygame.MOUSEBUTTONDOWN:
                # 角色选择
                if game_state == "character_select":
                    for char_type, rect in character_rects.items():
                        if rect.collidepoint(mouse_pos):
                            if event.button == 1:  # 左键 - P1选择
                                player1_character = char_type
                            elif event.button == 3 and game_mode == "vs_player":  # 右键 - P2选择
                                player2_character = char_type

                # 装备商店
                elif game_state == "shop":
                    # 签到按钮
                    if signin_rect and signin_rect.collidepoint(mouse_pos):
                        reward = game_data.daily_signin()
                        if reward > 0:
                            print(f"签到成功！获得 {reward} 金币")

                    # 装备购买/装备
                    for equipment_id, rect in equipment_rects.items():
                        if rect.collidepoint(mouse_pos):
                            if equipment_id in game_data.equipped_items:
                                # 卸下装备
                                game_data.unequip_item(equipment_id)
                                print(f"卸下装备: {EQUIPMENT_CONFIGS[equipment_id]['name']}")
                            elif equipment_id in game_data.equipment:
                                # 装备物品
                                game_data.equip_item(equipment_id)
                                print(f"装备: {EQUIPMENT_CONFIGS[equipment_id]['name']}")
                            else:
                                # 购买装备
                                if game_data.buy_equipment(equipment_id):
                                    print(f"购买成功: {EQUIPMENT_CONFIGS[equipment_id]['name']}")
                                else:
                                    print("金币不足！")

                # Boss选择
                elif game_state == "boss_select":
                    for boss_id, rect in boss_rects.items():
                        if rect.collidepoint(mouse_pos):
                            selected_boss = boss_id
                            game_state = "character_select"

        # 游戏逻辑更新
        if game_state == "playing" and player1 and player2:
            all_sprites.update()
            check_attack_collisions(player1, player2)
            check_attack_collisions(player2, player1)

            # 检查胜负
            if player1.health <= 0 and winner is None:
                if game_mode == "boss":
                    winner = f"{BOSS_CONFIGS[selected_boss]['name']}"
                else:
                    winner = "AI" if game_mode == "vs_ai" else "玩家2"
                game_state = "game_over"
            elif player2.health <= 0 and winner is None:
                winner = "玩家1"
                # 给予金币奖励
                if game_mode == "boss":
                    reward = BOSS_CONFIGS[selected_boss]["reward"]
                    game_data.add_coins(reward)
                    game_data.boss_defeats += 1
                    print(f"击败Boss！获得 {reward} 金币")
                elif game_mode in ["vs_ai", "vs_player"]:
                    reward = 10
                    game_data.add_coins(reward)
                    game_data.total_wins += 1
                    print(f"胜利！获得 {reward} 金币")
                game_state = "game_over"

        # 绘制
        screen.fill((20, 25, 40))  # 深色背景

        if game_state == "menu":
            draw_main_menu()
        elif game_state == "mode_select":
            draw_mode_select_menu(ai_difficulty)
        elif game_state == "character_select":
            character_rects = draw_character_selection_screen(player1_character, player2_character, mouse_pos, game_mode)
        elif game_state == "shop":
            equipment_rects, signin_rect = draw_shop_screen(mouse_pos)
        elif game_state == "boss_select":
            boss_rects = draw_boss_selection_screen(mouse_pos)
        elif game_state == "playing":
            # 绘制地面
            pygame.draw.line(screen, (80, 80, 80), (0, SCREEN_HEIGHT - 50), (SCREEN_WIDTH, SCREEN_HEIGHT - 50), 5)

            if player1 and player2:
                all_sprites.draw(screen)
                draw_health_bars(player1, player2, game_mode)
                draw_controls_help()
                draw_skill_cooldowns(player1, player2)

                # 调试攻击框（可选）
                # if player1.attack_hitbox: pygame.draw.rect(screen, (255,0,255), player1.attack_hitbox, 2)
                # if player2.attack_hitbox: pygame.draw.rect(screen, (255,255,0), player2.attack_hitbox, 2)
        elif game_state == "game_over":
            # 绘制地面
            pygame.draw.line(screen, (80, 80, 80), (0, SCREEN_HEIGHT - 50), (SCREEN_WIDTH, SCREEN_HEIGHT - 50), 5)

            if player1 and player2:
                all_sprites.draw(screen)
                draw_health_bars(player1, player2, game_mode)
            draw_game_over_screen(winner)
        
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

def draw_skill_cooldowns(player1, player2):
    """绘制技能冷却指示器"""
    # P1技能冷却 - 自适应位置
    skills = ["punch", "kick", "special", "ultimate"]
    skill_names = ["拳", "踢", "特", "终"]

    # 确保技能冷却指示器在屏幕范围内
    skill_start_x = min(30, SCREEN_WIDTH // 20)
    skill_y = min(90, SCREEN_HEIGHT // 8)

    for i, skill in enumerate(skills):
        x = skill_start_x + i * 50
        y = skill_y

        # 技能图标背景
        pygame.draw.rect(screen, DARK_GRAY, (x, y, 40, 30))

        # 冷却进度
        if hasattr(player1, 'attack_cooldown_time') and skill in player1.attack_cooldown_time:
            max_cooldown = player1.attack_cooldown_time[skill]
            current_cooldown = player1.current_cooldown if player1.attack_type == skill else 0

            if current_cooldown > 0:
                cooldown_ratio = current_cooldown / max_cooldown
                cooldown_height = int(30 * cooldown_ratio)
                pygame.draw.rect(screen, RED, (x, y + 30 - cooldown_height, 40, cooldown_height))
            else:
                pygame.draw.rect(screen, GREEN, (x, y, 40, 30))

        # 技能名称
        skill_text = font.render(skill_names[i], True, WHITE)
        text_rect = skill_text.get_rect(center=(x + 20, y + 15))
        screen.blit(skill_text, text_rect)

    # P2技能冷却（右侧）- 自适应位置
    skill_end_x = max(SCREEN_WIDTH - 230, SCREEN_WIDTH - 250)

    for i, skill in enumerate(skills):
        x = skill_end_x + i * 50
        y = skill_y

        # 技能图标背景
        pygame.draw.rect(screen, DARK_GRAY, (x, y, 40, 30))

        # 冷却进度
        if hasattr(player2, 'attack_cooldown_time') and skill in player2.attack_cooldown_time:
            max_cooldown = player2.attack_cooldown_time[skill]
            current_cooldown = player2.current_cooldown if player2.attack_type == skill else 0

            if current_cooldown > 0:
                cooldown_ratio = current_cooldown / max_cooldown
                cooldown_height = int(30 * cooldown_ratio)
                pygame.draw.rect(screen, RED, (x, y + 30 - cooldown_height, 40, cooldown_height))
            else:
                pygame.draw.rect(screen, GREEN, (x, y, 40, 30))

        # 技能名称
        skill_text = font.render(skill_names[i], True, WHITE)
        text_rect = skill_text.get_rect(center=(x + 20, y + 15))
        screen.blit(skill_text, text_rect)

def create_players(p1_controls, p2_controls, p1_char, p2_char, mode, difficulty="normal"):
    """创建玩家角色"""
    player1 = Stickman(150, SCREEN_HEIGHT - 50, player_controls=p1_controls,
                       facing_left=False, character_type=p1_char)

    if mode == "vs_ai" or mode == "training":
        player2 = AIStickman(SCREEN_WIDTH - 150, SCREEN_HEIGHT - 50, None, player1,
                           facing_left=True, difficulty=difficulty)
        player2.character_type = p2_char
        # 重新应用角色配置
        config = CHARACTER_CONFIGS.get(p2_char, CHARACTER_CONFIGS["warrior"])
        player2.color = config["color"]
        player2.max_health = config["max_health"]
        player2.health = player2.max_health
        player2.speed = config["speed"]
        player2.attack_damage = config["attack_damage"].copy()
        player2.attack_range = config["attack_range"].copy()
        player2.attack_cooldown_time = config["attack_cooldown"].copy()
        player2.damage_reduction = config["damage_reduction"]
        player2.energy_regen = config["energy_regen"]
    else:  # vs_player
        player2 = Stickman(SCREEN_WIDTH - 150, SCREEN_HEIGHT - 50,
                          player_controls=p2_controls, facing_left=True, character_type=p2_char)

    return player1, player2

def create_boss_battle(p1_controls, p1_char, boss_type):
    """创建Boss战斗"""
    player1 = Stickman(150, SCREEN_HEIGHT - 50, player_controls=p1_controls,
                       facing_left=False, character_type=p1_char)

    # 创建Boss
    boss = BossStickman(SCREEN_WIDTH - 150, SCREEN_HEIGHT - 50, boss_type, player1, facing_left=True)

    return player1, boss

def reset_game(all_sprites, player1, player2):
    """重置游戏状态"""
    all_sprites.empty()
    all_sprites.add(player1)
    all_sprites.add(player2)

def draw_shop_screen(mouse_pos=None):
    """绘制装备商店界面"""
    screen.fill((15, 20, 35))  # 深蓝色背景

    # 绘制商店框架
    shop_width = min(SCREEN_WIDTH - 40, 900)
    shop_height = min(SCREEN_HEIGHT - 40, 700)
    shop_x = (SCREEN_WIDTH - shop_width) // 2
    shop_y = (SCREEN_HEIGHT - shop_height) // 2

    pygame.draw.rect(screen, (25, 30, 45), (shop_x, shop_y, shop_width, shop_height))
    pygame.draw.rect(screen, GOLD, (shop_x, shop_y, shop_width, shop_height), 4)

    # 标题和金币显示
    try:
        font_path_simhei = pygame.font.match_font("simhei")
        if font_path_simhei:
            title_font = pygame.font.Font(font_path_simhei, 36)
        else:
            raise pygame.error("SimHei not found")
    except pygame.error:
        title_font = pygame.font.Font(None, 36)

    title_text = title_font.render("装备商店", True, WHITE)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, shop_y + 30))
    screen.blit(title_text, title_rect)

    coin_text = title_font.render(f"金币: {game_data.coins}", True, GOLD)
    screen.blit(coin_text, (shop_x + 20, shop_y + 60))

    # 每日签到按钮
    signin_rect = pygame.Rect(shop_x + shop_width - 150, shop_y + 60, 120, 30)
    signin_reward = game_data.daily_signin()
    if signin_reward > 0:
        pygame.draw.rect(screen, GREEN, signin_rect)
        signin_text = font.render(f"签到+{signin_reward}", True, WHITE)
    else:
        pygame.draw.rect(screen, DARK_GRAY, signin_rect)
        signin_text = font.render("已签到", True, WHITE)

    signin_text_rect = signin_text.get_rect(center=signin_rect.center)
    screen.blit(signin_text, signin_text_rect)

    # 装备列表
    equipment_rects = {}
    equipment_list = list(EQUIPMENT_CONFIGS.keys())
    cols = 3
    rows = 2

    start_x = shop_x + 50
    start_y = shop_y + 120
    spacing_x = (shop_width - 100) // cols
    spacing_y = 200

    for i, equipment_id in enumerate(equipment_list):
        row = i // cols
        col = i % cols
        x = start_x + col * spacing_x
        y = start_y + row * spacing_y

        config = EQUIPMENT_CONFIGS[equipment_id]

        # 装备框
        equipment_rect = pygame.Rect(x, y, spacing_x - 20, 180)
        equipment_rects[equipment_id] = equipment_rect

        # 检查是否拥有或装备
        owned = equipment_id in game_data.equipment
        equipped = equipment_id in game_data.equipped_items

        if equipped:
            pygame.draw.rect(screen, GREEN, equipment_rect)
            pygame.draw.rect(screen, WHITE, equipment_rect, 3)
        elif owned:
            pygame.draw.rect(screen, BLUE, equipment_rect)
            pygame.draw.rect(screen, WHITE, equipment_rect, 2)
        else:
            pygame.draw.rect(screen, DARK_GRAY, equipment_rect)
            pygame.draw.rect(screen, WHITE, equipment_rect, 2)

        # 装备图标和名称
        try:
            font_path_simhei = pygame.font.match_font("simhei")
            if font_path_simhei:
                icon_font = pygame.font.Font(font_path_simhei, 32)
                name_font = pygame.font.Font(font_path_simhei, 18)
                desc_font = pygame.font.Font(font_path_simhei, 14)
            else:
                raise pygame.error("SimHei not found")
        except pygame.error:
            icon_font = pygame.font.Font(None, 32)
            name_font = pygame.font.Font(None, 18)
            desc_font = pygame.font.Font(None, 14)

        icon_text = icon_font.render(config["icon"], True, WHITE)
        icon_rect = icon_text.get_rect(center=(x + spacing_x//2 - 10, y + 30))
        screen.blit(icon_text, icon_rect)

        name_text = name_font.render(config["name"], True, WHITE)
        name_rect = name_text.get_rect(center=(x + spacing_x//2 - 10, y + 70))
        screen.blit(name_text, name_rect)

        # 描述
        desc_text = desc_font.render(config["description"], True, LIGHT_GRAY)
        desc_rect = desc_text.get_rect(center=(x + spacing_x//2 - 10, y + 90))
        screen.blit(desc_text, desc_rect)

        # 价格或状态
        if equipped:
            status_text = desc_font.render("已装备", True, GREEN)
        elif owned:
            status_text = desc_font.render("点击装备", True, CYAN)
        else:
            status_text = desc_font.render(f"价格: {config['price']}", True, YELLOW)

        status_rect = status_text.get_rect(center=(x + spacing_x//2 - 10, y + 150))
        screen.blit(status_text, status_rect)

    # 操作提示
    try:
        font_path_simhei = pygame.font.match_font("simhei")
        if font_path_simhei:
            tip_font = pygame.font.Font(font_path_simhei, 20)
        else:
            raise pygame.error("SimHei not found")
    except pygame.error:
        tip_font = pygame.font.Font(None, 20)

    tip_text = tip_font.render("ESC - 返回主菜单", True, WHITE)
    screen.blit(tip_text, (shop_x + 20, shop_y + shop_height - 30))

    return equipment_rects, signin_rect

def draw_boss_selection_screen(mouse_pos=None):
    """绘制Boss选择界面"""
    screen.fill((15, 20, 35))  # 深蓝色背景

    # 绘制Boss选择框架
    boss_width = min(SCREEN_WIDTH - 40, 800)
    boss_height = min(SCREEN_HEIGHT - 40, 600)
    boss_x = (SCREEN_WIDTH - boss_width) // 2
    boss_y = (SCREEN_HEIGHT - boss_height) // 2

    pygame.draw.rect(screen, (25, 30, 45), (boss_x, boss_y, boss_width, boss_height))
    pygame.draw.rect(screen, RED, (boss_x, boss_y, boss_width, boss_height), 4)

    # 标题
    try:
        font_path_simhei = pygame.font.match_font("simhei")
        if font_path_simhei:
            title_font = pygame.font.Font(font_path_simhei, 36)
            name_font = pygame.font.Font(font_path_simhei, 28)
            desc_font = pygame.font.Font(font_path_simhei, 18)
            tip_font = pygame.font.Font(font_path_simhei, 20)
        else:
            raise pygame.error("SimHei not found")
    except pygame.error:
        title_font = pygame.font.Font(None, 36)
        name_font = pygame.font.Font(None, 28)
        desc_font = pygame.font.Font(None, 18)
        tip_font = pygame.font.Font(None, 20)

    title_text = title_font.render("Boss挑战模式", True, WHITE)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, boss_y + 30))
    screen.blit(title_text, title_rect)

    # Boss列表
    boss_rects = {}
    boss_list = list(BOSS_CONFIGS.keys())

    start_y = boss_y + 80
    spacing_y = 120

    for i, boss_id in enumerate(boss_list):
        y = start_y + i * spacing_y
        config = BOSS_CONFIGS[boss_id]

        # Boss框
        boss_rect = pygame.Rect(boss_x + 50, y, boss_width - 100, 100)
        boss_rects[boss_id] = boss_rect

        pygame.draw.rect(screen, (40, 40, 60), boss_rect)
        pygame.draw.rect(screen, config["color"], boss_rect, 3)

        # Boss信息
        name_text = name_font.render(config["name"], True, WHITE)
        screen.blit(name_text, (boss_rect.x + 20, boss_rect.y + 10))

        desc_text = desc_font.render(config["description"], True, LIGHT_GRAY)
        screen.blit(desc_text, (boss_rect.x + 20, boss_rect.y + 40))

        reward_text = desc_font.render(f"奖励: {config['reward']} 金币", True, GOLD)
        screen.blit(reward_text, (boss_rect.x + 20, boss_rect.y + 65))

        # 血量显示
        health_text = desc_font.render(f"血量: {config['max_health']}", True, RED)
        screen.blit(health_text, (boss_rect.x + boss_rect.width - 120, boss_rect.y + 20))

    # 操作提示
    tip_text = tip_font.render("点击选择Boss | ESC - 返回主菜单", True, WHITE)
    screen.blit(tip_text, (boss_x + 20, boss_y + boss_height - 30))

    return boss_rects

def draw_main_menu():
    """绘制主菜单"""
    # 自适应屏幕尺寸的背景装饰 - 更大的框包围所有文字
    menu_width = min(700, SCREEN_WIDTH - 100)
    menu_height = 500
    menu_x = (SCREEN_WIDTH - menu_width) // 2
    menu_y = (SCREEN_HEIGHT - menu_height) // 2 - 30

    pygame.draw.rect(screen, (30, 35, 50), (menu_x, menu_y, menu_width, menu_height))
    pygame.draw.rect(screen, GOLD, (menu_x, menu_y, menu_width, menu_height), 4)

    display_message("火柴人终极对战", size=48, y_offset=-160)
    display_message("选择游戏模式:", size=32, y_offset=-100)
    display_message("1 - 对战AI", size=28, y_offset=-50)
    display_message("2 - 双人对战", size=28, y_offset=-10)
    display_message("3 - 练习模式", size=28, y_offset=30)
    display_message("4 - Boss挑战", size=28, y_offset=70)
    display_message("5 - 装备商店", size=28, y_offset=110)
    display_message("F11 - 全屏切换", size=22, y_offset=150)
    display_message("ESC - 退出游戏", size=22, y_offset=180)

def draw_mode_select_menu(current_difficulty):
    """绘制模式选择菜单"""
    # 自适应屏幕尺寸的背景装饰 - 更大的框包围所有文字
    menu_width = min(650, SCREEN_WIDTH - 150)
    menu_height = 380
    menu_x = (SCREEN_WIDTH - menu_width) // 2
    menu_y = (SCREEN_HEIGHT - menu_height) // 2 - 10

    pygame.draw.rect(screen, (30, 35, 50), (menu_x, menu_y, menu_width, menu_height))
    pygame.draw.rect(screen, CYAN, (menu_x, menu_y, menu_width, menu_height), 4)

    display_message("选择AI难度:", size=40, y_offset=-100)
    display_message("1 - 简单 (适合新手)", size=26, y_offset=-40)
    display_message("2 - 普通 (平衡挑战)", size=26, y_offset=-5)
    display_message("3 - 困难 (高手对决)", size=26, y_offset=30)
    display_message("4 - 噩梦 (极限挑战)", size=26, y_offset=65)
    display_message(f"当前: {current_difficulty.upper()}", size=22, y_offset=110)
    display_message("BACKSPACE - 返回主菜单", size=18, y_offset=140)

def draw_game_over_screen(winner):
    """绘制游戏结束界面"""
    # 半透明覆盖层
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(128)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))

    # 自适应屏幕尺寸的胜利框
    box_width = min(400, SCREEN_WIDTH - 100)
    box_height = 200
    box_x = (SCREEN_WIDTH - box_width) // 2
    box_y = (SCREEN_HEIGHT - box_height) // 2

    pygame.draw.rect(screen, (50, 50, 70), (box_x, box_y, box_width, box_height))
    pygame.draw.rect(screen, GOLD, (box_x, box_y, box_width, box_height), 4)

    if winner:
        display_message(f"🏆 {winner} 获胜! 🏆", size=60, y_offset=-30)
    display_message("R - 重新选择角色", size=35, y_offset=30)
    display_message("M - 返回主菜单", size=35, y_offset=70)


if __name__ == "__main__":
    print("--- 开始火柴人对打小游戏 ---")
    if not any(LOADED_SOUNDS.values()): 
        print("提示: 未能生成任何内置音效。游戏将无声运行。")
    elif not all(LOADED_SOUNDS.values()): 
        print("提示: 部分内置音效未能生成。游戏可能部分有声运行。")
    
    game_loop()
    print("--- 游戏结束 ---")