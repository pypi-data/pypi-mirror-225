# Tools useful in optimeering apps
# For now, this is included in the app itself
# Once it is more mature we can port it over to its own project

#### EXCEPTIONS


class MissingDataError(ValueError):
    """Raised when we have no data (but should have) for an object (e.g. graph, table) in the app"""

    pass
