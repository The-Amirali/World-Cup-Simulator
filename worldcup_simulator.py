#worldcup_simulator.py
# ================================
# دانشجو: Amirali Ganjvar
# شماره دانشجویی : 404131133
# عنوان پروژه: شبیه ساز جام جهانی 2026
# تاریخ تحویل : 1405/04/29
# ================================

import csv
import os
import random
import numpy as np

from ClassTeam import Team
from ClassMatch import Match
from ClassGroup import Group
from ClassKnockoutStage import KnockoutStage


class WorldCupSimulator:
    """
    کلاس اصلی مدیریت شبیه‌ساز جام جهانی ۲۰۲۶ شامل سیدبندی، قرعه‌کشی، بازی‌ها و آمارگیری نهایی
    """

    def __init__(self):
        '''
        سازنده کلاس WorldCupSimulator
        '''
        self.teams = []
        self.groups = []
        self.round_of_16 = None
        self.quarterfinals = None
        self.semifinals = None
        self.final = None
        self.champion = None
        self.knockout_teams = []
    
    def load_teams_from_csv(self, filename):
        """
        خواندن مشخصات فنی، نام و رنکینگ فیفای ۳۲ تیم ملی از روی فایل ورودی

        Args:
            filename (str): مسیر کامل یا نسبی فایل CSV
        """
        with open(filename, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for parts in reader:
                if len(parts) == 4:
                    name, attack, defense, rank = parts
                    if rank.isdigit():
                        team = Team(name, int(attack), int(defense), int(rank))
                        self.teams.append(team)

    def seed_and_draw_groups(self):
        """
        دسته‌بندی ۳۲ تیم بارگذاری‌ شده به ۴ سید رنکینگی و قرعه‌کشی  انها درون ۸ گروه (A تا H)
        """
        self.teams.sort(key=lambda team: team.rank)

        seed1 = self.teams[:8]
        seed2 = self.teams[8:16]
        seed3 = self.teams[16:24]
        seed4 = self.teams[24:32]

        random.shuffle(seed1)
        random.shuffle(seed2)
        random.shuffle(seed3)
        random.shuffle(seed4)

        for i in range(8):
            group_teams = [seed1[i], seed2[i], seed3[i], seed4[i]]
            group_name = chr(65 + i)
            group = Group(group_name, group_teams)
            self.groups.append(group)
    
    def run_group_stage(self, verbose=True):
        """
        اجرای مسابقات تمام گروه‌ها، رتبه‌بندی تیم‌ها و راهیابی تیم‌های برتر به مرحله حذفی

        Args:
            verbose (bool): وضعیت چاپ یا عدم چاپ جدول رده‌بندی گروه‌ها در خروجی 
        """
        for team in self.teams:
            team.reset_stats()

        self.round_of_16 = None
        self.quarterfinals = None
        self.semifinals = None
        self.final = None
        self.champion = None
        self.knockout_teams = []
        
        for group in self.groups:
            group.play_all_matches()
            ranked_teams = group.get_rankings()
            
            first_place = ranked_teams[0]
            second_place = ranked_teams[1]
            
            self.knockout_teams.append(first_place)
            self.knockout_teams.append(second_place)
            
            if verbose:
                print(f"\nGroup {group.name}")
                for index, team in enumerate(ranked_teams):
                    gd = team.goal_difference()
                    gd_str = f"+{gd}" if gd > 0 else f"{gd}"
                    print(f"{index + 1}. {team.name}: {team.points} pts, GD {gd_str}, GF {team.goals_for}")

    def setup_knockout_bracket(self):
        '''
        ساخت براکت حذفی با استفاده از حلقه ، طبق ترتیب فرمول فیفا.
        '''
        r16_matches = []
        
        # حلقه اول: جفت کردن اول‌های گروه با دوم‌های گروه بعدی (A1 vs B2, C1 vs D2, ...)
        for i in range(0, 16, 4):
            r16_matches.append(Match(self.knockout_teams[i], self.knockout_teams[i + 3], is_knockout=True))

        # حلقه دوم: جفت کردن دوم‌های گروه با اول‌های گروه بعدی (B1 vs A2, D1 vs C2, ...)
        for i in range(0, 16, 4):
            r16_matches.append(Match(self.knockout_teams[i + 2], self.knockout_teams[i + 1], is_knockout=True))
            
        # انتقال مسابقات به کلاس KnockoutStage برای مرحله یک‌هشتم نهایی
        self.round_of_16 = KnockoutStage("Round of 16", r16_matches)

    def run_knockout_stage(self, verbose=True):
        '''
        اجرای تمام مراحل حذفی و تعیین قهرمان نهایی تورنمنت.

        Args:
            verbose (bool): وضعیت نمایش متنی نتایج مراحل حذفی در کنسول
        '''
        if verbose:
            print("\n===================================")
            print("    STARTING THE KNOCKOUT STAGE     ")
            print("===================================")

        # اجرای مرحله یک‌هشتم نهایی
        self.round_of_16.play_round()
        if verbose:
            self.round_of_16.display_results()
        winners = self.round_of_16.get_winners()
        
        #  اجرای مراحل یک‌چهارم و نیمه‌نهایی
        for stage_name in ["Quarterfinals", "Semifinals"]:
            next_matches = []
            
            # برنده‌های مرحله قبل را ۲ تا ۲ تا روبروی هم می‌گذاریم
            for i in range(0, len(winners), 2):
                match = Match(winners[i], winners[i + 1], is_knockout=True)
                next_matches.append(match)
                
            # ساخت و اجرای مرحله حذفی جدید
            stage = KnockoutStage(stage_name, next_matches)
            stage.play_round()
            if verbose:
                stage.display_results()
            
            winners = stage.get_winners()

            if stage_name == "Quarterfinals":
                self.quarterfinals = stage
            else:
                self.semifinals = stage

        # برگزاری فینال و تعیین قهرمان
        final_match = Match(winners[0], winners[1], is_knockout=True)
        self.final = KnockoutStage("Final", [final_match])
        self.final.play_round()
        
        self.champion = final_match.winner
        
        # چاپ خروجی فینال 
        if verbose:
            print("\n===Final===")
            if final_match.pens1 is not None and final_match.pens2 is not None:
                print(f"{final_match.team1.name} {final_match.goals1} ({final_match.pens1}) - ({final_match.pens2}) {final_match.goals2} {final_match.team2.name} | Winner: {final_match.winner.name}")
            else:
                print(f"{final_match.team1.name} {final_match.goals1} - {final_match.goals2} {final_match.team2.name} | Winner: {final_match.winner.name}")

    def run_full_simulation(self, verbose=False):
        """
        اجرای کامل یک دوره جام جهانی از ابتدا تا انتها با ریست کردن کامل وضعیت آماری تیم‌ها

        Args:
            verbose (bool): فعال یا غیرفعال کردن چاپ جزئیات مسابقات در طول شبیه‌سازی

        Returns:
                Team: شیء مربوط به تیم قهرمان تورنمنت
        """
        for team in self.teams:
            team.reset_stats()
            
        # خالی کردن لیست‌ها و متغیرها برای شبیه‌سازی جدید
        self.knockout_teams = []
        self.round_of_16 = None
        self.quarterfinals = None
        self.semifinals = None
        self.final = None
        self.champion = None
        
        # قرعه‌کشی و اجرای مرحله گروهی
        if not self.groups:
            self.seed_and_draw_groups()
        self.run_group_stage(verbose=verbose)
        
        # چیدن براکت حذفی و اجرای مسابقات حذفی
        self.setup_knockout_bracket()
        self.run_knockout_stage(verbose=verbose)
        
        # برگرداندن شیء تیم قهرمان
        return self.champion

    def most_likely_champion(self, num_simulations=1000):
        """
        شبیه‌سازی کل تورنمنت به تعداد دفعات مشخص و گزارش آماری درصد قهرمانی هر تیم 

        Args:
            num_simulations (int): تعداد کل شبیه‌سازی‌های جام جهانی (پیش‌فرض ۱۰۰۰ بار)
        """
        if num_simulations <= 0:
            print(" Error: Number of simulations must be a positive integer.")
            return

        print(f" Simulating {num_simulations} world cups, please wait...\n")

        champions_chances = {}

        for i in range(num_simulations):
            self.groups = []  # ریست کردن گروه‌ها برای هر شبیه‌سازی
            self.seed_and_draw_groups()
            champion = self.run_full_simulation(verbose=False)
            if champion.name in champions_chances:
                champions_chances[champion.name] += 1
            else:
                champions_chances[champion.name] = 1

        sorted_champions = sorted(champions_chances.items(), key=lambda x: x[1], reverse=False)

        for team, wins in sorted_champions:
            probability = (wins / num_simulations) * 100
            print(f"{team}: {probability:.1f}% chance of winning")

        try:
            import matplotlib.pyplot as plt
        
            teams = [x[0] for x in sorted_champions]
            chances = [(x[1] / num_simulations) * 100 for x in sorted_champions]

            # رسم نمودار میله‌ای افقی (معکوس کردن لیست‌ها برای قرارگیری بیشترین شانس در بالای نمودار)
            plt.barh(teams[::-1], chances[::-1], color='red')
            # تنظیم عنوان اصلی نمودار همراه با نمایش تعداد شبیه‌سازی‌ها
            plt.title(f'World Cup 2026 Championship Probabilities\n({num_simulations} Simulations)')
            # درجه‌بندی محور افقی از ۰ تا ۲۰ درصد با گام‌های ۵ تایی
            plt.xticks(np.arange(0, 21, 5))
            # تنظیم برچسب محور افقی (درصد شانس قهرمانی)
            plt.xlabel('Chance of Winning (%)')
            # تنظیم برچسب محور عمودی (تیم‌ها)
            plt.ylabel('Teams')
            # کوچک کردن اندازه فونت اسامی تیم‌ها در محور عمودی جهت خوانایی بهتر
            plt.yticks(fontsize=8)
            # تنظیم خودکار حاشیه‌های نمودار برای جلوگیری از بیرون‌زدگی متون
            plt.tight_layout()
            print("Displaying bar chart of championship probabilities...")
            plt.show()

        except ImportError:
            print("matplotlib is not installed. Please install it to see the bar chart.")

    def display_bracket(self):
        '''
        نمایش براکت حذفی به صورت متنی.
        '''
        if not self.round_of_16 or not self.quarterfinals or not self.semifinals or not self.final:
            print(" Error: Knockout stages have not been played yet.")
            return

        def display_match(match):
            if match.pens1 is not None and match.pens2 is not None:
                return f"{match.team1.name} {match.goals1} ({match.pens1}) - ({match.pens2}) {match.goals2} {match.team2.name} | Winner: {match.winner.name}"
            else:
                return f"{match.team1.name} {match.goals1} - {match.goals2} {match.team2.name} | Winner: {match.winner.name}"

        print("\n==== Knockout Stage Bracket ====")

        # نمایش مرحله یک‌هشتم نهایی
        print("\n===Round of 16===")
        for match in self.round_of_16.matches:
            print(display_match(match))

        # نمایش مرحله یک‌چهارم نهایی
        print("\n===Quarterfinals===")
        for match in self.quarterfinals.matches:
            print(display_match(match))

        # نمایش مرحله نیمه‌نهایی
        print("\n===Semifinals===   ")
        for match in self.semifinals.matches:
            print(display_match(match))

        # نمایش فینال
        final_match = self.final.matches[0]
        print("\n===Final===")
        print(display_match(final_match))

    def run_menu(self):
        """
        راه‌اندازی منوی تعامل با کاربر برای اجرای شبیه‌ساز جام جهانی ۲۰۲۶ و انتخاب گزینه‌های مختلف
        """
        while True:
            print("\n=== World Cup 2026 Simulator ===")
            print("1. Load team data from CSV")
            print("2. Draw groups (Automatic seeding)")
            print("3. Run group stage and display group tables")
            print("4. Run full tournament simulation and display champion")
            print("5. Run multiple simulations and report champion probabilities")
            print("6. Display knockout stage bracket at the last simulation")
            print("7. Exit")
            choice = input("Enter your choice (1-7): ")

            if choice == '1':
                filename = input("\nEnter the path to the CSV file(default: worldcup_2026_teams.txt): ")
                current_dir = os.path.dirname(os.path.abspath(__file__))
                if not filename:
                    filename = os.path.join(current_dir, "worldcup_2026_teams.txt")
                else:
                    filename = os.path.abspath(filename)
                
                if os.path.exists(filename):
                    self.teams = []  # خالی کردن لیست تیم‌ها قبل از لود کردن مجدد
                    self.load_teams_from_csv(filename)
                    print(f" Loaded {len(self.teams)} teams from {filename}")
                else:
                    print(f" Error: File {filename} does not exist.")

            elif choice == '2':
                if len(self.teams) != 32:
                    print(" \nError: You must load exactly 32 teams before drawing groups.")
                else:
                    self.groups = []  # ریست کردن لیست گروه‌ها برای جلوگیری از انباشته شدن گروه‌ها
                    self.seed_and_draw_groups()
                    print(" \nGroups have been drawn.")
            
            elif choice == '3':
                if len(self.teams) != 32:
                    print(" \nError: You must load exactly 32 teams before drawing groups.")
                elif not self.groups:
                    print(" \nError: You must draw groups before running the group stage.")
                else:
                    self.run_group_stage(verbose=True)
                    print(" \nGroup stage completed and tables displayed.")

            elif choice == '4':
                if len(self.teams) != 32:
                    print(" \nError: You must load exactly 32 teams before running the tournament.")
                else:
                    champion = self.run_full_simulation(verbose=True)
                    print(f"\n The champion of the World Cup 2026 is: {champion.name}")

            elif choice == '5':
                if len(self.teams) != 32:
                    print(" \nError: You must load exactly 32 teams before running simulations.")
                else:
                    try:
                        simulation_number = input("\nEnter the number of simulations to run(default is 1000): ").strip()
                        if not simulation_number:
                            self.most_likely_champion()
                        else:
                            self.most_likely_champion(num_simulations=int(simulation_number))
                    except ValueError:
                        print(" Error: Please enter a valid integer for the number of simulations.")

            elif choice == '6':
                if len(self.teams) != 32:
                    print(" \nError: You must load exactly 32 teams before displaying the bracket.")
                elif not self.round_of_16:
                    print(" \nError: You must run a full tournament simulation before displaying the bracket.")
                else:
                    self.display_bracket()

            elif choice == '7':
                print("Exiting the simulator. Goodbye!")
                break


simulator = WorldCupSimulator()
simulator.run_menu()
