class ValidationError(Exception):
    """
    The exception raised when there are discrepancies between two
    objects of the same type.
    """

    def __init__(self, message: str) -> None:
        super().__init__(message)
