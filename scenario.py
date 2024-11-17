import glm
from models import model_position
from OpenGL.GL import *
from PIL import Image
from shaders import shaders_setup
from utils import setup_vao_vbo_skybox
class Castle:
    def __init__(self, model_instance):
        self.model_instance = model_instance
        self.position = glm.vec3(0.0,0.0,0.0)
        self.initial_state()
    
    def initial_state(self):
        model_position(self.model_instance, glm.vec3(0.0,0,3))
        self.model_instance.model = glm.rotate(self.model_instance.model, glm.radians(180), glm.vec3(0, 1, 0))

    def run_loop(self):
        model_position(self.model_instance, self.position)
        self.model_instance.draw_model()

class Skybox:
    def __init__(self, textures_folder):
        # Load skybox textures
        skybox_faces = [
            f'{textures_folder}/sky-right.jpg',
            f'{textures_folder}/sky-left.jpg',
            f'{textures_folder}/sky-top.jpg',
            f'{textures_folder}/sky-bottom.jpg',
            f'{textures_folder}/sky-front.jpg',
            f'{textures_folder}/sky-back.jpg'
        ]
        self.texture = self.load_skybox(skybox_faces)

        # Setup skybox VAO and VBO
        self.vao = setup_vao_vbo_skybox()

        # Load skybox shader
        self.shader_program = shaders_setup('skybox_vertex_shader.glsl', 'skybox_fragment_shader.glsl')
    
    def load_skybox(self, faces):
        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_CUBE_MAP, texture_id)

        for i, face in enumerate(faces):
            image = Image.open(face)
            image = image.transpose(Image.FLIP_TOP_BOTTOM)  # Flip the image vertically
            img_data = image.convert("RGB").tobytes()
            glTexImage2D(GL_TEXTURE_CUBE_MAP_POSITIVE_X + i, 0, GL_RGB, image.width, image.height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)

        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_R, GL_CLAMP_TO_EDGE)

        return texture_id

    def draw_skybox(self, camera_instance):
        glDepthFunc(GL_LEQUAL)
        glUseProgram(self.shader_program)
        view = glm.mat4(glm.mat3(camera_instance.view))  # Remove translation from the view matrix
        projection = camera_instance.projection
        glUniformMatrix4fv(glGetUniformLocation(self.shader_program, "view"), 1, GL_FALSE, glm.value_ptr(view))
        glUniformMatrix4fv(glGetUniformLocation(self.shader_program, "projection"), 1, GL_FALSE, glm.value_ptr(projection))
        glBindVertexArray(self.vao)
        glBindTexture(GL_TEXTURE_CUBE_MAP, self.texture)
        glDrawArrays(GL_TRIANGLES, 0, 36)
        glBindVertexArray(0)
        glDepthFunc(GL_LESS)