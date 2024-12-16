import typing as tt
import numpy as np
class Board : 
    rank = {"a" : 0 , "b" : 1 , "c" : 2 , "d" : 3 , "e" : 4 , "f" : 5 , "g" : 6 , "h" : 7}
    file = {"1" : 0 , "2" : 1 , "3" : 2 , "4" : 3 , "5" : 4 , "6" : 5 , "7" : 6 , "8" : 7}
    def __init__(self) -> None:
        """
        Initialize the board
        Board = [
            [h1 , h2 , h3 , h4 , h5 , h6 , h7 , h8],
            [g1 , g2 , g3 , g4 , g5 , g6 , g7 , g8],
            [f1 , f2 , f3 , f4 , f5 , f6 , f7 , f8],
            [e1 , e2 , e3 , e4 , e5 , e6 , e7 , e8],
            [d1 , d2 , d3 , d4 , d5 , d6 , d7 , d8],        
            [c1 , c2 , c3 , c4 , c5 , c6 , c7 , c8],
            [b1 , b2 , b3 , b4 , b5 , b6 , b7 , b8],
            [a1 , a2 , a3 , a4 , a5 , a6 , a7 , a8]
        ]
        Keep a1 = 0 and b1 = 8 so on till h8 = 63 , i.e Square = 8*rank + file , both are 0-indexed
        To represent the board we typically need one bitboard for each piece-type and color -
        likely encapsulated inside a class or structure, or as an array of bitboards as part of a position object. 
        A one-bit inside a bitboard implies the existence of a piece of this piece-type on a certain square -
        one to one associated by the bit-position.
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
        self.allBitBoards = np.vstack((
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
        self.updateBoard()

    def renderBoard(self) -> str:
        val = ""
        for i , sqauare in enumerate(self.allBitBoards) : 
            if not i % 8 : 
                val += "\n"
            if sqauare :
                val += " X "
                continue
            val += " - "
        return val
    def updateBoard(self) -> np.ndarray[np.byte]:
        result = np.zeros(64 , dtype=np.byte)
        for board in self.allBitBoards : 
            result = np.bitwise_or(result , board , dtype=np.byte)
        self.allBitBoards = result
    def createEmptyBitboard(self) -> tt.List[int]:
        return np.zeros(64 , dtype=np.byte)
    def setBitboard(self , bitboard: tt.List[int] , position: tt.List[int]) -> None:
        for square in position : 
            bitboard[square] = 1
    def initStartPosition(self) -> None:
        self.setBitboard(self.WHITE_PAWN_bitboard , [self.getSquareFromText(i) for i in ["b1" , "b2" , "b3" , "b4" ,"b5" ,"b6" ,"b7" ,"b8"]])
        self.setBitboard(self.WHITE_ROOK_bitboard , [self.getSquareFromText(i) for i in ["a1" , "a8"]])
        self.setBitboard(self.WHITE_KNIGHT_bitboard , [self.getSquareFromText(i) for i in ["a2" , "a7"]])
        self.setBitboard(self.WHITE_BISHOP_bitboard , [self.getSquareFromText(i) for i in ["a3" , "a6"]])
        self.setBitboard(self.WHITE_QUEEN_bitboard , [self.getSquareFromText("a4")])
        self.setBitboard(self.WHITE_KING_bitboard , [self.getSquareFromText("a5")])
        self.setBitboard(self.BLACK_PAWN_bitboard , [self.getSquareFromText(i) for i in ["g1" , "g2" , "g3" , "g4" ,"g5" ,"g6" ,"g7" ,"g8"]])
        self.setBitboard(self.BLACK_ROOK_bitboard , [self.getSquareFromText(i) for i in ["h1" , "h8"]])
        self.setBitboard(self.BLACK_KNIGHT_bitboard , [self.getSquareFromText(i) for i in ["h2" , "h7"]])
        self.setBitboard(self.BLACK_BISHOP_bitboard , [self.getSquareFromText(i) for i in ["h3" , "h6"]])
        self.setBitboard(self.BLACK_QUEEN_bitboard , [self.getSquareFromText("h4")])
        self.setBitboard(self.BLACK_KING_bitboard , [self.getSquareFromText("h5")])
    @classmethod
    def getSquareFromText(self , squareInText: str) -> int:
        return 8 * Board.rank[squareInText[0]] + Board.file[squareInText[1]]
    @classmethod
    def getSquareFromNumber(self , squareInNumber: int) -> str:
        return chr((squareInNumber // 8) + ord("a")) + str(squareInNumber % 8 + 1)


if __name__ == "__main__":
    board = Board()
    print(board.renderBoard())