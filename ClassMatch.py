#ClassMatch.py
#Amirali Ganjvar 404131133


from ClassTeam import Team


class Match:
    '''
    کلاس ثبت اطلاعات یک مسابقه مشخص و اعمال نتایج آن روی مشخصات آماری دو تیم بازی‌کننده
    '''

    def __init__(self, team1: Team, team2: Team, is_knockout: bool = False):
        '''
        سازنده کلاس Match.

        Args:
            team1 (Team): تیم اول
            team2 (Team): تیم دوم
            is_knockout (bool): آیا این مسابقه در مرحله حذفی است یا خیر
        '''
        self.team1 = team1
        self.team2 = team2
        self.goals1 = 0
        self.goals2 = 0
        self.is_knockout = is_knockout
        self.winner = None

        self.pens1 = None
        self.pens2 = None

    def play(self):
        '''
        اجرای مسابقه ، شبیه‌سازی نتیجه، به‌روزرسانی آمار هر دو تیم (گل زده/خورده و
        در مرحله گروهی امتیاز) و تعیین برنده مسابقه.

        Returns:
            None
        '''
        # شبیه‌سازی نتیجه مسابقه با استفاده از منطق پیاده‌سازی‌شده در Team
        goals1, goals2, winner, pens1, pens2 = self.team1.simulate_match(self.team2, self.is_knockout)

        self.goals1 = goals1
        self.goals2 = goals2
        self.winner = winner
        self.pens1 = pens1
        self.pens2 = pens2

        # بروزرسانی امار تیم ها
        self.team1.goals_for += self.goals1
        self.team1.goals_against += self.goals2

        self.team2.goals_for += self.goals2
        self.team2.goals_against += self.goals1

        # امتیازدهی تیم ها در مرحله گروهی
        if not self.is_knockout:
            if self.winner == self.team1:
                self.team1.points += 3
            elif self.winner == self.team2:
                self.team2.points += 3
            else:
                self.team1.points += 1
                self.team2.points += 1