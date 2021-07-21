import hashlib

import chess
import chess.pgn
from cairosvg import svg2png

from ScriptedShot import ScriptedShot


class ChessScript:
    def __init__(self, pgn):
        self.game = chess.pgn.read_game(pgn)
    def get_title(self):
        headers = self.game.headers
        return "{0} vs {1} on {2} round {3}".format(
            headers["White"],
            headers["Black"],
            headers["Date"],
            headers["Round"]
        )
    def get_text(self):
        move = self.game.move
        piece_type = self.previous_position.piece_type_at(move.from_square)
        piece_name = chess.piece_name(piece_type)
        to_square_name = chess.SQUARE_NAMES[move.to_square]
        return '{0} to {1}'.format(piece_name, to_square_name)
    def get_image(self):
        boardsvg = chess.svg.board(
            board=self.game.board(),
            size=1080,
            lastmove=self.game.move
        )
        hash_object = hashlib.sha256(boardsvg.encode('utf-8'))
        filename = "/tmp/{0}.png".format(hash_object.hexdigest())
        svg2png(bytestring=boardsvg,write_to=filename)
        return filename
    def __iter__(self):
        return self
    def __next__(self):
        if self.game.is_end():
            raise StopIteration
        self.previous_position = self.game.board()
        self.game = self.game.next()
        return ScriptedShot(
            text=self.get_text(),
            image_filename=self.get_image(),
        )
