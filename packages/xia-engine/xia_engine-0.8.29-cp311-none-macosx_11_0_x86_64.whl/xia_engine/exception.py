class XiaError(Exception):
    """General XIA Error"""
    status_code = 500

    def __init__(self, message, *args):
        super().__init__(message, *args)
        self.message = message


class BadRequestError(XiaError):
    """400: Bad Request"""
    status_code = 400


class AuthenticationError(XiaError):
    """401 Unauthorized"""
    status_code = 401


class AuthorizationError(XiaError):
    """403 Forbidden"""
    status_code = 403


class OutOfQuotaError(XiaError):
    """429 Out of Defined Quota"""
    status_code = 429


class OutOfScopeError(XiaError):
    """403 Out of datascope"""
    status_code = 403


class NotFoundError(XiaError):
    """404 Not Found"""
    status_code = 404


class ConflictError(XiaError):
    """409 Conflict"""
    status_code = 409


class UnprocessableError(XiaError):
    """422 Unprocessable """
    status_code = 422


class ServerError(XiaError):
    """500 Internal Server Error"""
    status_code = 500
