from OpenGL.GL import *
import glm

# def lighting_setup(shader_program, position=glm.vec3(5, 5, 5), color=glm.vec3(1, 1, 1)):
#     # Lighting and camera positions
#     glUniform3fv(glGetUniformLocation(shader_program, 'lightPos'), 1, glm.value_ptr(position))
#     glUniform3fv(glGetUniformLocation(shader_program, 'lightColor'), 1, glm.value_ptr(color))

def lighting_setup(shader_program, ambient_color=(0.8, 0.8, 0.8)):
    glUniform3fv(glGetUniformLocation(shader_program, 'ambientColor'), 1, ambient_color)