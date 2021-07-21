import os
import unittest

from Video import to_video

from tests.MockScript import MockScript
from tests.MockShot import MockShot


class TestScriptedShot(unittest.TestCase):
    def test_video(self):
        # Arrange
        expected_filename = '/tmp/82e3803dde1eed6ffa5320f9b01e22aea585fa6f4a902e1451de315eeaf92fef.mp4'
        __location__ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))
        sample_wav_file = os.path.join(__location__, 'sample.wav')
        sample_png_file = os.path.join(__location__, 'sample.png')
        script = MockScript(
            [
                MockShot(
                   sample_wav_file,
                   sample_png_file,
                ),
                MockShot(
                   sample_wav_file,
                   sample_png_file,
                ),
            ]
        )

        # Act
        actual_filename = to_video(script)

        # Assert
        self.assertEqual(actual_filename, expected_filename)
