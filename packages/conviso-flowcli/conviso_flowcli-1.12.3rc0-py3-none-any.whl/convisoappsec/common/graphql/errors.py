class Error(Exception):
    pass


class AuthenticationError(Error):
    pass


class ServerError(Error):
    pass


class ReponseError(Error):
    pass
