import glfw
from OpenGL.GL import *

from arwing import Arwing
from andross import *
from shaders import shaders_setup
from models import setup_model
from visualization import lighting_setup
from camera import Camera

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

# Render loop
while not glfw.window_should_close(window):
    # Clear screen
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Black background
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    
    # Use shader program
    glUseProgram(shader_program)

    lighting_setup(shader_program)

    # Excecute camera actions
    camera_instance.run_loop()

    # Draw Arwing
    arwing_instance.run_loop()

    # Draw Andross
    andross_instance.draw_model()

    # Swap buffers and poll events
    glfw.swap_buffers(window)
    glfw.poll_events()

# Cleanup resources
glDeleteProgram(shader_program)

# Terminate GLFW
glfw.terminate()