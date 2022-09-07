import datetime
import sys

from DBManagers.db_manager import DBManager
from Models.player import Player, Gender
from Settings.db_config import PLAYERS_TABLE
from Utils.exceptions import NotValidChoiceError, EmptyFieldError
from Utils.validators import check_multiple_choice, check_not_empty_field
from Views.ConsoleLineViews.players import ConsoleLinePlayerView
from Views.player_view import PlayerView


class PlayerManager:

    def __init__(self, player_view: PlayerView, db_manager: DBManager) -> None:
        self.view = player_view
        self.db_manager = db_manager

    def _player_manager_user_action(self) -> str:
        """User choose an action when player manager start"""

        text = "Voulez-vous créer un joueur ou mettre à jour le score d'un joueur"
        choices = [
            ("1", "Créer un joueur", "CREATE"),
            ("2", "Modifier un joueur", "UPDATE"),
            ("3", "Revenir en arrière", "BACK"),
            ("4", "Quitter", "QUIT")
        ]
        while True:
            user_choice = self.view.prompt_to_create_or_update_player(text=text,
                                                                      choices=choices)
            try:
                return check_multiple_choice(user_choice, choices)
            except NotValidChoiceError:
                self.view.warning(invalid_choice=True)

    def _get_first_name(self) -> str:
        while True:
            first_name = self.view.prompt_for_str_field(text="Veuillez renseigner le prénom du joueur",
                                                        label="prenom")
            try:
                return check_not_empty_field(first_name)
            except EmptyFieldError as e:
                self.view.warning(text=str(e))

    def _get_last_name(self) -> str:
        while True:
            last_name = self.view.prompt_for_str_field(text="Veuillez renseigner le nom de famille du joueur",
                                                       label="nom de famille")
            try:
                return check_not_empty_field(last_name)
            except EmptyFieldError as e:
                self.view.warning(text=str(e))

    def _get_gender(self) -> str:
        choices = [
            ("1", "Homme", "M"),
            ("2", "Femme", "F")
        ]
        while True:
            gender = self.view.prompt_for_multiple_choices_field(text="Veuillez renseigner le sexe du joueur: ",
                                                                 choices=choices)
            try:
                return check_multiple_choice(gender, choices)
            except NotValidChoiceError:
                self.view.warning(invalid_choice=True)

    def _get_birth_date(self) -> str:
        while True:
            text = "Veuillez renseigner la date de naissance (formmat dd/mm/yyyy)"
            label = "date de naissance"
            user_choice = self.view.prompt_for_str_field(text=text, label=label)
            try:
                datetime.datetime.strptime(user_choice, '%d/%m/%Y')
                return user_choice
            except ValueError:
                self.view.warning(text="La date doit être saisie au format dd/mm/yyyy.")

    def _get_full_name_player(self) -> tuple[str, str]:
        first_name = self._get_first_name()
        last_name = self._get_last_name()
        return first_name, last_name

    def _get_info_player(self) -> Player:
        full_name = self._get_full_name_player()
        gender = Gender(self._get_gender())
        birth_date = self._get_birth_date()
        player = Player(
            first_name=full_name[0],
            last_name=full_name[1],
            gender=gender.value,
            date_of_birth=birth_date
        )
        return player

    def _create_player(self) -> bool:
        """
        The user enters the characteristics of the player.
        Player is created if it not exit
        :return: True for success | False in case of failure
        """

        self.view.information(text="Création d'un nouveau joueur")
        player = self._get_info_player()

        search_values = [
            ("first_name", player.first_name), ("last_name", player.last_name)
        ]
        if db_manager.is_object_exist(PLAYERS_TABLE, search_values):
            self.view.warning(text="Ce joueur est déjà connu dans la base de données.")
            return False

        message = f"Voulez vous créer le joueur suivant :\n{player.player_data}"
        if self.view.confirm(message).lower() == "n":
            # "n" = no -> quit the loop
            return False
        self.db_manager.save(PLAYERS_TABLE, player.player_data)
        return True

    def _get_field_to_update(self):
        """user choose a field to update"""

        choices = [
            ("1", "FIRST NAME", "first_name"),
            ("2", "LAST NAME", "last_name"),
            ("3", "RANKING", "ranking")
        ]
        while True:
            text = "Quel champ voumez-vous modifier: "
            field_name = self.view.prompt_for_multiple_choices_field(text=text,
                                                                     choices=choices)
            try:
                return check_multiple_choice(field_name, choices)
            except NotValidChoiceError:
                self.view.warning(invalid_choice=True)

    def _get_new_field_value(self, field: str, instance: Player) -> str | int:
        """
        :param field: field to update
        :param instance: Instance that will be modify
        :return: new value
        """

        text = f"Modifier {field} (valeur : {instance.player_data[field]})"
        while True:
            field_value = self.view.prompt_for_str_field(text=text,
                                                         label=field)
            if field in ("first_name", "last_name"):
                try:
                    return check_not_empty_field(field_value)
                except EmptyFieldError as e:
                    self.view.warning(text=str(e))
            if field == "ranking":
                try:
                    return int(field_value)
                except ValueError:
                    self.view.warning(text="Veuillez renseigner un nombre entier.")

    def _update_player(self) -> bool:
        """
        Get a player by full name
        Then Get a field and update with new value
        :return: True for success | False in case of failure
        """

        self.view.information(text="Modification d'un joueur.")
        full_name = self._get_full_name_player()
        search_values = [
            ("first_name", full_name[0]), ("last_name", full_name[1])
        ]

        if not self.db_manager.is_object_exist(PLAYERS_TABLE, search_values):
            return False

        object_player = self.db_manager.get_object(PLAYERS_TABLE, search_values)
        player = Player(**object_player)
        player_id = object_player.doc_id

        field_to_update = self._get_field_to_update()
        new_value = self._get_new_field_value(field=field_to_update, instance=player)
        self.db_manager.update_attribute(
            db_table=PLAYERS_TABLE,
            attribute_name=field_to_update,
            new_attribute_value=new_value,
            instance_id=player_id
        )
        return True

    def run(self):
        while True:
            """ Create or Read player"""
            create_or_update_player = self._player_manager_user_action()

            match create_or_update_player:
                case "CREATE":

                    if self._create_player():
                        self.view.information("Joueur enregistré")
                    else:
                        self.view.warning(text="Joueur NON enregistré")

                case "UPDATE":
                    if self._update_player():
                        self.view.information(text="Joueur CORRECTEMENT mis à jour")
                    else:
                        self.view.warning(text="Abandons...")

                case "BACK":
                    break

                case "QUIT":
                    sys.exit()


if __name__ == '__main__':
    from DBManagers.tiny_manager import TinyManager

    db_manager = TinyManager()
    player_controller = PlayerManager(ConsoleLinePlayerView, db_manager)
    player_controller.run()
