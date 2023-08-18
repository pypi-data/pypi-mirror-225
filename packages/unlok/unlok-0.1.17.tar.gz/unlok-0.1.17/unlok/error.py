class UnlokError(Exception):
    """Base class for all unlok exceptions."""

    pass


class NoUnlokFound(UnlokError):
    pass
