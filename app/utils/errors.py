class FileSaveError(Exception):
    """
    Raised on bad HTTP request.
    """
    def __init__(self, message: str):
        self.status_code = 404
        self.message = message
        super().__init__(self.message)


class FilePathError(Exception):
    """
    Raised on bad HTTP request.
    """
    def __init__(self, message: str):
        self.status_code = 404
        self.message = message
        super().__init__(self.message)


class FileReadError(Exception):
    """
    Raised on bad HTTP request.
    """
    def __init__(self, message: str):
        self.status_code = 500
        self.message = message
        super().__init__(self.message)


class FileProcessingError(Exception):
    """
    Raised on bad HTTP request.
    """
    def __init__(self, message: str):
        self.status_code = 500
        self.message = message
        super().__init__(self.message)
