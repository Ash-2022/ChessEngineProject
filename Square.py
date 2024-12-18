import numpy as np
from enum import IntEnum
from Constants import Rank , File
import typing as tt

class Square:
    def __init__(self , squareIndex: int) -> None:
        self.sqIdx = np.uint8(squareIndex) # Creates a 8-bit representation for a square -> 0-63
    def __str__(self) -> str:
        return chr((self.sqIdx % 8) + ord("a")) + str((self.sqIdx // 8) + 1)
    
    @classmethod
    def getSquareFromRankAndFileEnum(cls , rank: IntEnum , file: IntEnum) -> object:
        # cls is a conventionally used name for the class itself
        return cls(rank.value << np.uint8(3) | file.value) # IntEnum.value gives the integer value for the Enum(string) "rank" of type enum
    
    @classmethod
    def getSquareFromString(cls , squareString: str) -> object:
        # cls is a conventionally used name for the class itself
        f = np.uint8(ord(squareString[0]) - ord("a"))
        r = np.uint8(int(squareString[1]) - 1)
        return cls((r << np.uint8(3)) | f) # 8 * rank + file
    
    def toBitBoard(self) ->np.uint64:
        return np.uint64(1) << self.sqIdx
    
if __name__ == "__main__":
    print(Square.getSquareFromString("a1"))