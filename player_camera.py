import glm
import glfw
from OpenGL.GL import *

class PlayerCamera:
    def __init__(self, shader_program):
        self.shader_program = shader_program
        self.position = glm.vec3(0, 0, 0)
        self.projection = glm.perspective(glm.radians(45), 800 / 600, 0.1, 1000.0)
        self.rotation = glm.vec3(0, glm.radians(-90), 0)  # Looking towards positive Z-axis
        self.front = glm.vec3(0, 0, 1)  # Positive Z-axis direction
        self.up = glm.vec3(0, 1, 0)
        self.right = glm.vec3(1, 0, 0)
        self.base_rotation_speed = glm.radians(1.0)  # Base rotation speed
        self.base_movement_speed = 0.1  # Base movement speed
        self.movement_speed = self.base_movement_speed
        self.rotation_speed = self.base_rotation_speed
        self.key_a_pressed = False
        self.key_d_pressed = False
        self.update_view_matrix()  # Initialize the view matrix

    def process_input(self, window):
        rotation_speed = self.base_rotation_speed

        # Check if left shift is pressed
        if glfw.get_key(window, glfw.KEY_LEFT_SHIFT) == glfw.PRESS:
            rotation_speed += glm.radians(1.0)  # Increase rotation speed by 1 degree

        self.rotation_speed = rotation_speed  # Store rotation speed for external use

        # Check if space key is pressed for movement speed
        if glfw.get_key(window, glfw.KEY_SPACE) == glfw.PRESS:
            self.movement_speed = self.base_movement_speed * 5
        else:
            self.movement_speed = self.base_movement_speed

        # Update key press status for 'a' and 'd' keys
        self.key_a_pressed = glfw.get_key(window, glfw.KEY_A) == glfw.PRESS
        self.key_d_pressed = glfw.get_key(window, glfw.KEY_D) == glfw.PRESS

        if glfw.get_key(window, glfw.KEY_W) == glfw.PRESS:
            self.rotation.x -= rotation_speed
        if glfw.get_key(window, glfw.KEY_S) == glfw.PRESS:
            self.rotation.x += rotation_speed
        if self.key_a_pressed:
            self.rotation.y -= rotation_speed
        if self.key_d_pressed:
            self.rotation.y += rotation_speed

        # Move forward continuously
        self.position += self.front * self.movement_speed

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