class KeyboardHandler:
    def __init__(self):
        self.key_bindings = {}  # Словарь для хранения привязок клавиш к действиям
        self.position = [0, 0, 0]  # Текущие координаты (x, y, z)
        self.speed = 1  # Скорость перемещения
        self.opengl_widget = None  # Ссылка на OpenGL-виджет
        self.last_position = [0, 0, 0]  # Последние известные координаты

    def bind_key(self, key, action):
        """Привязывает клавишу к действию."""
        self.key_bindings[key] = action

    def handle_key_press(self, key):
        """Обрабатывает нажатие клавиши."""
        if key in self.key_bindings:
            self.key_bindings[key]()
            print(f"Текущая позиция: {self.position}")
            if self.opengl_widget and self.position != self.last_position:
                self.opengl_widget.update()  # Перерисовываем виджет, если координаты изменились
                self.last_position = self.position[:]  # Обновляем последние известные координаты
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
