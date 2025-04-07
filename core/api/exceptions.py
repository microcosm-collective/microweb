class APIException(Exception):
    """
    Encapsulates HTTP errors thrown by the microcosm API.
    """

    def __init__(self, error_message, status_code=None, detail=None):
        self.status_code = status_code
        self.detail = detail
        super().__init__(error_message)

    def __str__(self):
        return 'HTTP status: %d: %s' % (self.status_code, self.message)