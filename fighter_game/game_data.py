"""
游戏数据管理系统
"""

import json
import os
from datetime import datetime, date
from .constants import SAVE_FILE, EQUIPMENT_CONFIGS

class GameData:
    """游戏数据管理类"""
    
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
