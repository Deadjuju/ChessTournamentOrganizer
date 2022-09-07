"""Custom Exceptions"""


class NotValidChoiceError(Exception):
    def __init__(self, message):
        super().__init__(message)


class EmptyFieldError(Exception):
    def __init__(self, message):
        super().__init__(message)
