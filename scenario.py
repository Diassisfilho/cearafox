import random
import glm
from models import model_position
from OpenGL.GL import *
from PIL import Image
from shaders import shaders_setup
from utils import setup_vao_vbo_skybox

class Castle:
    def __init__(self, model_instance):
        self.model_instance = model_instance
        self.position = glm.vec3(0.0, -10, -40)
        self.initial_state()
    
    def initial_state(self):
        self.model_instance.model = glm.mat4(1.0)
        self.model_instance.model = glm.translate(self.model_instance.model, self.position)
        self.model_instance.model = glm.scale(self.model_instance.model, glm.vec3(10,10,10))
        self.model_instance.model = glm.rotate(self.model_instance.model, glm.radians(180), glm.vec3(0, 1, 0))

    def run_loop(self):
        self.model_instance.draw_model()

class GoldRing:
    def __init__(self, model_instance):
        self.model_instance = model_instance
        self.position = glm.vec3(0.0, 0.0, 0.0)
        self.rotation_angle = float(random.randint(0,360))  # Initialize rotation angle
        self.was_crossed = False
        self.collision_radius = 2.0  # Adjust based on the ring's size
        self.initial_state()
    
    def initial_state(self):
        self.model_instance.model = glm.mat4(1.0)
        self.model_instance.model = glm.translate(self.model_instance.model, self.position)
    
    def update_position_and_rotation(self, position, rotation):
        self.position = position
        self.rotation = rotation
        self.update_model_matrix()

    def update_model_matrix(self):
        self.model_instance.model = glm.mat4(1.0)
        self.model_instance.model = glm.translate(self.model_instance.model, self.position)
        self.model_instance.model = glm.rotate(self.model_instance.model, glm.radians(self.rotation[0]), glm.vec3(1, 0, 0))
        self.model_instance.model = glm.rotate(self.model_instance.model, glm.radians(self.rotation[1]), glm.vec3(0, 1, 0))
        self.model_instance.model = glm.rotate(self.model_instance.model, glm.radians(self.rotation[2]), glm.vec3(0, 0, 1))

    def run_loop(self):
        # Increment the rotation angle
        self.rotation_angle += glm.radians(1)  # Adjust the rotation speed as needed

        # Reset the model matrix
        self.model_instance.model = glm.mat4(1.0)

        # Apply transformations
        self.model_instance.model = glm.translate(self.model_instance.model, self.position)
        self.model_instance.model = glm.rotate(self.model_instance.model, self.rotation_angle, glm.vec3(0, 0, 1))  # Rotate around Z-axis

        # Draw the model
        self.model_instance.draw_model()
    
    def check_collision(self, arwing_position):
        if not self.was_crossed:
            # Calculate the distance between the Arwing and the Gold Ring
            distance = glm.distance(self.position, arwing_position)
            if distance < self.collision_radius:
                self.was_crossed = True
                return True
        return False

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

    def draw(self, camera_instance):
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