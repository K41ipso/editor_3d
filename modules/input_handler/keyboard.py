class KeyboardHandler:
    def __init__(self, main_window=None):
        self.key_bindings = {}  # Словарь для хранения привязок клавиш к действиям
        self.position = [0, 0, 0]  # Текущие координаты (x, y, z)
        self.last_position = [0, 0, 0]  # Последние известные координаты
        self.speed = 0.1  # Скорость перемещения
        self.opengl_widget = None  # Ссылка на OpenGL-виджет
        self.main_window = main_window  # Ссылка на MainWindow

    def bind_key(self, key, action):
        """Привязывает клавишу к действию."""
        self.key_bindings[key] = action

    def handle_key_press(self, key):
        """Обрабатывает нажатие клавиши."""
        if key in self.key_bindings:
            self.key_bindings[key]()
            print(f"Текущая позиция: {self.position}")
            if self.opengl_widget and self.position != self.last_position:
                self.main_window.update_opengl_widget()  # Вызов метода перерисовки из MainWindow
                self.last_position = self.position[:]  # Обновляем последние известные координаты
            else:
                print("OpenGL Widget не установлен или позиция не изменилась.")
        else:
            print(f"Клавиша '{key}' не привязана ни к какому действию.")

    def move_forward(self):
        """Перемещение вперёд (по оси Z)."""
        if self.position[2] + self.speed <= 30:
            self.position[2] += self.speed

    def move_backward(self):
        """Перемещение назад (по оси Z)."""
        if self.position[2] - self.speed >= -30:
            self.position[2] -= self.speed

    def move_left(self):
        """Перемещение влево (по оси X)."""
        if self.position[0] + self.speed <= 30:
            self.position[0] += self.speed

    def move_right(self):
        """Перемещение вправо (по оси X)."""
        if self.position[0] - self.speed >= -30:
            self.position[0] -= self.speed

    def move_up(self):
        """Перемещение вверх (по оси Y)."""
        if self.position[1] + self.speed <= 10:
            self.position[1] += self.speed

    def move_down(self):
        """Перемещение вниз (по оси Y)."""
        if self.position[1] - self.speed >= -10:
            self.position[1] -= self.speed

    def set_opengl_widget(self, widget):
        """Устанавливает ссылку на OpenGL-виджет."""
        self.opengl_widget = widget
