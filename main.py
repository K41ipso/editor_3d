import sys

from PyQt5.QtWidgets import QApplication

from modules.menu import MainWindow


def main() -> None:
    # Создание приложения PyQt5
    app = QApplication(sys.argv)

    # Создание главного окна
    window = MainWindow()
    window.show()

    # Запуск основного цикла
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
