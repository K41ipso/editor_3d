from PyQt5.QtWidgets import QApplication

def exit_application():
    """
    Завершает работу приложения.
    """
    print("Завершение работы приложения.")
    QApplication.quit()