
class InvalidFillingError(Exception):
    pass


class FillingShapeError(InvalidFillingError):
    pass


class TileLocationError(InvalidFillingError):
    pass

class InvalidFillingException(Exception):
    pass


class MissingPlaneException(InvalidFillingException):
    pass


class PlaneDirectionException(InvalidFillingException):
    pass


class PlaneLocationException(InvalidFillingException):
    pass
