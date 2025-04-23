import sys
from PyQt5.QtWidgets import QApplication
from modules.menu import MainWindow
#from modules.audio import play_background_music
#import os


def main():
    # Создание приложения PyQt5
    app = QApplication(sys.argv)

    # Загрузка фоновой музыки с громкостью 30%
    #music_path = os.path.join(os.path.dirname(__file__), "resources/sounds/menu_music_e1m1.mp3")
    #play_background_music(music_path, volume=0.3)  # Громкость 30%

    # Создание главного окна
    window = MainWindow()
    window.show()

    # Запуск основного цикла
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()