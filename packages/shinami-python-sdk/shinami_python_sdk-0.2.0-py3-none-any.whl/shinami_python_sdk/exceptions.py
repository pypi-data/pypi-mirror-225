class ShinamiInvalidApiTokenException(Exception):
    def __init__(self, message: str) -> None:
        self.message = message


class ShinamiWalletExistsException(Exception):
    def __init__(self, message: str) -> None:
        self.message = message


class ShinamiWalletNotFoundException(Exception):
    def __init__(self, message: str) -> None:
        self.message = message


class ShinamiWalletException(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
