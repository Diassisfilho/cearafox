import glm
import glfw
from src.models import model_position

class Andross:
    def __init__(self, model_instance):
        self.model_instance = model_instance
        self.position = glm.vec3(0.0,0.0,0.0)
        self.initial_state()
    
    def initial_state(self):
        self.model_instance.model = glm.scale(glm.mat4(1.0), glm.vec3(0.05, 0.05, 0.05))
        model_position(self.model_instance, glm.vec3(0.0,0.0,-190))

    def run_loop(self):
        model_position(self.model_instance, self.position)
        self.model_instance.draw_model()