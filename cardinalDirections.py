class CardinalDirection:
    __match_args__ = tuple("direction")

    def __init__(self, direction):
        if direction not in "NORTH SOUTH WEST EAST".split():
            raise ValueError(f"{direction} is not a cardinal direction.")
        self.direction = direction

    def opposite_direction(self):
        if self.direction == "NORTH":
            return SOUTH
        elif self.direction == "WEST":
            return EAST
        elif self.direction == "SOUTH":
            return NORTH
        elif self.direction == "EAST":
            return WEST

    def __key(self):
        return self.direction

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, CardinalDirection):
            return self.__key() == other.__key()
        return NotImplemented

    def __repr__(self):
        return repr(self.__key())


NORTH = CardinalDirection("NORTH")
WEST = CardinalDirection("WEST")
SOUTH = CardinalDirection("SOUTH")
EAST = CardinalDirection("EAST")
