import numpy as np
from Square import Square
from Constants import Rank , File
import typing as tt

"""
    Initialize the board using 
    LERF -> Little Endian Rank File Mapping
    Board = 
    [
        [h8 , g8 , f8 , e8 , d8 , c8 , b8 , a8],
        [h7 , g7 , f7 , e7 , d7 , c7 , b7 , a7],
        [h6 , g6 , f6 , e6 , d6 , c6 , b6 , a6],
        [h5 , g5 , f5 , e5 , d5 , c5 , b5 , a5],
        [h4 , g4 , f4 , e4 , d4 , c4 , b4 , a4],
        [h3 , g3 , f3 , e3 , d3 , c3 , b3 , a3],
        [h2 , g2 , f2 , e2 , d2 , c2 , b2 , a2],
        [h1 , g1 , f1 , e1 , d1 , c1 , b1 , a1],
    ]
    Keep a1 = 0 and b1 = 2 so on til h8 = 63 , i.e Square = 8*rank + file , both are 0-indexed
    eg : f7 = 8*6 + 5 = 53
    LS1B : It identifies the rightmost bit set to 1 
    in the binary representation of a number and often 
    isolates it for further operations.

    LS1B(x) = x AND (-x) 
    -x = ~x + 1 => 2's compliment of x

    The De Bruijn bitscan is a clever algorithm used to efficiently determine the position of the LS1B
    in a binary number. It is highly efficient because it avoids looping and uses a single multiplication
    combined with a lookup table.
    LS1B(in binary) * DE Bruijn's constant = position of LS1B in binary
    (represented by log2(64) = 6 Most significant bits)
    so shift the number by (64-6)=58 to get the position and use that to lookup from table
"""

EMPTY_BB = np.uint64(0)

# De Bruijn's constant for 64-bit systems
# NOTE: only works if bb is non-zero
debruijn = np.uint64(0x03f79d71b4cb0a89)

ls1b_lookup = np.array(
        [ 0,  1, 48,  2, 57, 49, 28,  3,
         61, 58, 50, 42, 38, 29, 17,  4,
         62, 55, 59, 36, 53, 51, 43, 22,
         45, 39, 33, 30, 24, 18, 12,  5,
         63, 47, 56, 27, 60, 41, 37, 16,
         54, 35, 52, 21, 44, 32, 23, 11,
         46, 26, 40, 15, 34, 20, 31, 10,
         25, 14, 19,  9, 13,  8,  7,  6],
        dtype=np.uint8)

msb_lookup = np.array(
        [ 0, 47,  1, 56, 48, 27,  2, 60,
         57, 49, 41, 37, 28, 16,  3, 61,
         54, 58, 35, 52, 50, 42, 21, 44,
         38, 32, 29, 23, 17, 11,  4, 62,
         46, 55, 26, 59, 40, 36, 15, 53,
         34, 51, 20, 43, 31, 22, 10, 45,
         25, 39, 14, 33, 19, 30,  9, 24,
         13, 18,  8, 12,  7,  6,  5, 63],
        dtype=np.uint8)

def msbBitScan(bb : np.uint64) -> np.uint8:
    """
    Finds the position of the most significant bit set in the given bitboard.
    This function works by propagating all the set bits to the right, and then
    performing a De Bruijn multiplication to find the position of the most significant bit.
    """
    bb |= bb >> np.uint8(1)
    bb |= bb >> np.uint8(2)
    bb |= bb >> np.uint8(4)
    bb |= bb >> np.uint8(8)
    bb |= bb >> np.uint8(16)
    bb |= bb >> np.uint8(32)
    return msb_lookup[(bb * debruijn) >> np.uint8(58)]

def ls1bBitScan(bb : np.uint64) -> np.uint8:
    return ls1b_lookup[((bb & -bb) * debruijn) >> np.uint8(58)]

def occupiedSquares(bb: np.uint64) -> tt.Generator[Square , None , None]:
    """
    Generator function that yields squares occupied by pieces in the given bitboard.

    This function identifies all the squares that are currently occupied by pieces
    on a chessboard, represented by the given bitboard 'bb'. It utilizes the 
    least significant 1 bit (LS1B) method to find the index of each occupied square,
    converts it to a `Square` object, and yields it. The bitboard 'bb' is updated
    by removing the identified square until no occupied squares remain.

    Args:
        bb (np.uint64): A 64-bit integer representing the bitboard where each bit 
                        corresponds to a square on the chessboard (1 for occupied,
                        0 for empty).

    Yields:
        Square: The next occupied square on the board as a `Square` object.
    """

    while bb != EMPTY_BB:
        lsb_square = Square(ls1bBitScan(bb))
        yield lsb_square
        bb ^= lsb_square.toBitBoard()
def populationCount(bb : np.uint64) -> int:
    """Brian Kernighan's way to find the population count(No. of 1's in a bitboard)

    Args:
        bb (np.uint64): Bitboard

    Returns:
        int: Population Count
    """
    count:int = 0
    while bb : 
        count += 1
        bb &= bb - np.uint8(1) # Clear the LS1B
    return count

def checkIfSquareIsSet(bb:np.uint64, sq:Square) -> bool:
    """
    Checks if a particular square is occupied on the bitboard.

    This function determines whether the square represented by `sq` is 
    set (i.e., occupied) in the given bitboard `bb`.

    Args:
        bb (np.uint64): A 64-bit integer representing the bitboard where 
                        each bit corresponds to a square on the chessboard 
                        (1 for occupied, 0 for empty).
        sq (Square): A `Square` object representing the square to be checked 
                     for occupation.

    Returns:
        bool: True if the square is set (occupied) on the bitboard, False if not.
    """

    return (sq.toBitBoard() & bb) != EMPTY_BB

def bitBoardToStr(bb:np.uint64) -> str:
    """
    Converts a bitboard to a string representation.

    This function takes a bitboard (a 64-bit integer) as input and returns a string representation of the bitboard. The string consists of a 8x8 grid of characters, where a '1' represents a set bit and a '.' represents a cleared bit. The rows and columns of the grid are ordered such that the rank increases from top to bottom and the file increases from left to right.

    Args:
        bb (np.uint64): A 64-bit integer representing the bitboard.

    Returns:
        str: A string representation of the bitboard.
    """
    bb_str = []
    for r in reversed(Rank):
        for f in File:
            sq = Square.getSquareFromRankAndFileEnum(r, f)
            if checkIfSquareIsSet(bb, sq):
                bb_str.append('1')
            else:
                bb_str.append('.')
        bb_str.append('\n')
    return ''.join(bb_str)

def clearSquareOnBB(bb:np.uint64, sq:Square) -> np.uint64:
    return (~sq.toBitBoard()) & bb

def setSquareOnBB(bb :np.uint64, sq:Square) -> np.uint64:  
    return sq.toBitBoard() | bb

if __name__ == "__main__":
    def test_bitscan():
        assert ls1bBitScan(np.uint64(0xF000000000000000)) == np.uint8(60)
        assert msbBitScan(np.uint64(0xF000000000000000)) == np.uint8(63)

    def test_popcount():
        assert populationCount(np.uint64(0xF0000F00000F0000)) == np.uint8(12)
    test_bitscan()
    test_popcount()