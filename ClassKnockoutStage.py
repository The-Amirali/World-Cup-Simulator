#ClassKnockoutStage.py
#Amirali Ganjvar 404131133

class KnockoutStage:
    '''
    کلاس مدیریت مسابقات، نتایج و تیم‌های صعودکننده در یکی از مراحل حذفی تورنمنت
    '''

    def __init__(self, round_name: str, matches: list):
        '''
        سازنده کلاس KnockoutStage

        Args:
            round_name (str): نام مرحله حذفی ("Round of 16", "Quarterfinals", "Semifinals", "Final")
            matches (list of Match): لیست مسابقات این مرحله
        '''
        self.round_name = round_name
        self.matches = matches

    def play_round(self):
        """
        برگزاری تمامی مسابقات تعریف‌ شده در هر مرحله حذفی
        """
        for match in self.matches:
            match.play()

    def get_winners(self):
        """
        جمع‌آوری و بازگرداندن لیست تیم‌هایی که در بازی‌های خود برنده شده و صعود کرده‌اند

        Returns:
            list: لیستی از اشیا تیم‌های برنده این مرحله
        """
        winners = []
        for match in self.matches:
            winners.append(match.winner)
        return winners

    def display_results(self):
        """
        چاپ منظم نتایج مسابقات برگزار شده در این مرحله حذفی 
        """
        print(f"\n= Results of {self.round_name} =")
        for match in self.matches:
            if match.pens1 is not None and match.pens2 is not None:
                print(f"{match.team1.name} {match.goals1} ({match.pens1}) - ({match.pens2}) {match.goals2} {match.team2.name} | Winner: {match.winner.name}")
            else:
                print(f"{match.team1.name} {match.goals1} - {match.goals2} {match.team2.name} | Winner: {match.winner.name}")