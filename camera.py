import glm
import glfw
from OpenGL.GL import *

class Camera:
    def __init__(self, shader_program):
        self.shader_program = shader_program
        self.position = glm.vec3(0, 3, 8)
        self.projection = glm.perspective(glm.radians(45), 800/600, 0.1, 1000.0)
        self.view = glm.lookAt(self.position, glm.vec3(0, 0, 0), glm.vec3(0, 1, 0))

    def update_view(self, target_position):
        # Set the camera position relative to the target (Arwing)
        self.view = glm.lookAt(self.position, glm.vec3(target_position.x, self.position.y, target_position.z), glm.vec3(0, 1, 0))

    def run_loop(self):
        self.position.z = (0.001 * glfw.get_time())

        glUniformMatrix4fv(glGetUniformLocation(self.shader_program, 'view'), 1, GL_FALSE, glm.value_ptr(self.view))
        glUniformMatrix4fv(glGetUniformLocation(self.shader_program, 'projection'), 1, GL_FALSE, glm.value_ptr(self.projection))
        glUniform3fv(glGetUniformLocation(self.shader_program, 'viewPos'), 1, glm.value_ptr(self.position))