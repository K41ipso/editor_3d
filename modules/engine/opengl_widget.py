from typing import Any, Tuple
from OpenGL.GL import (
    GL_COLOR_BUFFER_BIT,
    GL_DEPTH_BUFFER_BIT,
    GL_DEPTH_TEST,
    GL_MODELVIEW,
    GL_PROJECTION,
    GL_TRIANGLES,
    GL_LINES,
    glBegin,
    glClear,
    glClearColor,
    glColor3f,
    glEnable,
    glEnd,
    glLoadIdentity,
    glMatrixMode,
    glTranslatef,
    glVertex3f,
    glViewport,
    glRotatef
)
from OpenGL.GLU import gluPerspective
from PyQt5.QtWidgets import QOpenGLWidget
from PyQt5.QtCore import Qt


class OpenGLWidget(QOpenGLWidget):
    def __init__(
        self,
        space_data: Any = None,
        parent: Any = None,
        keyboard_handler: Any = None,
        rotation_x: float = 0.0,
        rotation_y: float = 0.0,
        rotation_z: float = 0.0,
        last_mouse_pos: Any = None,
        mouse_pressed: bool = False
    ) -> None:
        super().__init__(parent)
        self.space_data = space_data
        self.rotation_x = rotation_x
        self.rotation_y = rotation_y
        self.rotation_z = rotation_z
        self.last_mouse_pos = last_mouse_pos
        self.keyboard_handler = keyboard_handler
        self.mouse_pressed = mouse_pressed

    def initializeGL(self) -> None:
        glClearColor(0.1, 0.1, 0.1, 1.0)
        glEnable(GL_DEPTH_TEST)

    def resizeGL(self, width: int, height: int) -> None:
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, width / height, 0.1, 50.0)
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self) -> None:
        #print(f"Отрисовка: {self.space_data}")

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        if self.keyboard_handler:
            x, y, z = self.keyboard_handler.position
            glTranslatef(x, y, z - 5.0)
        else:
            glTranslatef(0.0, 0.0, -5.0)

        glRotatef(self.rotation_x, 1, 0, 0)
        glRotatef(self.rotation_y, 0, 1, 0)
        glRotatef(self.rotation_z, 0, 0, 1)

        self.draw_coordinate_grid()
        self.draw_plane()

        print("Пространство обновлено")

    def draw_coordinate_grid(self) -> None:
        # Рисуем серую сетку по осям X и Y
        glColor3f(0.5, 0.5, 0.5)  # Устанавливаем серый цвет для линий сетки
        glBegin(GL_LINES)  # Начинаем определение линий
        grid_size = 100  # Размер сетки
        step = 1  # Шаг между линиями

        for i in range(-grid_size, grid_size + 1, step):
            # Линии по оси X
            glVertex3f(i, -grid_size, 0)  # Начало линии
            glVertex3f(i, grid_size, 0)  # Конец линии

            # Линии по оси Y
            glVertex3f(-grid_size, i, 0)  # Начало линии
            glVertex3f(grid_size, i, 0)  # Конец линии

        glEnd()  # Завершаем определение линий

        # Рисуем координатные оси X, Y, Z с цветовым выделением
        axis_length = 100  # Длина осей
        glBegin(GL_LINES)

        # Ось X (красная)
        glColor3f(1.0, 0.0, 0.0)  # Красный цвет
        glVertex3f(0, 0, 0)  # Начало оси X
        glVertex3f(axis_length, 0, 0)  # Конец оси X

        # Ось Y (зеленая)
        glColor3f(0.0, 1.0, 0.0)  # Зеленый цвет
        glVertex3f(0, 0, 0)  # Начало оси Y
        glVertex3f(0, axis_length, 0)  # Конец оси Y

        # Ось Z (синяя)
        glColor3f(0.0, 0.0, 1.0)  # Синий цвет
        glVertex3f(0, 0, 0)  # Начало оси Z
        glVertex3f(0, 0, axis_length)  # Конец оси Z

        glEnd()  # Завершаем определение линий

    def data_space_reload(self, our_data: Any) -> None:
        self.space_data = our_data
        self.update()

    def draw_plane(self) -> None:
        print("Начало отрисовки плоскости")
        if not self.space_data or "plane" not in self.space_data:
            print("Нет данных для отрисовки плоскостей.")
            return
        try:
            for plane_id, plane_data in self.space_data["plane"].items():
                points = plane_data["points"]
                color = plane_data["color"]

                if len(points) < 3:
                    print(f"Недостаточно точек для отрисовки плоскости {plane_id}.")
                    continue

                # Установка цвета и начало рисования
                glBegin(GL_TRIANGLES)
                glColor3f(*color)

                for point in points:
                    glVertex3f(*point)

                glEnd()

                print(f"Плоскость {plane_id} успешно нарисована.")
        except TypeError as e:
            print(f"Ошибка типа данных при отрисовке плоскости: {e}")
        except Exception as e:
            print(f"Неожиданная ошибка при отрисовке плоскости: {e}")

    def mousePressEvent(self, event: Any) -> None:
        """
        Обработка нажатия кнопки мыши.
        """
        if event.button() == Qt.LeftButton:
            self.mouse_pressed = True
            self.last_mouse_pos = event.pos()

    def mouseMoveEvent(self, event: Any) -> None:
        if self.mouse_pressed or self.last_mouse_pos is not None:
            dx = event.x() - self.last_mouse_pos.x()
            dy = event.y() - self.last_mouse_pos.y()
            self.rotation_x += dy
            self.rotation_z += dx
            self.last_mouse_pos = event.pos()
            self.update()

    def mouseReleaseEvent(self, event: Any) -> None:
        """
        Обработка отпускания кнопки мыши.
        """
        if event.button() == Qt.LeftButton:
            self.mouse_pressed = False
            self.last_mouse_pos = None
