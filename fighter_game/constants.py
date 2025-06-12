"""
格斗游戏常量定义
"""

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

# 游戏数据文件
SAVE_FILE = "game_data.json"
