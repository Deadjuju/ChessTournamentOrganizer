"""custom validators"""
from Utils.exceptions import NotValidChoiceError, EmptyFieldError


def check_multiple_choice(user_choice, choices):
    for choice in choices:
        if user_choice in choice[0]:
            return choices[int(user_choice) - 1][-1]
    message = f"Invalid user choice: {user_choice}."
    raise NotValidChoiceError(message)


def check_not_empty_field(user_value):
    if user_value == "":
        message = "Empty value not allowed"
        raise EmptyFieldError(message)
    return user_value
