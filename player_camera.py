import glm
import glfw
from OpenGL.GL import *

class PlayerCamera:
    def __init__(self, shader_program):
        self.shader_program = shader_program
        self.position = glm.vec3(0, 3, 10)
        self.projection = glm.perspective(glm.radians(45), 800/600, 0.1, 1000.0)
        self.rotation = glm.vec3(0, glm.radians(-90), 0)  # Looking towards positive Z-axis
        self.front = glm.vec3(0, 0, 1)  # Positive Z-axis direction
        self.up = glm.vec3(0, 1, 0)
        self.right = glm.vec3(1, 0, 0)
        self.update_view_matrix()  # Initialize the view matrix

    def process_input(self, window):
        rotation_speed = glm.radians(1.0)
        movement_speed = 0.1

        if glfw.get_key(window, glfw.KEY_W) == glfw.PRESS:
            self.rotation.x -= rotation_speed
        if glfw.get_key(window, glfw.KEY_S) == glfw.PRESS:
            self.rotation.x += rotation_speed
        if glfw.get_key(window, glfw.KEY_A) == glfw.PRESS:
            self.rotation.y -= rotation_speed
        if glfw.get_key(window, glfw.KEY_D) == glfw.PRESS:
            self.rotation.y += rotation_speed

        # Move forward continuously
        self.position += self.front * movement_speed

    def update_view_matrix(self):
        # Calculate the new front vector
        front = glm.vec3(
            glm.cos(self.rotation.y) * glm.cos(self.rotation.x),
            glm.sin(self.rotation.x),
            glm.sin(self.rotation.y) * glm.cos(self.rotation.x)
        )
        self.front = glm.normalize(front)
        
        # Recalculate the right and up vector
        self.right = glm.normalize(glm.cross(self.front, glm.vec3(0, 1, 0)))
        self.up = glm.normalize(glm.cross(self.right, self.front))
        
        # Update the view matrix
        self.view = glm.lookAt(self.position, self.position + self.front, self.up)

    def run_loop(self, window):
        self.process_input(window)
        self.update_view_matrix()
        glUniformMatrix4fv(glGetUniformLocation(self.shader_program, 'view'), 1, GL_FALSE, glm.value_ptr(self.view))
        glUniformMatrix4fv(glGetUniformLocation(self.shader_program, 'projection'), 1, GL_FALSE, glm.value_ptr(self.projection))
        glUniform3fv(glGetUniformLocation(self.shader_program, 'viewPos'), 1, glm.value_ptr(self.position))