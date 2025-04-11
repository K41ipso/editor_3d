from PyQt5.QtWidgets import QMenuBar, QAction


def setup_main_menu(window):
    """Настройка главного меню."""
    print("Настройка главного меню...")

    menu_bar = QMenuBar(window)
    window.setMenuBar(menu_bar)

    # Меню "File"
    file_menu = menu_bar.addMenu("File")

    save_action = QAction("Save", window)
    load_action = QAction("Load", window)
    exit_action = QAction("Exit", window)
    exit_action.triggered.connect(window.close)

    file_menu.addAction(save_action)
    file_menu.addAction(load_action)
    file_menu.addSeparator()
    file_menu.addAction(exit_action)