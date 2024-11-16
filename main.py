import glfw
from OpenGL.GL import *

from airwing import arwing_position
from shaders import shaders_setup
from models import setup_model, rotate_instance_by_time
from visualization import camera_setup, lighting_setup

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

# Setup arwing
arwing_instance = setup_model(shader_program, 'arwing.obj', 'arwing.mtl')
# arwing_position(arwing_instance)

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

    camera_setup(shader_program)
    lighting_setup(shader_program)

    # Draw Arwing
    rotate_instance_by_time(arwing_instance)
    arwing_instance.draw_model()

    # Swap buffers and poll events
    glfw.swap_buffers(window)
    glfw.poll_events()

# Cleanup resources
glDeleteProgram(shader_program)

# Terminate GLFW
glfw.terminate()