import glm
import glfw
from models import model_position

class Arwing:
    def __init__(self, model_instance):
        self.model_instance = model_instance
        self.velocity = 0.01
        self.initial_state()
    
    def initial_state(self):
        model_position(self.model_instance, glm.vec3(0.0,0.0,0.0))
        self.model_instance.model = glm.rotate(self.model_instance.model, glm.radians(180), glm.vec3(0,1,0))
        self.model_instance.model = glm.rotate(self.model_instance.model, glm.radians(10), glm.vec3(1,0,0))

    def run_loop(self):
        model_position(self.model_instance, glm.vec3(0.0,0.0,glfw.get_time()*self.velocity))
        self.model_instance.draw_model()