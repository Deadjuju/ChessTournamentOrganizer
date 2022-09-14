import datetime
import sys

from DBManagers.db_manager import DBManager
from Models.player import Player
from Models.tournament import Tournament, TimeControl
from Settings.db_config import TOURNAMENTS_TABLE, PLAYERS_TABLE
from Settings.project_config import NUMBERS_OF_PLAYERS
from Utils.exceptions import NotValidChoiceError, EmptyFieldError
from Utils.validators import check_multiple_choice, check_not_empty_field
from Views.ConsoleLineViews.tournament import TournamentLinePlayerView
from Views.tournament_view import TournamentView


class TournamentManager:

    def __init__(self, tournament_view: TournamentView, db_manager: DBManager) -> None:
        self.view = tournament_view
        self.db_manager = db_manager

    def _get_not_empty_str(self, text: str, label: str) -> str:
        """
        Get a user's response in str format concerning a field (not empty)
        :param text: text to display
        :param label: name od field
        :return: user response
        """

        while True:
            name = self.view.prompt_for_str_field(text, label)
            try:
                return check_not_empty_field(name)
            except EmptyFieldError as e:
                self.view.warning(text=str(e))

    def _get_valid_date(self, text: str, label: str) -> str:
        """
        Get a user's response in date format concerning a date field
        :param text: text to display
        :param label: name od field
        :return: user response
        """

        while True:
            user_choice = self.view.prompt_for_str_field(text=text, label=label)
            try:
                datetime.datetime.strptime(user_choice, '%d/%m/%Y')
                return user_choice
            except ValueError:
                self.view.warning(text="La date doit être saisie au format dd/mm/yyyy.")

    def _get_answer_in_multi_choices(self, text: str, choices: list) -> str:
        """
        Offers several choices to the user and checks his answer
        :param text: Text to display
        :param choices: user choices
        :return: user choice
        """
        choices.sort(key=lambda x: x[0])
        while True:
            user_choice = self.view.prompt_for_multiple_choices_field(text=text,
                                                                      choices=choices)
            try:
                return check_multiple_choice(user_choice, choices)
            except NotValidChoiceError:
                self.view.warning(invalid_choice=True)

    def _are_conditions_met_to_create_tournament(self) -> bool:
        """
        Checks if the conditions are met to be able to create a tournament.
        Two points are analysed:
        • The number of players already created
        • The number of players available
        :return: True if all conditions are met else False
        """

        if self.db_manager.count_objects_in_db(PLAYERS_TABLE) < NUMBERS_OF_PLAYERS:
            self.view.warning(text="Il n'y a pas assez de joueur enregistré pour créer un tournois")
            return False

        players_in_db: list = self.db_manager.get_all_objects_from_table(PLAYERS_TABLE)
        free_players = len(
            ["" for player in players_in_db if not player['is_already_in_a_tournament']]
        )
        if free_players < NUMBERS_OF_PLAYERS:
            self.view.warning(text="Il n'y a pas assez de joueur disponible pour créer un tournois")
            return False

        return True

    def _are_conditions_met_to_start_tournament(self) -> bool:
        """
        Checks if the conditions are met to be able to load a tournament.
        :return: True if all conditions are met else False
        """

        if self.db_manager.count_objects_in_db(TOURNAMENTS_TABLE) == 0:
            return False
        return True

    def _get_tournament_manager_user_action(self) -> str:
        """
        User choice to start tournament manager.
        Adapts the list of choices offered to the user according to the conditions met.
        :return: user choice
        """

        text = "Voulez-vous créer un tournois ou ouvrir un tournois existant"
        choices = []

        if self._are_conditions_met_to_create_tournament():
            choices.append((str(len(choices) + 1), "Créer un tournois", "CREATE"))

        if self._are_conditions_met_to_start_tournament():
            choices.append((str(len(choices) + 1), "Ouvrir un tournois", "OPEN"))

        if len(choices) == 0:
            return "BACK"

        choices.append((str(len(choices) + 1), "Revenir en arrière", "BACK"))
        choices.append((str(len(choices) + 1), "Quitter", "QUIT"))
        return self._get_answer_in_multi_choices(text, choices)

    def _get_time_control(self) -> str:
        text = "Veuillez renseigner le type de control du temps"
        choices = [
            ("1", "Bullet", "bullet"),
            ("2", "Blitz", "blitz"),
            ("3", "Coup rapide", "quick move"),
        ]
        return self._get_answer_in_multi_choices(text, choices)

    def _get_name(self) -> str:
        return self._get_not_empty_str(text="Veuillez renseigner le lieu du tournois",
                                       label="nom du tournois")

    def _get_place(self) -> str:
        return self._get_not_empty_str(text="Veuillez renseigner le nom du tournois",
                                       label="lieu de déroulement du tournois")

    def _get_description(self) -> str:
        return self._get_not_empty_str(text="Description du tournois",
                                       label="description")

    def _get_player_first_name(self) -> str:
        return self._get_not_empty_str(text="Prénom du joueur",
                                       label="prenom")

    def _get_player_last_name(self) -> str:
        return self._get_not_empty_str(text="Nom de famille du joueur",
                                       label="nom de famille")

    def _get_start_date(self) -> str:
        return self._get_valid_date(text="Veuillez renseigner la date de début du tournois (formmat dd/mm/yyyy)",
                                    label="Début du tournois")

    def _get_end_date(self) -> str:
        return self._get_valid_date(text="Veuillez renseigner la date de fin du tournois (formmat dd/mm/yyyy)",
                                    label="Fin du tournois")

    def _get_tournament_info(self) -> Tournament:
        """
        Get all info to create an instance of tournament
        :return: Instance of tournament
        """
        name = self._get_name()
        place = self._get_place()
        start_date = self._get_start_date()
        end_date = self._get_end_date()
        description = self._get_description()
        time_control = TimeControl(self._get_time_control())
        tournament = Tournament(
            name=name,
            place=place,
            start_date=start_date,
            end_date=end_date,
            description=description,
            time_control=time_control.value
        )
        return tournament

    def _is_player_exist(self, search_values: list[tuple[str, str]]) -> bool:
        """
        Checks if the requested player exists in the db and informs/warns the user accordingly.
        :param search_values:
        :return:
        """
        if self.db_manager.is_object_exist(PLAYERS_TABLE, search_values):
            self.view.information(text="Joueur selectionné.")
            return True
        self.view.warning(text="Joueur non trouvé.")

    def _select_a_player(self) -> None | int:
        """
        Search for a player in the database using his first and last name
        :return: Player id in db if found else None
        """

        search_values = [
            ("first_name", self._get_player_first_name()),
            ("last_name", self._get_player_last_name())
        ]
        if not self._is_player_exist(search_values):
            return
        object_player = self.db_manager.get_object(PLAYERS_TABLE, search_values)
        player = Player(**object_player)
        add_in_tournament = self.view.confirm(message=f"Ajouter le joueur '{player}' au tournoi?").lower()
        if add_in_tournament == "n":
            return
        return object_player.doc_id

    def _add_players(self, tournament: Tournament) -> bool:
        """
        Adds players based on the number of players per tournament
        :param tournament: tournament concerned
        :return: True if all players are correctly added, else False
        """

        self.view.information(text="Ajout des joueurs :")

        while len(tournament.players_id) < NUMBERS_OF_PLAYERS:
            self.view.information(text=f"Ajout du joueur {len(tournament.players_id) + 1}")
            player_id = self._select_a_player()

            if player_id in tournament.players_id:
                self.view.warning(text="Ce joueur est déjà enregistré pour le tournois.")
                player_id = None

            if player_id is not None:
                tournament.players_id.append(player_id)
                self.view.information(text="Joueur correctement ajouté au tournois.")
                print(tournament.players_id)
            else:
                self.view.warning(text="Joueur non enregistré.")

                if self.view.confirm(
                        message="Continuer l'enregistrement des joueurs? "
                ).lower() == "n":
                    return False
        return True

    def _save_tournament_and_update_players(self, tournament: Tournament) -> None:
        """
        Save the tournaments in the db.
        Updates the status of players in the db.
        :param tournament:
        :return:
        """

        self.db_manager.save(TOURNAMENTS_TABLE, tournament.tournament_data)
        self.db_manager.update_attribute_many(
                db_table=PLAYERS_TABLE,
                attribute_name="is_already_in_a_tournament",
                new_attribute_value=True,
                instances_id_list=tournament.players_id
            )

    def _create_tournament(self) -> bool:
        """
        Actions to create a tournament.
        :return: True if tournament success to create, else false
        """

        self.view.information(text="Création d'un nouveau tournois")

        tournament: Tournament = self._get_tournament_info()

        search_values = [
            ("first_name", tournament.name), ("last_name", tournament.start_date)
        ]
        if db_manager.is_object_exist(TOURNAMENTS_TABLE, search_values):
            self.view.warning(text="Ce tournois est déjà connu dans la base de données.")
            return False

        self._add_players(tournament)

        message = f"Voulez vous créer le tournois suivant :\n{tournament.tournament_data}"
        if self.view.confirm(message).lower() == "n":
            return False

        self._save_tournament_and_update_players(tournament)
        return True

    def run(self) -> None:
        """ Create or load tournament"""

        while True:
            create_or_get_tournament: str = self._get_tournament_manager_user_action()

            match create_or_get_tournament:
                case "CREATE":
                    self._create_tournament()

                case "OPEN":
                    print("OPEN")

                case "BACK":
                    break

                case "QUIT":
                    sys.exit()


if __name__ == '__main__':
    from DBManagers.tiny_manager import TinyManager

    db_manager = TinyManager()
    tournament = TournamentManager(TournamentLinePlayerView, db_manager=db_manager)
    tournament.run()
