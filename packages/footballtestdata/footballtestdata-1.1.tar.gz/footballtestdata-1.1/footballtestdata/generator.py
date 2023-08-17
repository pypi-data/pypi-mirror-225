import datetime
import random
from footballtestdata.data import ENG, ITA, SPA, GER, position

class FootballerGenerator:
    def __init__(self, first_names, last_names, cities, club, position):
        self.first_names = first_names
        self.last_names = last_names
        self.cities = cities
        self.club = club
        self.position = position
        
    @staticmethod
    def generate_random_date_of_birth(start_year, end_year):
        start_date = datetime.date(start_year, 1, 1)
        end_date = datetime.date(end_year, 12, 31)
        random_date = start_date + datetime.timedelta(days=random.randint(0, (end_date - start_date).days))
        return random_date

    def generate_fake_footballer(self, nationality):
        first_name = random.choice(self.first_names)
        last_name = random.choice(self.last_names)
        club = random.choice(self.cities) + ' ' + random.choice(self.club)
        position = random.choice(self.position)
        date_of_birth = self.generate_random_date_of_birth(1986, 2005)
        matches_played = random.randint(1, 34)
        minutes_played = random.randint(matches_played, matches_played * 90)
        # TODO Make goals and assists more realistic
        # TODO Add more statistics: xG and others
        goals = (lambda pos: 0 if pos == "GK" else random.randint(0, min(minutes_played // 50, 6)) if pos in ["LB", "CB", "RB"] else random.randint(0, min(minutes_played // 50, 9)) if pos in ["DM", "CM"] else random.randint(0, min(minutes_played // 50, 12)) if pos in ["AM", "LM", "RM"] else random.randint(0, min(minutes_played // 30, 28)))(position)
        assists = (lambda pos: random.randint(0, min(minutes_played // 50, 3)) if pos == "GK" else random.randint(0, min(minutes_played // 50, 6)) if pos in ["LB", "CB", "RB"] else random.randint(0, min(minutes_played // 50, 9)) if pos in ["DM", "CM"] else random.randint(0, min(minutes_played // 50, 12)) if pos in ["AM", "LM", "RM"] else random.randint(0, min(minutes_played // 50, 19)))(position)


        return {
            'first_name': first_name,
            'last_name': last_name,
            'position': position,
            'nationality': nationality,
            'club': club,
            'dob': date_of_birth, 
            'matches_played': matches_played,
            'minutes_played': minutes_played,
            'goals': goals,
            'assists': assists
        }
    # TODO add a piece of code that allows you to create one fake club with 23 players
    