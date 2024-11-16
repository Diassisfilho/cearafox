import glm

# Calculate position of the arwing
def arwing_position(instance):
    # Translate the model along the z-axis to make it distant from the camera
    instance.model = glm.translate(instance.model, glm.vec3(0, 0, -10))