from PyQt5.QtCore import QThread
from modules.engine.core import Engine


class SpaceCreationThread(QThread):
    def __init__(self, engine, dimensions, save_path):
        """
        Инициализация потока для создания нового пространства.
        :param engine: Экземпляр движка.
        :param dimensions: Размеры пространства (например, (10, 10, 10)).
        :param save_path: Путь для сохранения состояния.
        """
        super().__init__()
        self.engine = engine
        self.dimensions = dimensions
        self.save_path = save_path

    def run(self):
        """
        Основной метод потока.
        Создает новое пространство и сохраняет его состояние.
        """
        self.engine.initialize_empty_space(dimensions=self.dimensions)
        self.engine.save_space(self.save_path)


def create_new_space(main_window):
    """
    Создает новое пространство, сохраняет его состояние и отображает его.
    :param main_window: Экземпляр MainWindow.
    """
    engine = Engine()
    save_path = "saves/new_space.json"

    # Создаем поток для долгих операций
    thread = SpaceCreationThread(engine, dimensions=(10, 10, 10), save_path=save_path)

    # Подключаем обработчик завершения потока
    thread.finished.connect(lambda: on_space_created(main_window, engine.get_space()))

    # Запускаем поток
    thread.start()


def on_space_created(main_window, space_data):
    """
    Вызывается после завершения создания пространства.
    :param main_window: Экземпляр MainWindow.
    :param space_data: Данные созданного пространства.
    """
    print("Новое пространство создано.")

    # Удаляем старый виджет
    old_widget = main_window.centralWidget()
    if old_widget:
        old_widget.deleteLater()

    # Заменяем главное меню на OpenGL-виджет
    from modules.engine.render import Renderer  # Импортируем Renderer
    renderer = Renderer(space_data)
    main_window.setCentralWidget(renderer)

    # Добавляем верхнее меню
    main_window.setup_main_menu()

    print("Пространство отображено.")