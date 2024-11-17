import glm
from models import model_position

class Arwing:
    def __init__(self, model_instance):
        self.model_instance = model_instance
        self.position = glm.vec3(0.0, 2.2, 4.0)
        self.initial_state()
    
    def initial_state(self):
        self.update_model_matrix()

    def update_model_matrix(self):
        model_position(self.model_instance, self.position)
        self.model_instance.model = glm.scale(self.model_instance.model, glm.vec3(0.5, 0.5, 0.5))
        self.model_instance.model = glm.rotate(self.model_instance.model, glm.radians(180), glm.vec3(0, 1, 0))
        self.model_instance.model = glm.rotate(self.model_instance.model, glm.radians(10), glm.vec3(1, 0, 0))

    def update_position(self, camera_position, camera_front, distance):
        self.position = camera_position + camera_front * distance
        self.update_model_matrix()

    def run_loop(self):
        self.model_instance.draw_model()