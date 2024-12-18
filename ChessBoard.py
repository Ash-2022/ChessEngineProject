import numpy as np
import typing as tt
from Square import Square
from Constants import Rank , File , Color , PieceType
from BitBoard import *
from enum import IntEnum
from Move import Move

class ChessBoard : 
    def __init__(self) -> None:
        self.pieces = np.zeros((2 , 6) , dtype=np.uint64) # 2 colors , 6 pieces
        self.combinedColors = np.zeros(2 , dtype=np.uint64)
        self.board = np.uint64(0)
        self.color = Color.WHITE
    
    def  __str__(self):
        """
        Returns a string representation of the chess board.

        This method constructs a visual representation of the board
        where each square is represented by a character corresponding
        to the piece on that square. Uppercase letters represent white
        pieces and lowercase letters represent black pieces. Empty squares
        are represented by a period ('.'). The board is rendered in a grid
        format with ranks displayed from top to bottom and files from left 
        to right. The current player's turn is appended as additional information.

        Returns:
            str: A string representation of the board and the current player's turn.
        """
        board_str = []
        for r in reversed(Rank):
            for f in File:
                sq = Square.getSquareFromRankAndFileEnum(r, f)
                white_piece = self.pieceOnSquare(sq, Color.WHITE)
                black_piece = self.pieceOnSquare(sq, Color.BLACK)
                if white_piece is not None:
                    board_str.append(" "+ white_piece.upper() + " ")
                elif black_piece is not None:
                    board_str.append(" " + black_piece.lower() + " ")
                else:
                    board_str.append(' . ')
            board_str.append('\n')
        board_str = ''.join(board_str)
        info_str = "%s to move" % self.color.name
        return "%s%s" % (board_str, info_str)
    def getPieceBB(self, piece : PieceType, color: tt.Optional[Color] = None) -> np.uint64:
        # NOTE: Defaults to current color
        """
        Returns the bitboard for the given piece of the given color, or the current color if None is given.

        :param piece: The piece to get the bitboard for.
        :param color: The color of the piece, or None to default to the current color.
        :return: The bitboard for the given piece of the given color.
        """
        if color is None:
            color = self.color
        return self.pieces[color][piece]
    def pieceOnSquare(self, sq : Square, color: tt.Optional[Color] = None ) -> tt.Iterable[str]:
        # NOTE: Defaults to current color
        """
        Returns the piece on the given square of the given color, or None if empty.
        Defaults to current color if color is None.
        :param sq: The square to check.
        :param color: The color to check, or None to default to the current color.
        :return: The piece on the given square of the given color, or None if empty.
        """
        if color is None:
            color = self.color
        return next(
            (p.humanReadable() for p in PieceType if 
                isSet(self.getPieceBB(p, color), sq)),
            None)

    def setPieceOnSquare(self, sq: Square, piece: PieceType, color: tt.Optional[Color] = None) -> None:
        # NOTE: Defaults to current color
        """
        Sets the specified piece on the given square for the given color.

        This method updates the bitboards to place a piece of a specified type and color
        on a given square of the chessboard. If no color is specified, it defaults to the
        current color. The function modifies the bitboard representation of the individual
        piece, the combined color representation, and the overall board representation.

        Args:
            sq (Square): The square where the piece is to be placed.
            piece (PieceType): The type of the piece to place.
            color (Color, optional): The color of the piece. Defaults to the current color.

        Returns:
            None
        """

        if color is None:
            color = self.color
        pieceBB = self.getPieceBB(piece, color)
        colorBB = self.combinedColors[color]
        boardBB= self.board

        self.pieces[color][piece] = setSquareOnBB(pieceBB, sq)
        self.combinedColors[color] = setSquareOnBB(colorBB, sq)
        self.board = setSquareOnBB(boardBB, sq)

    def clearSquare(self, sq: Square, color: tt.Optional[Color] = None):
        # NOTE: Defaults to current color
        """
        Clears the specified square of the given color.

        This method updates the bitboards to remove any piece from a given square of the chessboard.
        If no color is specified, it defaults to the current color. The function modifies the bitboard
        representation of the individual piece, the combined color representation, and the overall board
        representation.

        Args:
            sq (Square): The square to clear.
            color (Color, optional): The color of the piece to clear. Defaults to the current color.

        Returns:
            None
        """

        if color is None:
            color = self.color

        piece = self.pieceOnSquare(sq, color)
        if piece is None:
            return

        pieceBB = self.getPieceBB(piece, color)
        colorBB = self.combinedColors[color]
        boardBB = self.board

        self.pieces[color][piece] = clearSquareOnBB(pieceBB, sq)
        self.combinedColors[color] = clearSquareOnBB(colorBB, sq)
        self.board = clearSquareOnBB(boardBB, sq)
    def apply_move(self, move: Move) -> object:
        """
        Applies move to chess board
        Returns a new board, doesn't modify original
        """
        new_board = ChessBoard()
        new_board.pieces = np.copy(self.pieces)
        new_board.combinedColors = np.copy(self.combinedColors)
        new_board.board = np.copy(self.board)
        new_board.color = self.color

        piece = self.pieceOnSquare(move.src)
        new_board.clearSquare(move.src)
        new_board.clearSquare(move.dest, ~new_board.color) # in event of a capture
        new_board.setPieceOnSquare(move.dest, piece if move.promo is None else move.promo)
        
        new_board.color = ~new_board.color
        return new_board
    def init_game(self):
        # 2 nibbles for 1 file/rank in hex notations 
        # White Piece Setup
        self.pieces[Color.WHITE][PieceType.PAWN] = np.uint64(0x000000000000FF00)
        self.pieces[Color.WHITE][PieceType.KNIGHT] = np.uint64(0x0000000000000042)
        self.pieces[Color.WHITE][PieceType.BISHOP] = np.uint64(0x0000000000000024)
        self.pieces[Color.WHITE][PieceType.ROOK] = np.uint64(0x0000000000000081)
        self.pieces[Color.WHITE][PieceType.QUEEN] = np.uint64(0x0000000000000008)
        self.pieces[Color.WHITE][PieceType.KING] = np.uint64(0x0000000000000010) 
        # 0x10 = e1 , 0x08 = d1()

        # Black Piece Setup
        self.pieces[Color.BLACK][PieceType.PAWN] = np.uint64(0x00FF000000000000)
        self.pieces[Color.BLACK][PieceType.KNIGHT] = np.uint64(0x4200000000000000)
        self.pieces[Color.BLACK][PieceType.BISHOP] = np.uint64(0x2400000000000000)
        self.pieces[Color.BLACK][PieceType.ROOK] = np.uint64(0x8100000000000000)
        self.pieces[Color.BLACK][PieceType.QUEEN] = np.uint64(0x0800000000000000)
        self.pieces[Color.BLACK][PieceType.KING] = np.uint64(0x1000000000000000)

        for p in PieceType:
            for c in Color:
                self.combinedColors[c] |= self.pieces[c][p]

        self.board = self.combinedColors[Color.WHITE] | self.combinedColors[Color.BLACK]

if __name__ == "__main__":
    cb = ChessBoard()
    cb.init_game()
    print(cb)