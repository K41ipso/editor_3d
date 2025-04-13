import pygame


def play_background_music(music_path, volume=1.0):
    """
    Воспроизведение фоновой музыки.
    :param music_path: Путь к файлу с музыкой.
    :param volume: Громкость (от 0.0 до 1.0).
    """
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.set_volume(volume)  # Установка громкости
        pygame.mixer.music.play(-1)  # Бесконечное воспроизведение
        print(f"Фоновая музыка успешно загружена: {music_path}, громкость: {volume * 100}%")
    except Exception as e:
        print(f"Ошибка при воспроизведении фоновой музыки: {e}")


def play_sound_effect(sound_path):
    """Воспроизведение звукового эффекта."""
    try:
        sound = pygame.mixer.Sound(sound_path)  # Загрузка звукового эффекта
        sound.play()  # Воспроизведение звука
        print(f"Звуковой эффект успешно загружен: {sound_path}")
    except Exception as e:
        print(f"Ошибка при воспроизведении звукового эффекта: {e}")