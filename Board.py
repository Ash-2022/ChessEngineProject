import typing as tt
import numpy as np
class Board : 
    file = {"a" : 0 , "b" : 1 , "c" : 2 , "d" : 3 , "e" : 4 , "f" : 5 , "g" : 6 , "h" : 7}
    rank = {"1" : 0 , "2" : 1 , "3" : 2 , "4" : 3 , "5" : 4 , "6" : 5 , "7" : 6 , "8" : 7}
    def __init__(self) -> None:

        """
        
        To represent the board we typically need one bitboard for each piece-type and color -
        likely encapsulated inside a class or structure, or as an array of bitboards as part of a position object. 
        A one-bit inside a bitboard implies the existence of a piece of this piece-type on a certain square -
        one to one associated by the bit-position.
        Intuition for move generation : 
        1) Piece Capture : Use AND operation with bitboards
        """
        self.WHITE_PAWN_bitboard = self.createEmptyBitboard()
        self.WHITE_ROOK_bitboard = self.createEmptyBitboard()
        self.WHITE_KNIGHT_bitboard = self.createEmptyBitboard()
        self.WHITE_BISHOP_bitboard = self.createEmptyBitboard()
        self.WHITE_QUEEN_bitboard = self.createEmptyBitboard()
        self.WHITE_KING_bitboard = self.createEmptyBitboard()
        self.BLACK_PAWN_bitboard = self.createEmptyBitboard()
        self.BLACK_ROOK_bitboard = self.createEmptyBitboard()
        self.BLACK_KNIGHT_bitboard = self.createEmptyBitboard()
        self.BLACK_BISHOP_bitboard = self.createEmptyBitboard()
        self.BLACK_QUEEN_bitboard = self.createEmptyBitboard()
        self.BLACK_KING_bitboard = self.createEmptyBitboard()
        self.initStartPosition()
        self.occupiedBitBoards = np.vstack((
            self.WHITE_ROOK_bitboard,
            self.WHITE_KNIGHT_bitboard,
            self.WHITE_BISHOP_bitboard,
            self.WHITE_QUEEN_bitboard,
            self.WHITE_KING_bitboard,
            self.WHITE_PAWN_bitboard,
            self.BLACK_ROOK_bitboard,
            self.BLACK_KNIGHT_bitboard,
            self.BLACK_BISHOP_bitboard,
            self.BLACK_QUEEN_bitboard,
            self.BLACK_KING_bitboard,
            self.BLACK_PAWN_bitboard
        ))
        self.updateOccupiedBoard()

    @staticmethod # Method Not tied to the class
    def renderBoard(bitBoard: np.ndarray) -> str:
        val = ""
        for i , square in enumerate(bitBoard) : 
            if not i % 8 : 
                val += "\n"
            if square :
                val += " X "
                continue
            val += " - "
        return val
    def updateOccupiedBoard(self) -> np.ndarray[np.byte]:
        result = np.zeros(64 , dtype=np.byte)
        for board in self.occupiedBitBoards : 
            result = np.bitwise_or(result , board , dtype=np.byte)
        self.occupiedBitBoards = result
    def getEmptyBitBoard(self) -> np.ndarray[np.byte]: 
        # print(self.occupiedBitBoards)
        return 1 - self.occupiedBitBoards # Bitwise NOT in numpy
    def createEmptyBitboard(self) -> tt.List[int]:
        return np.zeros(64 , dtype=np.uint64)
    def setBitboard(self , bitboard: tt.List[int] , position: tt.List[int]) -> None:
        for square in position : 
            bitboard[square] = 1
    def initStartPosition(self) -> None:
        self.setBitboard(self.WHITE_PAWN_bitboard , [self.getSquareFromText(i) for i in ["a2" , "b2" , "c2" , "d2" ,"e2" ,"f2" ,"g2" ,"h2"]])
        self.setBitboard(self.WHITE_ROOK_bitboard , [self.getSquareFromText(i) for i in ["a1" , "h1"]])
        self.setBitboard(self.WHITE_KNIGHT_bitboard , [self.getSquareFromText(i) for i in ["b1" , "g1"]])
        self.setBitboard(self.WHITE_BISHOP_bitboard , [self.getSquareFromText(i) for i in ["c1" , "f1"]])
        self.setBitboard(self.WHITE_QUEEN_bitboard , [self.getSquareFromText("d1")])
        self.setBitboard(self.WHITE_KING_bitboard , [self.getSquareFromText("e1")])
        self.setBitboard(self.BLACK_PAWN_bitboard , [self.getSquareFromText(i) for i in ["a7" , "b7" , "c7" , "d7" ,"e7" ,"f7" ,"g7" ,"h7"]])
        self.setBitboard(self.BLACK_ROOK_bitboard , [self.getSquareFromText(i) for i in ["a8" , "h8"]])
        self.setBitboard(self.BLACK_KNIGHT_bitboard , [self.getSquareFromText(i) for i in ["b8" , "g8"]])
        self.setBitboard(self.BLACK_BISHOP_bitboard , [self.getSquareFromText(i) for i in ["c8" , "f8"]])
        self.setBitboard(self.BLACK_QUEEN_bitboard , [self.getSquareFromText("d8")])
        self.setBitboard(self.BLACK_KING_bitboard , [self.getSquareFromText("e8")])
   


if __name__ == "__main__":
    board = Board()
    print(board.renderBoard(board.occupiedBitBoards)) 
    print(board.renderBoard(board.getEmptyBitBoard())) 