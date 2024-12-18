import enum

class Color(enum.IntEnum):
    WHITE = 0
    BLACK = 1
    
    def __invert__(self):
        if self == Color.WHITE:
            return Color.BLACK
        else:
            return Color.WHITE

class PieceType(enum.IntEnum):
    PAWN = 0
    KNIGHT = 1
    BISHOP = 2
    ROOK = 3
    QUEEN = 4
    KING = 5

    def humanReadable(self) : 
        if self == PieceType.PAWN:
            return "P"
        elif self == PieceType.KNIGHT:
            return "N"
        elif self == PieceType.BISHOP:
            return "B"
        elif self == PieceType.ROOK:
            return "R"
        elif self == PieceType.QUEEN:
            return "Q"
        elif self == PieceType.KING:
            return "K"

class File(enum.IntEnum) :
    A = 0
    B = 1
    C = 2    
    D = 3
    E = 4
    F = 5
    G = 6
    H = 7

class Rank(enum.IntEnum) :
    ONE = 0
    TWO = 1
    THREE = 2
    FOUR = 3
    FIVE = 4
    SIX = 5
    SEVEN = 6
    EIGHT = 7