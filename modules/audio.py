import os

import pygame.mixer


def play_background_music(music_path: str, volume: float = 1.0) -> None:
    """
    Воспроизведение фоновой музыки.
    :param music_path: Путь к файлу с музыкой.
    :param volume: Громкость (от 0.0 до 1.0).
    """
    try:
        # Инициализация только модуля mixer
        if not pygame.mixer.get_init():
            pygame.mixer.init()

        # Формируем абсолютный путь к файлу
        abs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../resources/sounds", music_path))

        # Проверяем существование файла
        if not os.path.exists(abs_path):
            raise FileNotFoundError(f"Файл музыки не найден по пути {abs_path}")

        # Загружаем и воспроизводим музыку
        pygame.mixer.music.load(abs_path)  # type: ignore[attr-defined]
        # Установка громкости
        pygame.mixer.music.set_volume(volume)  # type: ignore[attr-defined]
        # Бесконечное воспроизведение
        pygame.mixer.music.play(-1)  # type: ignore[attr-defined]
        print(f"Фоновая музыка успешно загружена: {abs_path}, громкость: {volume * 100}%")
    except FileNotFoundError as e:
        print(f"Ошибка: {e}")
    except Exception as e:
        print(f"Неожиданная ошибка при воспроизведении фоновой музыки: {e}")


def play_sound_effect(sound_path: str) -> None:
    """
    Воспроизведение звукового эффекта.
    :param sound_path: Путь к звуковому файлу.
    """
    try:
        # Инициализация только модуля mixer
        if not pygame.mixer.get_init():
            pygame.mixer.init()

        # Формируем абсолютный путь к файлу
        abs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../resources/sounds", sound_path))

        # Проверяем существование файла
        if not os.path.exists(abs_path):
            raise FileNotFoundError(f"Звуковой файл не найден по пути {abs_path}")

        # Загружаем и воспроизводим звук
        sound = pygame.mixer.Sound(abs_path)
        sound.play()
        print(f"Звуковой эффект успешно загружен: {abs_path}")
    except FileNotFoundError as e:
        print(f"Ошибка: {e}")
    except Exception as e:
        print(f"Неожиданная ошибка при воспроизведении звука: {e}")
