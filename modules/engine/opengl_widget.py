from typing import Any

from OpenGL.GL import (
    GL_COLOR_BUFFER_BIT,
    GL_DEPTH_BUFFER_BIT,
    GL_DEPTH_TEST,
    GL_LINES,
    GL_MODELVIEW,
    GL_PROJECTION,
    GL_QUADS,
    glBegin,
    glClear,
    glClearColor,
    glColor3f,
    glEnable,
    glEnd,
    glLoadIdentity,
    glMatrixMode,
    glRotatef,
    glTranslatef,
    glVertex3f,
    glViewport,
)
from OpenGL.GLU import gluPerspective
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QOpenGLWidget


class OpenGLWidget(QOpenGLWidget):
    def __init__(self, space_data: Any = None, parent: Any = None) -> None:
        super().__init__(parent)
        self.space_data = space_data
        self.rotation_x = 0  # Угол поворота по оси X
        self.rotation_y = 0  # Угол поворота по оси Y
        self.last_mouse_pos = None  # Последняя позиция мыши

    def initializeGL(self) -> None:
        """
        Инициализация OpenGL.
        """
        glClearColor(0.1, 0.1, 0.1, 1.0)  # Темно-серый фон
        glEnable(GL_DEPTH_TEST)

    def resizeGL(self, width: int, height: int) -> None:
        """
        Настройка проекции при изменении размеров окна.
        """
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, width / height, 0.1, 50.0)
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self) -> None:
        """
        Отрисовка OpenGL.
        """
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(0.0, 0.0, -5.0)  # Перемещение камеры
        glRotatef(self.rotation_x, 1, 0, 0)  # Поворот по оси X
        glRotatef(self.rotation_y, 0, 1, 0)  # Поворот по оси Y

        # Рисуем координатную сетку
        self.draw_coordinate_grid()

        # Рисуем куб (пример примитивного объекта)
        self.draw_cube()

    def draw_cube(self) -> None:
        """
        Рисует куб (пример примитивного объекта).
        """
        glBegin(GL_QUADS)
        glColor3f(1.0, 0.0, 0.0)  # Красный
        glVertex3f(1.0, 1.0, -1.0)
        glVertex3f(-1.0, 1.0, -1.0)
        glVertex3f(-1.0, 1.0, 1.0)
        glVertex3f(1.0, 1.0, 1.0)

        glColor3f(0.0, 1.0, 0.0)  # Зеленый
        glVertex3f(1.0, -1.0, 1.0)
        glVertex3f(-1.0, -1.0, 1.0)
        glVertex3f(-1.0, -1.0, -1.0)
        glVertex3f(1.0, -1.0, -1.0)
        glEnd()

    def draw_coordinate_grid(self) -> None:
        """
        Рисует координатную сетку.
        """
        try:
            print("Начало рисования координатной сетки...")

            # Установка цвета сетки
            glColor3f(0.5, 0.5, 0.5)  # Серый цвет для сетки
            print("Цвет сетки успешно установлен.")

            # Начало рисования линий
            glBegin(GL_LINES)
            print("Начало рисования линий (glBegin).")

            grid_size = 10
            step = 1
            for i in range(-grid_size, grid_size + 1, step):
                # Линии по оси X
                glVertex3f(i, 0, -grid_size)
                glVertex3f(i, 0, grid_size)

                # Линии по оси Z
                glVertex3f(-grid_size, 0, i)
                glVertex3f(grid_size, 0, i)

            glEnd()
            print("Рисование линий завершено (glEnd).")
            print("Координатная сетка успешно нарисована.")
        except Exception as e:
            print(f"Неожиданная ошибка при рисовании координатной сетки: {e}")

    def mousePressEvent(self, event: Any) -> None:
        """
        Обработка нажатия кнопки мыши.
        """
        if event.button() == Qt.LeftButton:
            self.last_mouse_pos = event.pos()

    def mouseMoveEvent(self, event: Any) -> None:
        """
        Обработка движения мыши.
        """
        if self.last_mouse_pos is not None:
            dx = event.x() - self.last_mouse_pos.x()  # type: ignore
            dy = event.y() - self.last_mouse_pos.y()
            self.rotation_x += dy  # Изменяем угол поворота по оси X
            self.rotation_y += dx  # Изменяем угол поворота по оси Y
            self.last_mouse_pos = event.pos()
            self.update()  # Перерисовываем виджет

    def mouseReleaseEvent(self, event: Any) -> None:
        """
        Обработка отпускания кнопки мыши.
        """
        self.last_mouse_pos = None
