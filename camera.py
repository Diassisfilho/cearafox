import glm
from OpenGL.GL import *

class Camera:
    def __init__(self, shader_program):
        self.shader_program = shader_program
        self.position = glm.vec3(0, 3, 8)
        self.projection = glm.perspective(glm.radians(45), 800/600, 0.1, 100.0)
        self.view = glm.lookAt(self.position, glm.vec3(0, 0, 0), glm.vec3(0, 1, 0))

    def update_view(self, target_position):
        # Set the camera position relative to the target (Arwing)
        self.position = target_position + glm.vec3(0, 3, 8)  # Adjust the z value to -8 to position the camera behind the Arwing
        self.view = glm.lookAt(self.position, target_position, glm.vec3(0, 1, 0))

    def run_loop(self):
        glUniformMatrix4fv(glGetUniformLocation(self.shader_program, 'view'), 1, GL_FALSE, glm.value_ptr(self.view))
        glUniformMatrix4fv(glGetUniformLocation(self.shader_program, 'projection'), 1, GL_FALSE, glm.value_ptr(self.projection))
        glUniform3fv(glGetUniformLocation(self.shader_program, 'viewPos'), 1, glm.value_ptr(self.position))