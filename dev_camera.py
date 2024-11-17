import glm
import glfw
from OpenGL.GL import *

class DevCamera:
    def __init__(self, shader_program):
        self.shader_program = shader_program
        self.position = glm.vec3(0, 3, 10)
        self.projection = glm.perspective(glm.radians(45), 800/600, 0.1, 1000.0)
        self.rotation = glm.vec3(0, glm.radians(-90), 0)  # Looking towards positive Z-axis
        self.front = glm.vec3(0, 0, 1)  # Positive Z-axis direction
        self.up = glm.vec3(0, 1, 0)
        self.right = glm.vec3(1, 0, 0)
        self.last_x = 400
        self.last_y = 300
        self.first_mouse = True
        self.update_view_matrix()  # Initialize the view matrix

    def process_input(self, window):
        movement_speed = 0.1
        if glfw.get_key(window, glfw.KEY_W) == glfw.PRESS:
            self.position += self.front * movement_speed
        if glfw.get_key(window, glfw.KEY_S) == glfw.PRESS:
            self.position -= self.front * movement_speed
        if glfw.get_key(window, glfw.KEY_A) == glfw.PRESS:
            self.position -= self.right * movement_speed
        if glfw.get_key(window, glfw.KEY_D) == glfw.PRESS:
            self.position += self.right * movement_speed
        if glfw.get_key(window, glfw.KEY_SPACE) == glfw.PRESS:
            self.position += self.up * movement_speed
        if glfw.get_key(window, glfw.KEY_LEFT_SHIFT) == glfw.PRESS:
            self.position -= self.up * movement_speed

    def process_mouse_movement(self, xpos, ypos):
        sensitivity = 0.001
        if self.first_mouse:
            self.last_x = xpos
            self.last_y = ypos
            self.first_mouse = False

        xoffset = xpos - self.last_x
        yoffset = self.last_y - ypos  # Reversed since y-coordinates go from bottom to top
        self.last_x = xpos
        self.last_y = ypos

        xoffset *= sensitivity
        yoffset *= sensitivity

        self.rotation.y += xoffset
        self.rotation.x += yoffset

        # Constrain the pitch
        if self.rotation.x > glm.radians(89.0):
            self.rotation.x = glm.radians(89.0)
        if self.rotation.x < glm.radians(-89.0):
            self.rotation.x = glm.radians(-89.0)

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