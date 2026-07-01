class InvalidPathException(Exception):

    def __init__(self, app, path, reason):
        super().__init__(f"Given {app} path \"{path}\" invalid: {why}")
        self.app = app
        self.path = path
        self.reason = reason

class InvalidSteamPathException(InvalidPathException):

    def __init__(self, path, reason):
        super().__init__("Steam", path, reason)

class ImproperTableFormatException(Exception):

    def __init__(self, table, message):
        super().__init__(message)
        self.table = table