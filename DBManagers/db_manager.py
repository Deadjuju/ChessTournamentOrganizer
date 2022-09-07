from abc import ABC, abstractmethod


class DBManager(ABC):

    @classmethod
    @abstractmethod
    def save(cls, table, data):
        """save in db"""

    @classmethod
    @abstractmethod
    def get_objects_id(cls, db_table, values) -> list[int]:
        """get ids from db"""

    @classmethod
    @abstractmethod
    def get_object(cls, db_table, values):
        """Get object data"""

    @classmethod
    @abstractmethod
    def is_object_exist(cls, db_table, values) -> bool:
        """check if object exist"""

    @classmethod
    def update_attribute(
            cls, db_table, attribute_name, new_attribute_value, instance_id
    ) -> None:
        """update an attribute in database"""

