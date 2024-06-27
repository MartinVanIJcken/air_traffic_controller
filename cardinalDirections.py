class CardinalDirection:
    __match_args__ = tuple("direction")

    def __init__(self, direction):
        if direction not in "NORTH SOUTH WEST EAST".split():
            raise ValueError(f"{direction} is not a cardinal direction.")
        self.direction = direction

    def opposite_direction(self):
        if self.direction == "NORTH":
            return CardinalDirection("SOUTH")
        elif self.direction == "WEST":
            return CardinalDirection("EAST")
        elif self.direction == "SOUTH":
            return CardinalDirection("NORTH")
        elif self.direction == "EAST":
            return CardinalDirection("WEST")

    def __eq__(self, other):
        return self.direction == other.direction

    def __repr__(self):
        return self.direction

NORTH = CardinalDirection("NORTH")
WEST = CardinalDirection("WEST")
SOUTH = CardinalDirection("SOUTH")
EAST = CardinalDirection("EAST")
