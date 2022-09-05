from abc import ABC, abstractmethod


class DBManager(ABC):

    @abstractmethod
    def save(self, table, data):
        """save in db"""

    @abstractmethod
    def get_instances_id(self, db_tables, values: list[tuple[str, str]]) -> list[int]:
        """get ids from db"""
