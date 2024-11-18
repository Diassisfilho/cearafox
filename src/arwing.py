import glm
from src.models import model_position

class Arwing:
    def __init__(self, model_instance):
        self.model_instance = model_instance
        self.position = glm.vec3(0.0, 0.0, 0.0)
        self.rotation = glm.vec3(0.0, 0.0, 0.0)
        self.camera_distance = 6
        self.roll_angle = 0.0  # Current roll angle around Z-axis
        self.initial_state()
    
    def initial_state(self):
        self.update_model_matrix()

    def update_position_and_rotation(self, player_camera, delta_time):
        # Update position to follow the camera
        self.position = player_camera.position + player_camera.front * self.camera_distance + glm.vec3(0, -1, 0)
        self.rotation = player_camera.rotation
        self.update_model_matrix()

        # Get key inputs and speeds from player camera
        key_a_pressed = player_camera.key_a_pressed
        key_d_pressed = player_camera.key_d_pressed
        rotation_speed = player_camera.rotation_speed
        movement_speed = player_camera.movement_speed

        # Calculate maximum roll angle based on speeds
        base_max_roll_angle = glm.radians(45.0)  # Base maximum roll
        speed_multiplier = max(rotation_speed / player_camera.base_rotation_speed,
                               movement_speed / player_camera.base_movement_speed)
        max_roll_angle = base_max_roll_angle * speed_multiplier
        max_roll_angle = min(max_roll_angle, glm.radians(70))  # Limit to 70 degrees

        # Calculate roll speed based on speeds
        base_roll_speed = glm.radians(180)  # Base roll speed
        roll_speed = base_roll_speed * speed_multiplier

        # Determine target roll angle based on key presses
        if key_a_pressed:
            target_roll_angle = -max_roll_angle
        elif key_d_pressed:
            target_roll_angle = max_roll_angle
        else:
            target_roll_angle = 0.0

        # Smoothly interpolate the roll angle towards the target roll angle
        angle_diff = target_roll_angle - self.roll_angle
        max_angle_change = roll_speed * delta_time
        if abs(angle_diff) > max_angle_change:
            angle_change = max_angle_change * (1 if angle_diff > 0 else -1)
        else:
            angle_change = angle_diff

        self.roll_angle += angle_change

        self.update_model_matrix()

    def update_model_matrix(self):
        self.model_instance.model = glm.mat4(1.0)
        self.model_instance.model = glm.translate(self.model_instance.model, self.position)
        # Rotate to face forward along the Z-axis
        self.model_instance.model = glm.rotate(self.model_instance.model, self.rotation.x, glm.vec3(1, 0, 0))
        self.model_instance.model = glm.rotate(self.model_instance.model, - self.rotation.y + glm.radians(90), glm.vec3(0, 1, 0))
        # Apply roll rotation around Z-axis
        self.model_instance.model = glm.rotate(self.model_instance.model, self.roll_angle, glm.vec3(0, 0, 1))
        # Scale the model
        self.model_instance.model = glm.scale(self.model_instance.model, glm.vec3(0.5, 0.5, 0.5))

    def run_loop(self):
        self.model_instance.draw_model()