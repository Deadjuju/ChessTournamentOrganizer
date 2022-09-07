class GeneralController:

    def _ask_and_check_field(self, field, message: str) -> str:
        """Ask and control of a field
                Args:
                    field (): Method to get the value of a field
                    message (str): Message in case of warning
                Returns:
                    user_choice (str): the field value
                """

        while True:
            user_choice = field()
            if user_choice != "":
                return user_choice
            else:
                self.view.warning(message=message)
