class InvalidAppPathException(Exception):

    def __init__(self, app, path, reason):
        super().__init__(f"Given {app} path \"{path}\" invalid: {why}")
        self.app = app
        self.path = path
        self.reason = reason

class InvalidSteamPathException(InvalidAppPathException):

    def __init__(self, path, reason):
        super().__init__("Steam", path, reason)

class InvalidGarrysModPathException(InvalidAppPathException):

    def __init__(self, path, reason):
        super().__init__("Garry's Mod", path, reason)

class ImproperTableFormatException(Exception):

    def __init__(self, table, message):
        super().__init__(message)
        self.table = table

class NoSteamRootException(Exception):

    def __init__(self, func):
        super().__init__(f"Cannot call {func.__name__} without existing Steam root folder.")