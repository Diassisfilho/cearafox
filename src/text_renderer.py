import freetype
import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *

class TextRenderer:
    def __init__(self, font_path, font_size):
        self.face = freetype.Face(font_path)
        self.face.set_char_size(font_size * 64)
        self.font_size = font_size

    def render_text(self, text, x, y, scale, color):
        glPushMatrix()
        glLoadIdentity()
        glColor3f(*color)
        glRasterPos2f(x, y)
        for char in text:
            self.face.load_char(char)
            bitmap = self.face.glyph.bitmap
            width = bitmap.width
            rows = bitmap.rows
            buffer = np.array(bitmap.buffer, dtype=np.ubyte)  # Convert buffer to NumPy array
            data = np.zeros((rows, width, 4), dtype=np.ubyte)
            data[:, :, 0] = buffer.reshape(rows, width)[::-1]  # Flip the rows
            data[:, :, 1] = buffer.reshape(rows, width)[::-1]  # Flip the rows
            data[:, :, 2] = buffer.reshape(rows, width)[::-1]  # Flip the rows
            data[:, :, 3] = buffer.reshape(rows, width)[::-1]  # Flip the rows
            glDrawPixels(width, rows, GL_RGBA, GL_UNSIGNED_BYTE, data)
            glBitmap(0, 0, 0, 0, self.face.glyph.advance.x // 64, 0, None)
        glPopMatrix()