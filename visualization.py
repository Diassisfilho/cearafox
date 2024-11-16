from OpenGL.GL import *
import glm

# Camera setup
def camera_setup(shader_program,position=glm.vec3(0, 3, 8)):
    view = glm.lookAt(glm.vec3(0, 3, 8), glm.vec3(0, 0, 0), glm.vec3(0, 1, 0))
    projection = glm.perspective(glm.radians(45), 800/600, 0.1, 100.0)
    glUniformMatrix4fv(glGetUniformLocation(shader_program, 'view'), 1, GL_FALSE, glm.value_ptr(view))
    glUniformMatrix4fv(glGetUniformLocation(shader_program, 'projection'), 1, GL_FALSE, glm.value_ptr(projection))
    glUniform3fv(glGetUniformLocation(shader_program, 'viewPos'), 1, glm.value_ptr(position))

def lighting_setup(shader_program, position=glm.vec3(5, 5, 5), color=glm.vec3(1, 1, 1)):
    # Lighting and camera positions
    glUniform3fv(glGetUniformLocation(shader_program, 'lightPos'), 1, glm.value_ptr(position))
    glUniform3fv(glGetUniformLocation(shader_program, 'lightColor'), 1, glm.value_ptr(color))