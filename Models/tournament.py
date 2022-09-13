"""
Model for tournaments
"""
from enum import Enum

from Settings.project_config import NUMBER_OF_TURNS


class TimeControl(Enum):
    BULLET = 'bullet'
    BLITZ = 'blitz'
    QUICK_MOVE = 'quick move'


class Tournament:
    """Class Tournament"""

    def __init__(self,
                 name: str,
                 place: str,
                 start_date: str,
                 end_date: str,
                 description: str,
                 time_control: TimeControl,
                 current_turn: int = 1,
                 turns_id=None,
                 players_id=None) -> None:

        self.name = name
        self.place = place
        self.start_date = start_date
        self.end_date = end_date
        self.description = description
        self.time_control = time_control

        self.number_of_turns: int = NUMBER_OF_TURNS

        self.current_turn = current_turn
        self.turns_id: list[int] = [] if turns_id is None else turns_id
        self.players_id: list[int] = [] if players_id is None else players_id

    @property
    def current_turn(self) -> int:
        return self._current_turn

    @current_turn.setter
    def current_turn(self, value: int) -> None:
        """
        create and toggle value of is_over attribute
        which indicates if tournament is over or not
        """

        if value >= self.number_of_turns:
            self.is_over = True
        else:
            self.is_over = False
        self._current_turn = value

    @property
    def date(self) -> str:
        if self.start_date == self.end_date:
            return self.start_date
        return f"{self.start_date} - {self.end_date}"

    @property
    def tournament_data(self) -> dict:
        data = self.__dict__
        data["is_over"] = self.is_over
        return data

    def __str__(self) -> str:
        return f"{self.name.title()} ({self.place.upper()}): {self.date}"

    def __repr__(self) -> str:
        return f"{self.tournament_data}"

    def next_turn(self) -> None:
        """one turn increment"""

        self.current_turn += 1


if __name__ == '__main__':
    from pprint import pprint

    name = "Tournoi de Chaville"
    place = "Chaville"
    start_date = "01/10/2022"
    end_date = "01/10/2022"
    description = "Tournois d'octobre de Chaville"
    time_control = TimeControl.BULLET.value

    tournament = Tournament(name, place, start_date, end_date, description, time_control)

    print(tournament)
    print(tournament.__repr__())
    pprint(tournament.tournament_data)

    print(f"Finish? {tournament.is_over}")
    print(f"Turn: {tournament.current_turn}")
    tournament.next_turn()
    print(f"Turn: {tournament.current_turn}")
    print(f"Finish? {tournament.is_over}")
    tournament.next_turn()
    print(f"Turn: {tournament.current_turn}")
    print(f"Finish? {tournament.is_over}")
    tournament.next_turn()
    print(f"Turn: {tournament.current_turn}")
    print(f"Finish? {tournament.is_over}")
    tournament.next_turn()
    print(f"Turn: {tournament.current_turn}")
    print(f"Finish? {tournament.is_over}")
