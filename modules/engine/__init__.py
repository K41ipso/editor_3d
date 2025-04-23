"""
Инициализация пакета engine.
"""

from .core import Engine
from .loader import load_state, save_state
from .render import Renderer
from .opengl_widget import OpenGLWidget

__all__ = ["Engine", "load_state", "save_state", "Renderer", "OpenGLWidget"]