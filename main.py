import glfw
from OpenGL.GL import *
import glm

from arwing import Arwing
from andross import Andross
from scenario import Castle, GoldRing, Skybox
from shaders import shaders_setup
from models import setup_model
from visualization import lighting_setup
from player_camera import PlayerCamera
from dev_camera import DevCamera, setup_mouse_movimentation
from text_renderer import TextRenderer

# Initialize GLFW
if not glfw.init():
    exit()

# Create a windowed mode window and its OpenGL context
width, height = 800, 600
window = glfw.create_window(width, height, "CearaFox", None, None)
if not window:
    glfw.terminate()
    exit()

# Get the primary monitor's video mode
monitor = glfw.get_primary_monitor()
video_mode = glfw.get_video_mode(monitor)

# Calculate the center position
center_x = (video_mode.size.width - width) // 2
center_y = (video_mode.size.height - height) // 2

# Set the window position
glfw.set_window_pos(window, center_x, center_y)

# Make the window's context current
glfw.make_context_current(window)

shader_program = shaders_setup('vertex_shader.glsl', 'fragment_shader.glsl')

# Setup cameras
camera_instance = DevCamera(shader_program)
setup_mouse_movimentation(camera_instance, window)

# Setup arwing
arwing_model = setup_model(shader_program, 'arwing.obj', 'arwing.mtl')
arwing_instance = Arwing(arwing_model)

# Setup scenario
scenario_model = setup_model(shader_program, './PeachsCastleExterior/Peaches Castle.obj', './PeachsCastleExterior/Peaches Castle.mtl')
scenario_instance = Castle(scenario_model)

# Setup Gold Rings
gold_ring_positions = [
    (0.00, 6.00, -14.00),
    (-12.13, -10.68, 9.61),
    (-35.60, -10.04, -1.27),
    (-46.12, -9.34, -38.85),
    (-68.33, -7.83, -14.50),
    (-2.90, -11.90, -55.31),
    (-2.90, -11.90, -45.31),
    (28.38, -13.07, -57.73),
    (39.85, -9.39, -76.39),
    (43.15, -13.68, -40.28),
    (-53.22, 2.48, -70.81),
    (61.51, -11.87, 28.54),
    (0.45, 70.05, -79.15),
    ]

gold_ring_rotations = [
    (0.08, -0.49, 0.00),
    (0.01, 1.33, 0.00),
    (-0.014, 0.27, 0.00),
    (-0.014, 0.27, 0.00),
    (-0.014, 0.27, 0.00),
    (-0.07, 0.11, 0.00),
    (-0.07, 0.11, 0.00),
    (-0.07, -6.44, 0.00),
    (0.47, 4.71, 0.00),
    (-0.03, -1.93, 0.00),
    (-0.09, -1.43, 0.00),
    (0.03, -8.07, 0.00),
    (0.00, 1.58, 0.00)
    ]
gold_ring_instances = [None for x in range(len(gold_ring_positions))]

for index, instance in enumerate(gold_ring_instances):
    gold_ring_model = setup_model(shader_program, 'Gold Ring.obj', 'Gold Ring.mtl')
    gold_ring_instances[index] = GoldRing(gold_ring_model)
    gold_ring_instances[index].update_position_and_rotation(
        glm.vec3(gold_ring_positions[index]),
        glm.vec3(gold_ring_rotations[index])
    )

# Setup skybox
skybox_instance = Skybox("Skybox")

# Setup text renderer
text_renderer = TextRenderer("star-fox-starwing.ttf", 24)

# Gameplay logic variables
passed_rings_count = 0

# Enable depth testing
glEnable(GL_DEPTH_TEST)

# Initialize time variables for delta_time calculation
last_time = glfw.get_time()

# Render loop
while not glfw.window_should_close(window):
    # Calculate delta_time
    current_time = glfw.get_time()
    delta_time = current_time - last_time
    last_time = current_time

    # Clear screen
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Black background
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    
    # Use shader program
    glUseProgram(shader_program)

    lighting_setup(shader_program)

    # Execute camera actions
    camera_instance.run_loop(window)

    # Draw Scenario 
    scenario_instance.run_loop()

    # # Update Arwing position and rotation to follow the camera
    # arwing_instance.update_position_and_rotation(camera_instance, delta_time)

    # # Draw arwing
    # arwing_instance.run_loop()

    for gold_ring_instance in gold_ring_instances:
        # Draw Gold Ring
        gold_ring_instance.run_loop()

        # Check for collision with the Gold Ring
        if gold_ring_instance.check_collision(arwing_instance.position):
            passed_rings_count += 1

    # Render skybox
    skybox_instance.draw(camera_instance)

    # Render text
    glUseProgram(0)  # Disable shader program to render text
    camera_pos_text = f"Camera {camera_instance.position.x:.2f},{camera_instance.position.y:.2f},{camera_instance.position.z:.2f}"
    text_renderer.render_text(camera_pos_text, -0.2, 0.9, 0.5, (1.0, 1.0, 1.0))
    camera_pos_text = f"Camera Rotation {camera_instance.rotation.x:.2f},{camera_instance.rotation.y:.2f},{camera_instance.rotation.z:.2f}"
    text_renderer.render_text(camera_pos_text, -0.95, -0.8, 0.5, (1.0, 1.0, 1.0))
    arwing_pos_text = f"Arwing {arwing_instance.position.x:.2f},{arwing_instance.position.y:.2f},{arwing_instance.position.z:.2f}"
    text_renderer.render_text(arwing_pos_text, 0, -0.9, 0.5, (1.0, 1.0, 1.0))
    text_renderer.render_text(f'Rings {passed_rings_count};{len(gold_ring_instances)}', -0.95, 0.9, 0.5, (1.0, 1.0, 1.0))

    # Swap buffers and poll events
    glfw.swap_buffers(window)
    glfw.poll_events()

# Cleanup resources
glDeleteProgram(shader_program)
glDeleteProgram(skybox_instance.shader_program)

# Terminate GLFW
glfw.terminate()