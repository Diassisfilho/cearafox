import glfw
from OpenGL.GL import *

from arwing import Arwing
from andross import *
from shaders import shaders_setup
from models import setup_model
from visualization import lighting_setup
from camera import Camera
from text_renderer import TextRenderer

# Initialize GLFW
if not glfw.init():
    exit()

# Create a windowed mode window and its OpenGL context
window = glfw.create_window(800, 600, "CearaFox", None, None)
if not window:
    glfw.terminate()
    exit()
glfw.make_context_current(window)

shader_program = shaders_setup('vertex_shader.glsl', 'fragment_shader.glsl')

# Setup camera
camera_instance = Camera(shader_program)

# Setup arwing
arwing_model = setup_model(shader_program, 'arwing.obj', 'arwing.mtl')
arwing_instance = Arwing(arwing_model)

# Setup andross
andross_instance = setup_model(shader_program, 'andross.obj', 'andross.mtl')
andross_initial_state(andross_instance)

# Enable depth testing
glEnable(GL_DEPTH_TEST)

# Setup text renderer
text_renderer = TextRenderer("star-fox-starwing.ttf", 24)

# Render loop
while not glfw.window_should_close(window):
    # Clear screen
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Black background
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    
    # Use shader program
    glUseProgram(shader_program)

    lighting_setup(shader_program)

    # Draw Arwing
    arwing_instance.run_loop()

    # Update camera to follow Arwing
    camera_instance.update_view(arwing_instance.position)

    # Execute camera actions
    camera_instance.run_loop()

    # Draw Andross
    andross_instance.draw_model()

    # Render text
    glUseProgram(0)  # Disable shader program to render text
    arwing_pos_text = f"Arwing {arwing_instance.position.y:.2f}, {arwing_instance.position.z:.2f}"
    text_renderer.render_text(arwing_pos_text, -0.95, 0.9, 0.5, (1.0, 1.0, 1.0))
    camera_pos_text = f"Camera {camera_instance.position.y:.2f}, {camera_instance.position.z:.2f}"
    text_renderer.render_text(camera_pos_text, 0.10, 0.9, 0.5, (1.0, 1.0, 1.0))

    # Swap buffers and poll events
    glfw.swap_buffers(window)
    glfw.poll_events()

# Cleanup resources
glDeleteProgram(shader_program)

# Terminate GLFW
glfw.terminate()