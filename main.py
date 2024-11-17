import glfw
from OpenGL.GL import *

from arwing import Arwing
from andross import Andross
from scenario import Castle, GoldRing, Skybox
from shaders import shaders_setup
from models import setup_model
from visualization import lighting_setup
from player_camera import PlayerCamera
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
player_camera = PlayerCamera(shader_program)

# Setup arwing
arwing_model = setup_model(shader_program, 'arwing.obj', 'arwing.mtl')
arwing_instance = Arwing(arwing_model)

# Setup scenario
scenario_model = setup_model(shader_program, './PeachsCastleExterior/Peaches Castle.obj', './PeachsCastleExterior/Peaches Castle.mtl')
scenario_instance = Castle(scenario_model)

# Setup Gold Ring
gold_ring_model = setup_model(shader_program, 'Gold Ring.obj', 'Gold Ring.mtl')
gold_ring_instance = GoldRing(gold_ring_model)

# Setup skybox
skybox_instance = Skybox("Skybox")

# Setup text renderer
text_renderer = TextRenderer("star-fox-starwing.ttf", 24)

# Enable depth testing
glEnable(GL_DEPTH_TEST)

# Render loop
while not glfw.window_should_close(window):
    # Clear screen
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Black background
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    
    # Use shader program
    glUseProgram(shader_program)

    lighting_setup(shader_program)

    # Execute camera actions
    player_camera.run_loop(window)

    # Draw Scenario 
    scenario_instance.run_loop()

    # Update Arwing position and rotation to follow the camera
    arwing_instance.update_position_and_rotation(player_camera.position, player_camera.front, player_camera.rotation)

    # Draw arwing
    arwing_instance.run_loop()

    # Draw Gold Ring
    gold_ring_instance.run_loop()

    # Render skybox
    skybox_instance.draw(player_camera)

    # Render text
    glUseProgram(0)  # Disable shader program to render text
    camera_pos_text = f"Camera {player_camera.position.x:.2f},{player_camera.position.y:.2f},{player_camera.position.z:.2f}"
    text_renderer.render_text(camera_pos_text, 0, 0.9, 0.5, (1.0, 1.0, 1.0))
    arwing_pos_text = f"Arwing {arwing_instance.position.x:.2f},{arwing_instance.position.y:.2f},{arwing_instance.position.z:.2f}"
    text_renderer.render_text(arwing_pos_text, 0, -0.9, 0.5, (1.0, 1.0, 1.0))

    # Swap buffers and poll events
    glfw.swap_buffers(window)
    glfw.poll_events()

# Cleanup resources
glDeleteProgram(shader_program)
glDeleteProgram(skybox_instance.shader_program)

# Terminate GLFW
glfw.terminate()