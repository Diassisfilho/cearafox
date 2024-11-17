import glm
from models import model_position

class Arwing:
    def __init__(self, model_instance):
        self.model_instance = model_instance
        self.position = glm.vec3(0.0, 2.2, 4.0)
        self.rotation = glm.vec3(0.0, 0.0, 0.0)
        self.initial_state()
    
    def initial_state(self):
        self.update_model_matrix()

    def update_model_matrix(self):
        self.model_instance.model = glm.mat4(1.0)
        self.model_instance.model = glm.translate(self.model_instance.model, self.position)
        self.model_instance.model = glm.rotate(self.model_instance.model, -self.rotation.y + glm.radians(90), glm.vec3(0, 1, 0))  # Face backward towards the camera
        self.model_instance.model = glm.rotate(self.model_instance.model, -self.rotation.x, glm.vec3(1, 0, 0))  # Apply X rotation
        self.model_instance.model = glm.scale(self.model_instance.model, glm.vec3(0.5, 0.5, 0.5))

    def update_position_and_rotation(self, camera_position, camera_front, camera_rotation, distance):
        self.position = camera_position + camera_front * distance
        self.rotation = camera_rotation
        self.update_model_matrix()

    def run_loop(self):
        self.model_instance.draw_model()