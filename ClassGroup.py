#ClassGroup.py
#Amirali Ganjvar 404131133

from ClassMatch import Match

class Group:
    '''
    کلاس مدیریت مسابقات گروهی و رتبه‌بندی تیم‌های هر گروه
    '''

    def __init__(self, name: str, teams: list):
        '''
        سازنده کلاس Group

        Args:
            name (str): نام گروه
            teams (list of Team): لیست ۴ عضوی تیم‌های گروه
        '''
        self.name = name
        self.teams = teams
        self.matches = []

    def play_all_matches(self):
        '''
        برگزاری تمام مسابقات مرحله گروهی: هر تیم دقیقاً یک بار با هر یک از
        سه تیم دیگر گروه بازی می‌کند (در مجموع ۶ مسابقه)

        Returns:
            None
        '''
        for i in range(len(self.teams)):
            for j in range(i + 1, len(self.teams)):
                match = Match(self.teams[i], self.teams[j])
                match.play()
                self.matches.append(match)
    def get_rankings(self):
        '''
        مرتب‌سازی و تعیین جایگاه تیم‌ها در جدول گروه بر اساس امتیاز، تفاضل گل، گل زده و شکستن تساوی‌ها

        Returns:
            list: لیست مرتب‌شده از ۴ تیم گروه از رتبه اول تا چهارم
        '''
        ranked_teams = self.teams.copy()
        
        ranked_teams.sort(
            key=lambda team: (
                team.points,
                team.goals_for - team.goals_against,
                team.goals_for
            ),
            reverse=True
        )
        #پیاده سازی کامل قانون بازی مستقیم بدون قرعه کشی تصادفی
        #پیدا کردن تیم هایی که امتیاز، تفاضل گل و گل زده یکسان دارند و بررسی بازی رو در رو
        for i in range(len(ranked_teams) - 1):
            team1 = ranked_teams[i]
            team2 = ranked_teams[i + 1]
            
            if (team1.points == team2.points and 
                (team1.goals_for - team1.goals_against) == (team2.goals_for - team2.goals_against) and 
                team1.goals_for == team2.goals_for):
                
                # پیدا کردن مسابقه رو در روی این دو تیم در این گروه
                for match in self.matches:
                    if (match.team1 == team1 and match.team2 == team2) or (match.team2 == team1 and match.team1 == team2):
                        # اگر تیم دوم بازی رو در رو را برده باشد، باید بیاید بالاتر (جابه‌جا شوند)
                        if match.winner == team2:
                            ranked_teams[i], ranked_teams[i + 1] = ranked_teams[i + 1], ranked_teams[i]
                        break

        return ranked_teams

    def advance_teams(self):
        '''
        تعیین دو تیم صعودکننده از گروه به مرحله حذفی.

        Returns:
            tuple: (first_team, second_team) - تیم اول و دوم گروه بر اساس رده‌بندی
        '''
        qualified_team = self.get_rankings()
        first_place = qualified_team[0]
        second_place = qualified_team[1]

        return first_place, second_place