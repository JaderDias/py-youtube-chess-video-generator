from ScriptedShot import ScriptedShot
import ChessScript
import io
import unittest

PGN_SAMPLE = '''
[Event "34th Leon GM 2021"]
[Site "chess.com INT"]
[Date "2021.06.30"]
[Round "1.1"]
[White "Dominguez Perez, Leinier"]
[Black "Ju, Wenjun"]
[Result "1-0"]
[WhiteTitle "GM"]
[BlackTitle "GM"]
[WhiteElo "2758"]
[BlackElo "2560"]
[ECO "C42"]
[Opening "Petrov"]
[Variation "Nimzovich attack"]
[WhiteFideId "3503240"]
[BlackFideId "8603006"]
[EventDate "2021.06.30"]

1. e4 e5 2. Nf3 Nf6 3. Nxe5 d6 4. Nf3 Nxe4 5. Nc3 Nxc3 6. dxc3 Be7 7. Be3 O-O 8.
Qd2 Nd7 9. O-O-O Nf6 10. Bd3 c5 11. a3 d5 12. c4 dxc4 13. Bxc4 Qxd2+ 14. Rxd2 b6
15. Re1 a6 16. Bf4 b5 17. Ba2 Ra7 18. Ne5 Nh5 19. Nc6 Nxf4 20. Nxa7 Bg5 21. Nxc8
Rxc8 22. g3 Ng6 23. f4 Nxf4 24. gxf4 Bxf4 25. Rf1 Bxd2+ 26. Kxd2 Rc7 27. a4 Kf8
28. Rf5 f6 29. b4 cxb4 30. axb5 axb5 31. Rxb5 Rc3 32. Rxb4 Rh3 33. Rb8+ Ke7 34.
Rb7+ Kd6 35. Rxg7 Rxh2+ 36. Kd3 h5 37. Bb3 h4 38. Ke4 Rh1 39. Rf7 Rf1 40. Rh7
Rh1 41. Rh6 Ke7 42. Kf3 Rf1+ 43. Kg2 Rf4 44. Kh3 1-0
'''

class TestChessScript(unittest.TestCase):
    def test_get_title(self):
        # Arrange
        expected = "Dominguez Perez, Leinier vs Ju, Wenjun on 2021.06.30 round 1.1"
        handle = io.StringIO(PGN_SAMPLE)
        chess_script = ChessScript.ChessScript(handle)

        # Act
        actual =  chess_script.get_title()

        # Assert
        self.assertEqual(actual, expected)
    def test_get_text(self):
        # Arrange
        expected = "pawn to e4"
        handle = io.StringIO(PGN_SAMPLE)
        chess_script = ChessScript.ChessScript(handle)
        chess_script.__next__()

        # Act
        actual =  chess_script.get_text()

        # Assert
        self.assertEqual(actual, expected)
    def test_get_image(self):
        # Arrange
        expected_content = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x048'
        expected_filename = '/tmp/b29f9029eaa90ad34dacec7f0886418edf966dc947d9ea0e04755f742e80130b.png'
        handle = io.StringIO(PGN_SAMPLE)
        chess_script = ChessScript.ChessScript(handle)
        chess_script.__next__()

        # Act
        actual_filename =  chess_script.get_image()

        # Assert
        self.assertEqual(actual_filename, expected_filename)
        with open(actual_filename, 'rb') as file:
            actual_content = file.read()
            self.assertEqual(actual_content[0:20], expected_content)
    def test_get_script(self):
        # Arrange
        expected = [
            ScriptedShot(
                text="pawn to e4",
                image_filename='/tmp/b29f9029eaa90ad34dacec7f0886418edf966dc947d9ea0e04755f742e80130b.png'
            ),
            ScriptedShot(
                text="pawn to e5",
                image_filename='/tmp/fc8def2c71daccbe3cece7072e2c4b50dfb258340e971ab656784db46d1cf0be.png'
            ),
        ]
        handle = io.StringIO(PGN_SAMPLE)
        chess_script = ChessScript.ChessScript(handle)
        i = 0

        # Act
        for actual in chess_script:
            # Assert
            self.assertEqual(actual.text, expected[i].text)
            self.assertEqual(actual.image_filename, expected[i].image_filename)
            i += 1
            if i == 2:
                break