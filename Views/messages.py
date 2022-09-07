"""
Abstract class for messages view
"""
from abc import ABC, abstractmethod


class MessageView(ABC):

    @classmethod
    @abstractmethod
    def information(cls, text):
        """Displays an informative message"""

    @classmethod
    @abstractmethod
    def warning(cls, invalid_choice: bool = False, text: str = ""):
        """Displays an warning message"""

    @classmethod
    @abstractmethod
    def confirm(cls, message) -> str:
        """Displays confirm message"""
