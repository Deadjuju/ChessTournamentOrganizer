"""
Model for players
"""
from enum import Enum


class Gender(Enum):
    MALE = 'M'
    FEMALE = 'F'


class Person:

    def __init__(self,
                 first_name: str,
                 last_name: str,
                 gender: Gender,
                 date_of_birth: str) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.date_of_birth = date_of_birth

    @property
    def full_name(self):
        return f"{self.last_name.upper()} {self.first_name.title()}"
    
    
class Player(Person):

    def __init__(self,
                 first_name: str,
                 last_name: str,
                 gender: Gender,
                 date_of_birth: str) -> None:
        super().__init__(first_name, last_name, gender, date_of_birth)
        self.ranking: int = 0
        self.tournament_score: float = 0
        self.players_already_faced: list = []
        self.is_already_in_a_tournament: bool = False

    @property
    def player_data(self) -> dict:
        data = self.__dict__
        return data

    def __str__(self) -> str:
        return f"{self.full_name}"

    def __repr__(self) -> str:
        return f"{self.player_data}"


if __name__ == "__main__":

    player = Player("Bob", "Razowski", Gender.MALE.value, "04/04/2000")

    print(player.full_name)
    print(player.player_data)
    print(player.__repr__())
