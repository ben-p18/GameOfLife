
class Error(Exception):
    pass

class IdenticalCoordinatesError(Error):
    pass

class NegativeCoordinateError(Error):
    pass

class NegativeLiveCellsError(Error):
    pass