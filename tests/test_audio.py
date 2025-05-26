import os
import unittest
from typing import Any
from unittest.mock import patch

from modules.audio import play_background_music, play_sound_effect


class TestAudio(unittest.TestCase):
    @patch("pygame.mixer.music")
    def test_play_background_music(self, MockMusic: Any) -> None:
        """Проверка воспроизведения фоновой музыки."""
        music_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../resources/sounds/menu_music_e1m1.mp3"))
        play_background_music(music_path, volume=0.5)
        MockMusic.load.assert_called_with(music_path)
        MockMusic.set_volume.assert_called_with(0.5)
        MockMusic.play.assert_called()

    @patch("pygame.mixer.Sound")
    def test_play_sound_effect(self, MockSound: Any) -> None:
        """Проверка воспроизведения звукового эффекта."""
        sound_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../resources/sounds/pm_button_click.mp3"))
        play_sound_effect(sound_path)
        MockSound.assert_called_with(sound_path)
        MockSound.return_value.play.assert_called()


if __name__ == "__main__":
    unittest.main()
