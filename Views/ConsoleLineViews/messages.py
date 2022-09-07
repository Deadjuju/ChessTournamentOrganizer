from Views.messages import MessageView


class ConsoleLineMessageView(MessageView):

    @classmethod
    def information(cls, text: str) -> None:
        label = "> INFORMATION: "
        print(f"{'_' * (len(label) + len(text))}\n{label}{text}")

    @classmethod
    def warning(cls, invalid_choice: bool = False, text: str = "") -> None:
        label = "> ATTENTION: "
        if invalid_choice:
            text = "Choix non valide"
        print(f"{'_' * (len(label) + len(text))}\n{label}{text}")

    @classmethod
    def confirm(cls, message) -> str:
        print(message)
        user_choice = input("Tapez 'n' pour annuler sinon validez.\n (n / ->) > ")
        return user_choice
