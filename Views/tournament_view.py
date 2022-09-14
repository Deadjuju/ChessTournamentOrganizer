from abc import ABC, abstractmethod

from Views.messages import MessageView


class TournamentView(MessageView, ABC):

    @classmethod
    @abstractmethod
    def prompt_for_multiple_choices_field(cls, text: str, choices: list[tuple[str, str, str]]):
        """user choice for multiple choices field"""

    @classmethod
    @abstractmethod
    def prompt_for_str_field(cls, text: str, label: str):
        """user choice for input field"""
