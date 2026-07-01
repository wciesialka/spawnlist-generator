class InvalidPathException(Exception):

    def __init__(self, path, reason):
        super().__init__(f"Path \"{path}\" invalid: {reason}")
        self.path = path
        self.reason = reason

class InvalidAppPathException(InvalidPathException):

    def __init__(self, app, path, reason):
        super().__init__(path, f"Invalid {app} path: {reason}")
        self.app = app
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