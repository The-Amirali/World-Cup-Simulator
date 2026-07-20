#ClassTeam.py
#Amirali Ganjvar 404131133

import random
import numpy as np


class Team:
    '''
    کلاس نشان‌دهنده یک تیم فوتبال به همراه مشخصات فنی (حمله، دفاع، رنکینگ) و آمارهای تورنمنت
    '''

    def __init__(self, name: str, attack: int, defense: int, rank: int):
        '''
        سازنده کلاس Team

        Args:
            name (str): نام تیم ملی
            attack (int): قدرت حمله (۱ تا ۱۰۰)
            defense (int): قدرت دفاع (۱ تا ۱۰۰)
            rank (int): رتبه فیفا 
        '''
        self.name = name
        self.attack = attack
        self.defense = defense
        self.rank = rank
        self.goals_for = 0
        self.goals_against = 0
        self.points = 0
        self.group = ''

    def goal_difference(self):
        '''
        محاسبه تفاضل گل تیم.

        Returns:
            int: تفاضل گل زده منهای گل خورده (goals_for - goals_against)
        '''
        return self.goals_for - self.goals_against
    
    def reset_stats(self):
        '''
        ریست کردن امار تیم ها قبل از هر شبیه سازی

        Returns:
            None
        '''
        self.goals_for = 0
        self.goals_against = 0
        self.points = 0

    def simulate_match(self, opponent, is_knockout=False):
        '''
        شبیه‌سازی مسابقه فوتبال بین تیم خودی و حریف بر اساس مدل پواسون و شبیه‌سازی وقت اضافه و پنالتی‌ها در مراحل حذفی

        Args:
            opponent (Team): شیء مربوط به تیم حریف
            is_knockout (bool): آیا مسابقه در مرحله حذفی برگزار می‌شود و نیاز به تعیین برنده قطعی دارد یا خیر

        Returns:
            tuple: شامل (گل‌های تیم خودی، گل‌های حریف، شیء تیم برنده، گل‌های پنالتی خودی، گل‌های پنالتی حریف)
        '''
        lambda_self = (self.attack / 100) * 1.5 + (1 - (opponent.defense / 100)) * 0.8
        lambda_opponent = (opponent.attack / 100) * 1.5 + (1 - (self.defense / 100)) * 0.8

        goals_self = np.random.poisson(lambda_self)
        goals_opponent = np.random.poisson(lambda_opponent)

        winner = None
        self_goals = None
        opponent_goals = None

        # فقط در مرحله حذفی و در صورت تساوی در ۹۰ دقیقه، وقت اضافه شبیه‌سازی می‌شود
        if is_knockout and goals_self == goals_opponent:
            # شبیه‌سازی ۳۰ دقیقه وقت اضافه با lambda برابر ۰.۳۳ برابر lambda اصلی
            et_goals_self = np.random.poisson(lambda_self * 0.33)
            et_goals_opponent = np.random.poisson(lambda_opponent * 0.33)

            # گل‌های وقت اضافه به نتیجه نهایی مسابقه اضافه می‌شوند
            goals_self += et_goals_self
            goals_opponent += et_goals_opponent

            if et_goals_self > et_goals_opponent:
                winner = self
            elif et_goals_self < et_goals_opponent:
                winner = opponent
            else:
                # اگر باز هم مساوی شد سراغ پنالتی ها میرویم
                self_goals = 0
                opponent_goals = 0

                # احتمال گل شدن هر پنالتی بر اساس حمله خودی و دفاع حریف
                p_self = 0.75 + (self.attack - opponent.defense) / 250
                p_opponent = 0.75 + (opponent.attack - self.defense) / 250

                # محدود کردن احتمال به بازه [0.6, 0.9]
                chance_self = max(0.6, min(0.9, p_self))
                chance_opponent = max(0.6, min(0.9, p_opponent))

                # ۵ پنالتی عادی برای هر تیم
                for i in range(5):
                    if random.random() < chance_self:
                        self_goals += 1
                    if random.random() < chance_opponent:
                        opponent_goals += 1
                
                if self_goals > opponent_goals:
                    winner = self
                elif self_goals < opponent_goals:
                    winner = opponent
                else:
                    # اگر بعد از 5 پنالتی همچنان مساوی بود سراغ پنالتی های ناگهانی میرویم
                    # تا زمانی که مجموع گل‌های دو تیم با هم برابر است هر دور یک
                    # پنالتی دیگر برای هر تیم زده می‌شود
                    while self_goals == opponent_goals:
                        if random.random() < chance_self:
                            self_goals += 1
                        if random.random() < chance_opponent:
                            opponent_goals += 1

                    if self_goals > opponent_goals:
                        winner = self
                    elif self_goals < opponent_goals:
                        winner = opponent

        # نتیجه در ۹۰ دقیقه مشخص شده (یا مرحله گروهی است) -> بر اساس تعداد گل تصمیم می‌گیریم
        elif goals_self > goals_opponent:
            winner = self
        elif goals_self < goals_opponent:
            winner = opponent
        else:
            # تساوی در مرحله گروهی -> بدون وقت اضافه و پنالتی برنده‌ای وجود ندارد
            winner = None

        return goals_self, goals_opponent, winner, self_goals, opponent_goals
