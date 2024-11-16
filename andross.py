import glm
from models import model_position

# Calculate position of the arwing
def andross_initial_state(instance):
    # Translate the model along the z-axis to make it distant from the camera
    instance.model = glm.scale(glm.mat4(1.0), glm.vec3(0.05, 0.05, 0.05))
    model_position(instance, glm.vec3(0.0,0.0,-190))
    