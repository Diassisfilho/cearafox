import glm
import glfw
from models import model_position
from OpenGL.GL import *
from PIL import Image

class Castle:
    def __init__(self, model_instance):
        self.model_instance = model_instance
        self.position = glm.vec3(0.0,0.0,0.0)
        self.initial_state()
    
    def initial_state(self):
        # self.model_instance.model = glm.scale(glm.mat4(1.0), glm.vec3(0.05, 0.05, 0.05))
        model_position(self.model_instance, glm.vec3(0.0,0,3))
        self.model_instance.model = glm.rotate(self.model_instance.model, glm.radians(180), glm.vec3(0, 1, 0))
        # self.model_instance.model = glm.rotate(self.model_instance.model, glm.radians(-10), glm.vec3(1, 0, 0))

    def run_loop(self):
        model_position(self.model_instance, self.position)
        self.model_instance.draw_model()

def load_skybox(faces):
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_CUBE_MAP, texture_id)

    for i, face in enumerate(faces):
        image = Image.open(face)
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
        img_data = image.convert("RGB").tobytes()
        glTexImage2D(GL_TEXTURE_CUBE_MAP_POSITIVE_X + i, 0, GL_RGB, image.width, image.height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)

    glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_R, GL_CLAMP_TO_EDGE)

    return texture_id