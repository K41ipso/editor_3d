import pygame


def play_background_music(music_path):
    """Воспроизведение фоновой музыки."""
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play(-1)  # Бесконечное воспроизведение
        print(f"Музыка успешно загружена: {music_path}")
    except Exception as e:
        print(f"Ошибка при воспроизведении музыки: {e}")