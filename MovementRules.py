import numpy as np
import typing as tt 
import BitBoard
from Square import Square
from Constants import Rank, File, Color

"""
This file contains various pre-computed bitboards and bitboard tables for move generation and general use
"""
EMPTY_BB = np.uint64(0)

RANKS = np.array(
            [np.uint64(0x00000000000000FF) << np.uint8(8*i) for i in range(8)],
            dtype=np.uint64)
FILES = np.array(
            [np.uint64(0x0101010101010101) << np.uint8(i) for i in range(8)],
            dtype=np.uint64)

RANK_MASKS = np.fromiter(
        (RANKS[i//8] for i in range(64)),
        dtype=np.uint64,
        count=64)
# fromiter create a ndarray out of a iterable object

FILE_MASKS = np.fromiter(
        (FILES[i%8] for i in range(64)),
        dtype=np.uint64,
        count=64)

A1H8_DIAG = np.uint64(0x8040201008040201)
H1A8_ANTIDIAG = np.uint64(0x0102040810204080)

CENTER = np.uint64(0x00003C3C3C3C0000)
# e6 , d6 , e5 , d5 , e4 , d4 , e3 , d3

# Precomputing the principal diagonal masks

def precomputeDiagonalMasks() -> tt.Tuple[np.uint64 , np.uint64]:
    """
    Precomputes the principal diagonal and anti-diagonal masks for each square on the board.

    Returns a tuple of two 15-element numpy arrays, where each element is a 64-bit bitboard
    representing the principal diagonal and anti-diagonal respectively, for each possible
    (file - rank) and (file + rank) combination.

    The principal diagonal masks are indexed by (file - rank) + 7, while the anti-diagonal
    masks are indexed by (file + rank).

    This function is used to initialize the DIAG_MASKS and ANTIDIAG_MASKS global variables.
    """
    principal_diags = [np.uint64(0)] * 15  # One for each possible (file - rank)
    anti_diags = [np.uint64(0)] * 15       # One for each possible (file + rank)

    for square in range(64):
        file = square % 8
        rank = square // 8
        diag_id = file - rank + 7    # Offset by 7 to make diag_id non-negative
        anti_diag_id = file + rank   # Anti-diag_id ranges from 0 to 14
        principal_diags[diag_id] |= (np.uint64(1) << np.uint8(square))
        anti_diags[anti_diag_id] |= (np.uint64(1) << np.uint8(square))

    return np.array(principal_diags , dtype=np.uint64), np.array(anti_diags , dtype=np.uint64)

# Compute the masks
DIAG_MASKS , ANTIDIAG_MASKS = precomputeDiagonalMasks()

# # Return the result in hexadecimal format for better readability
# print([hex(mask) for mask in DIAG_MASKS])

# Dynamically compute a mask for a specific square
def getDiagonalMasks(square: int) -> tt.Tuple[np.uint64 , np.uint64]:
    """
    Dynamically computes the principal diagonal and anti-diagonal masks for a given square on the chessboard.

    Args:
        square: The square index (0-63) for which to compute the diagonal masks.

    Returns:
        A tuple of two 64-bit bitboards, where the first element is the principal diagonal mask and
        the second element is the anti-diagonal mask for the given square.
    """
    file = square % 8
    rank = square // 8
    diag_id = file - rank + 7
    anti_diag_id = file + rank

    # Dynamically retrieve the mask
    principal_mask = DIAG_MASKS[diag_id]
    anti_mask = ANTIDIAG_MASKS[anti_diag_id]
    
    return principal_mask, anti_mask

# Bitboards for move generation


# KING

def getKingMovesFromSquareIndex(i:int) -> np.uint64:
    """
    Computes the king's possible moves from a given square index on the chessboard.

    This function calculates the bitboard representing all possible moves for a king
    located at a specific square index 'i'. It takes into account the boundaries of
    the chessboard to ensure the king does not move off the edges.

    Args:
        i (int): The index of the square on the chessboard (0-63).

    Returns:
        np.uint64: A bitboard mask representing all possible moves for a king from
        the given square index.
        (doesn't include current position of king)
    """

    sq = Square(i)
    bb = sq.toBitBoard()
    ne = (bb & ~FILES[File.A]) << np.uint8(7)
    n  = bb << np.uint8(8)
    nw = (bb & ~FILES[File.H]) << np.uint8(9)
    w  = (bb & ~FILES[File.H]) << np.uint8(1)
    se = (bb & ~FILES[File.H]) >> np.uint8(7)
    s  = bb >> np.uint8(8)
    sw = (bb & ~FILES[File.A]) >> np.uint8(9)
    e  = (bb & ~FILES[File.A]) >> np.uint8(1)

    return nw | n | ne | e | se | s | sw | w

KING_MOVES = np.fromiter(
        (getKingMovesFromSquareIndex(i) for i in range(64)),
        dtype=np.uint64,
        count=64)
# print(hex(getKingMovesFromSquareIndex(44)))

# KNIGHT 

def getKnightMovesFromSquareIndex(i: int) -> np.uint64:
    """
    Computes the knight's possible moves from a given square index on the chessboard.

    This function calculates the bitboard representing all possible moves for a knight
    located at a specific square index 'i'. It takes into account the boundaries of
    the chessboard to ensure the knight does not move off the edges.

    Args:
        i (int): The index of the square on the chessboard (0-63).

    Returns:
        np.uint64: A bitboard mask representing all possible moves for a knight from
        the given square index.
    """
    sq = Square(i)
    bb = sq.toBitBoard()

    # Boundary Conditions Management : 

    m1 = ~(FILES[File.A] | FILES[File.B])
    m2 = ~FILES[File.A]
    m3 = ~FILES[File.H]
    m4 = ~(FILES[File.H] | FILES[File.G])

    # If Moving Right by 2 , Do not generate using the A or B Files
    # If Moving Left by 2 , Do not generate using the G or H Files
    # If Moving Right by 1 , Do not generate using the A File
    # If Moving Left by 1 , Do not generate using the H File

    s1 = (bb & m1) << np.uint8(6) # Knight Moves Top by 1 Right by 2
    s2 = (bb & m2) << np.uint8(15) # Knight Moves Top by 2 Right by 1
    s3 = (bb & m3) << np.uint8(17) # Knight Moves Top by 2 Left by 1
    s4 = (bb & m4) << np.uint8(10) # Knight Moves Top by 1 Left by 2
    s5 = (bb & m4) >> np.uint8(6) # Knight Moves Bottom by 1 Right by 2
    s6 = (bb & m3) >> np.uint8(15) # Knight Moves Bottom by 2 Right by 1
    s7 = (bb & m2) >> np.uint8(17) # Knight Moves Bottom by 2 Left by 1
    s8 = (bb & m1) >> np.uint8(10) # Knight Moves Bottom by 1 Left by 2

    return s1 | s2 | s3 | s4 | s5 | s6 | s7 | s8


KNIGHT_MOVES = np.fromiter(
        (getKnightMovesFromSquareIndex(i) for i in range(64)),
        dtype=np.uint64,
        count=64)
# print(f"sq = {Square.getSquareFromString("g2").sqIdx} : Moves : {hex(compute_knight_moves(Square.getSquareFromString("g2").sqIdx))}")

# PAWN QUIETS
# NOTE: MUST BE CHECKED LATER FOR BLOCKERS IN EVENT OF DOUBLE ADVANCE

def getNoCapturePawnMovesFromSquareIndex(color: Color, i: int) -> np.uint64:
    """
    Computes the quiet pawn moves (i.e. moves that do not capture)
    from a given square index for a given color.

    This function takes into account the color of the pawn and
    whether it is on its starting rank, and returns a bitboard
    representing all possible quiet moves from the given square.
    """
    shift_forward = lambda bb, color, i:  \
        bb << np.uint(8*i) if color == Color.WHITE else bb >> np.uint8(8*i)
    starting_rank = RANKS[Rank.TWO] if color == Color.WHITE else RANKS[Rank.SEVEN]

    sq = Square(i)
    bb = sq.toBitBoard()

    s1 = shift_forward(bb, color, 1)
    s2 = shift_forward((bb & starting_rank), color, 2)

    return s1 | s2

PAWN_NO_CAPTURE = np.fromiter(
        (getNoCapturePawnMovesFromSquareIndex(color, i)
            for color in Color 
            for i in range(64)),
        dtype=np.uint64,
        count=2*64)
PAWN_NO_CAPTURE.shape = (2,64)

# PAWN ATTACKS

def getCapturePawnMovesFromSquareIndex(color: Color, i: int) -> np.uint64:
    """
    Computes the pawn's capture moves from a given square index for a given color.

    This function calculates the bitboard representing all possible capture moves 
    for a pawn located at a specific square index 'i'. It accounts for the color 
    of the pawn to determine the direction of attack, ensuring it does not move 
    off the edges of the board.

    Args:
        color (Color): The color of the pawn (WHITE or BLACK).
        i (int): The index of the square on the chessboard (0-63).

    Returns:
        np.uint64: A bitboard mask representing all possible capture moves for a 
        pawn from the given square index.
    """

    sq = Square(i)
    bb = sq.toBitBoard()

    if color == Color.WHITE:
        s1 = (bb & ~FILES[File.A]) << np.uint8(7)
        s2 = (bb & ~FILES[File.H]) << np.uint8(9)
    else:
        s1 = (bb & ~FILES[File.A]) >> np.uint8(9)
        s2 = (bb & ~FILES[File.H]) >> np.uint8(7)

    return s1 | s2

PAWN_CAPTURE = np.fromiter(
        (getCapturePawnMovesFromSquareIndex(color, i)
            for color in Color 
            for i in range(64)),
        dtype=np.uint64,
        count=2*64)
PAWN_CAPTURE.shape = (2,64)

# FIRST RANK MOVES
# Array is indexed by file of square and occupancy of line

def compute_first_rank_moves(i:int, occ:np.uint8) -> np.uint8:
    # i is square index from 0 to 8
    # occ is 8-bit number that represents occupancy of the rank 
    # Returns first rank moves (as uint8)

    """
    Computes the possible moves for a piece located on the first rank
    given a square index and rank occupancy.

    This function calculates attack rays to the left and right from a 
    specified square on the first rank, taking into account any pieces 
    blocking the path. It uses bit manipulation to efficiently determine 
    and return the legal moves as an 8-bit number.

    Args:
        i (int): The index of the square on the first rank (0 to 7).
        occ (np.uint8): An 8-bit number representing the occupancy of 
                        the rank, where each bit is a square on the rank.

    Returns:
        np.uint8: An 8-bit number representing the possible moves from 
                  the given square index on the first rank.
    """

    left_ray = lambda x: x - np.uint8(1) # Gets the Square to the left of x
    right_ray = lambda x: (~x) & ~(x - np.uint8(1)) # Gets the Square to the left of x

    x = np.uint8(1) << np.uint8(i)
    occ = np.uint8(occ)

    left_attacks = left_ray(x)
    left_blockers = left_attacks & occ
    if left_blockers != np.uint8(0):
        leftmost = np.uint8(1) << BitBoard.msbBitScan(np.uint64(left_blockers))
        left_garbage = left_ray(leftmost)
        left_attacks ^= left_garbage

    right_attacks = right_ray(x)
    right_blockers = right_attacks & occ
    if right_blockers != np.uint8(0):
        rightmost = np.uint8(1) << BitBoard.ls1bBitScan(np.uint64(right_blockers))
        right_garbage = right_ray(rightmost)
        right_attacks ^= right_garbage

    return left_attacks ^ right_attacks



FIRST_RANK_MOVES = np.fromiter(
        (compute_first_rank_moves(i, occ)
            for i in range(8) # 8 squares in a rank 
            for occ in range(256)), # 2^8 = 256 possible occupancies of a rank
        dtype=np.uint8,
        count=8*256)
FIRST_RANK_MOVES.shape = (8,256)

if __name__ == "__main__":
    # print(compute_king_moves(28))
    pass