from Views.ConsoleLineViews.messages import ConsoleLineMessageView
from Views.tournament_view import TournamentView


class TournamentLinePlayerView(ConsoleLineMessageView, TournamentView):

    @classmethod
    def prompt_for_multiple_choices_field(cls, text: str, choices: list[tuple[str, str, str]]) -> str:
        print(text)
        for choice in choices:
            print(f"Taper {choice[0]} -> {choice[1]}")
        user_choice = input("Your choice: ")
        return user_choice

    @classmethod
    def prompt_for_str_field(cls, text: str, label: str) -> str:
        print(text)
        user_choice = input(f"> {label.upper()}: ")
        return user_choice
