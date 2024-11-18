import glfw
from OpenGL.GL import *
import glm
import time

from src.arwing import Arwing
from src.andross import Andross
from src.scenario import Castle, GoldRing, Skybox
from src.shaders import shaders_setup
from src.models import setup_model
from src.ilumination import glob_lighting_draw, difuse_lighting_draw
from src.player_camera import PlayerCamera
from src.dev_camera import DevCamera, setup_mouse_movimentation
from src.text_renderer import TextRenderer
from src.utils import gold_ring_positions, gold_ring_rotations
from configs import DEV_MODE, DIFUSE_LIGHT_MODE, LIMIT_TIME

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

# Setup shaders
shader_program = shaders_setup('shaders/vertex_shader.glsl', 'shaders/fragment_shader_glob_ilum.glsl')
if(DIFUSE_LIGHT_MODE):
    shader_program = shaders_setup('shaders/vertex_shader.glsl', 'shaders/fragment_shader_difuse.glsl')

# Setup camera
camera_instance = PlayerCamera(shader_program)
if(DEV_MODE):
    camera_instance = DevCamera(shader_program)
    setup_mouse_movimentation(camera_instance, window)

# Setup arwing
arwing_model = setup_model(shader_program, 'assets/Arwing/arwing.obj', 'assets/Arwing/arwing.mtl')
arwing_instance = Arwing(arwing_model)

# Setup scenario
scenario_model = setup_model(shader_program, 'assets/PeachsCastleExterior/Peaches Castle.obj', 'assets/PeachsCastleExterior/Peaches Castle.mtl')
scenario_instance = Castle(scenario_model)

# Setup Gold Rings
gold_ring_instances = [None for x in range(len(gold_ring_positions))]

for index, instance in enumerate(gold_ring_instances):
    gold_ring_model = setup_model(shader_program, 'assets/Gold/Gold Ring.obj', 'assets/Gold/Gold Ring.mtl')
    gold_ring_instances[index] = GoldRing(gold_ring_model)
    gold_ring_instances[index].update_position_and_rotation(
        glm.vec3(gold_ring_positions[index]),
        glm.vec3(gold_ring_rotations[index])
    )

# Setup skybox
skybox_instance = Skybox("assets/Skybox")

# Setup text renderer
text_renderer = TextRenderer("fonts/star-fox-starwing.ttf", 24)

# Enable depth testing
glEnable(GL_DEPTH_TEST)

# Gameplay logic variables
crossed_rings_count = 0
is_failed = False
last_time = glfw.get_time()
start_time = time.time()

# Render loop
while not glfw.window_should_close(window):
    # Calculate delta_time
    current_time = glfw.get_time()
    delta_time = current_time - last_time
    last_time = current_time

    # Calculate elapsed time
    elapsed_time = time.time() - start_time

    if (not DEV_MODE):
        # Check if timeout is reached
        if elapsed_time >= LIMIT_TIME:
            # Reset camera position
            camera_instance.position = glm.vec3(0, 0, 0)
            camera_instance.rotation = glm.vec3(0, glm.radians(-90), 0)
            camera_instance.update_view_matrix()

            # Reset all rings' was_crossed variable
            for gold_ring_instance in gold_ring_instances:
                gold_ring_instance.was_crossed = False
            
            if crossed_rings_count < len(gold_ring_instances):
                is_failed = True
            else:
                is_failed = False

            # Reset count
            crossed_rings_count = 0

            # Reset the timer
            start_time = time.time()

    # Clear screen
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Black background
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    
    # Use shader program
    glUseProgram(shader_program)

    if(DIFUSE_LIGHT_MODE):
        difuse_lighting_draw(shader_program)
    else:
        glob_lighting_draw(shader_program)

    # Execute camera actions
    camera_instance.run_loop(window)

    # Draw Scenario 
    scenario_instance.run_loop()

    if (not DEV_MODE):
        # Update Arwing position and rotation to follow the camera
        arwing_instance.update_position_and_rotation(camera_instance, delta_time)

        # Draw arwing
        arwing_instance.run_loop()

    for gold_ring_instance in gold_ring_instances:
        # Draw Gold Ring
        gold_ring_instance.run_loop()

        # Check for collision with the Gold Ring
        if gold_ring_instance.check_collision(arwing_instance.position):
            crossed_rings_count += 1

    # Render skybox
    skybox_instance.draw(camera_instance)

    # Render text
    normal_text_color = (1.0,1.0,1.0)
    fatal_text_color = (1.0,0.0,0.0)
    win_text_color = (1.0, 1.0, 0.0)

    if (not DEV_MODE):
        glUseProgram(0)  # Disable shader program to render text
        remain_time = LIMIT_TIME - elapsed_time
        time_text_color = fatal_text_color if remain_time <= 10 else normal_text_color
        text_renderer.render_text(f'Rings {crossed_rings_count};{len(gold_ring_instances)}', -0.95, 0.9, 0.5, normal_text_color)
        text_renderer.render_text(f'Elapsed time {remain_time:.2f}', 0.2, 0.9, 0.5, time_text_color)
        if(crossed_rings_count == len(gold_ring_instances)):
            text_renderer.render_text("You win", -0.1, 0, 0.5, win_text_color)
        if(is_failed and remain_time >= LIMIT_TIME*0.9):
            text_renderer.render_text("You Fail", -0.15, 0, 0.5, win_text_color)
        text_renderer.render_text("WASD to Moviment", -0.95, -0.7, 0.5, normal_text_color)
        text_renderer.render_text("Space to Boost", -0.95, -0.8, 0.5, normal_text_color)
        text_renderer.render_text("Shift to Drift", -0.95, -0.9, 0.5, normal_text_color)
    elif (DEV_MODE):
        glUseProgram(0)  # Disable shader program to render text
        camera_pos_text = f"Camera {camera_instance.position.x:.2f},{camera_instance.position.y:.2f},{camera_instance.position.z:.2f}"
        text_renderer.render_text(camera_pos_text, -0.95, 0.9, 0.5, normal_text_color)
        camera_pos_text = f"Camera Rotation {camera_instance.rotation.x:.2f},{camera_instance.rotation.y:.2f},{camera_instance.rotation.z:.2f}"
        text_renderer.render_text(camera_pos_text, -0.95, -0.9, 0.5, normal_text_color)
        text_renderer.render_text("WASD to Moviment", -0.95, -0.5, 0.5, normal_text_color)
        text_renderer.render_text("Mouse to See Around", -0.95, -0.6, 0.5, normal_text_color)
        text_renderer.render_text("Shift Go Down", -0.95, -0.7, 0.5, normal_text_color)
        text_renderer.render_text("Space Go Up", -0.95, -0.8, 0.5, normal_text_color)

    # Swap buffers and poll events
    glfw.swap_buffers(window)
    glfw.poll_events()

# Cleanup resources
glDeleteProgram(shader_program)
glDeleteProgram(skybox_instance.shader_program)

# Terminate GLFW
glfw.terminate()