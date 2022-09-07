from typing import Optional

from tinydb.database import TinyDB as TinyDBType
from tinydb.table import Table as TableType
from tinydb.table import Document as DocumentType
from tinydb.queries import QueryInstance

from DBManagers.db_manager import DBManager


class TinyManager(DBManager):

    @classmethod
    def save(cls, table: TableType, data: dict):
        table.insert(data)

    @classmethod
    def _generate_query(cls, values: list[tuple[str, str]]) -> QueryInstance:

        custom_query = frozenset(
            [("==", (value[0],), value[1]) for value in values]
        )

        def test_func(val):
            dict_values = dict(values)
            for key in dict_values:
                if not dict_values[key] == val.get(key):
                    return False
            return True

        generated_query = QueryInstance(test=test_func, hashval=(custom_query, ))
        return generated_query

    @classmethod
    def get_objects_id(cls, db_table: TableType, values: list[tuple[str, str]]) -> list[int]:
        """
            values: (list[tuple[str, str]]): [("field_name", value), ]
        """

        query = cls._generate_query(values)
        instances = db_table.search(query)
        return [instance.doc_id for instance in instances]

    @classmethod
    def get_object(cls, db_table: TableType, values: list[tuple[str, str]]) -> Optional[DocumentType]:
        query = cls._generate_query(values)
        return db_table.get(query)

    @classmethod
    def is_object_exist(cls, db_table: TableType, values: list[tuple[str, str]]) -> bool:
        return bool(cls.get_object(db_table, values))


if __name__ == '__main__':

    from Models.player import Player, Gender
    from Settings.db_config import DB, PLAYERS_TABLE

    db = DB

    """ insert players in db """
    players = [
        ("Bob", "Razowski", Gender.MALE.value, "01/01/1950"),
        ("Jean-Jacques", "Boubou", Gender.MALE.value, "01/01/1950"),
        ("Bruce", "Wayne", Gender.MALE.value, "01/01/1950"),
        ("Sylvère", "Causard", Gender.MALE.value, "01/01/1950"),
        ("Serj", "Tankian", Gender.MALE.value, "01/01/1950"),
        ("Marie", "Curie", Gender.FEMALE.value, "01/01/1950"),
        ("Kimberley", "Rose", Gender.FEMALE.value, "01/01/1950"),
        ("Alicia", "Keys", Gender.FEMALE.value, "01/01/1950"),
        ("Angela", "Gossow", Gender.FEMALE.value, "01/01/1950"),
        ("Kirk", "Lazarus", Gender.MALE.value, "01/01/1950"),
        ("Philippe", "Rastier", Gender.MALE.value, "01/01/1950")
    ]

    # for player in players:
    #     player_to_save = Player(player[0], player[1], player[2], player[3])
    #     print(player)
    #     TinyManager.save(PLAYERS_TABLE, player_to_save.player_data)

    search_values = [("first_name", "Bob"), ("last_name", "Razowski")]
    instances = TinyManager.get_objects_id(PLAYERS_TABLE, search_values)
    print(instances)

    print(TinyManager.get_object(PLAYERS_TABLE, search_values))
    print(TinyManager.is_object_exist(PLAYERS_TABLE, search_values))

    search_values = [("gender", "F")]
    instances = TinyManager.get_objects_id(PLAYERS_TABLE, search_values)
    print(instances)
