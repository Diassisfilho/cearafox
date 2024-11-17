import glfw
from OpenGL.GL import *
import glm

from arwing import Arwing
from andross import Andross
from scenario import Castle, load_skybox
from shaders import shaders_setup
from models import setup_model
from utils import setup_skybox
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

# Setup mouse callback
def mouse_callback(window, xpos, ypos):
    camera_instance.process_mouse_movement(xpos, ypos)

glfw.set_cursor_pos_callback(window, mouse_callback)
glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)

# Setup cenario
scenario_model = setup_model(shader_program, './PeachsCastleExterior/Peaches Castle.obj', './PeachsCastleExterior/Peaches Castle.mtl')
scenario_instance = Castle(scenario_model)

# Setup arwing
# arwing_model = setup_model(shader_program, 'arwing.obj', 'arwing.mtl')
# arwing_instance = Arwing(arwing_model)

# # Setup andross
# andross_model = setup_model(shader_program, 'andross.obj', 'andross.mtl')
# andross_instance = Andross(andross_model)

# Enable depth testing
glEnable(GL_DEPTH_TEST)

# Setup text renderer
text_renderer = TextRenderer("star-fox-starwing.ttf", 24)

# Load skybox textures
skybox_faces = [
    "Skybox/sky-right.jpg",
    "Skybox/sky-left.jpg",
    "Skybox/sky-top.jpg",
    "Skybox/sky-bottom.jpg",
    "Skybox/sky-front.jpg",
    "Skybox/sky-back.jpg"
]
skybox_texture = load_skybox(skybox_faces)

# Setup skybox VAO and VBO
skybox_vao = setup_skybox()

# Load skybox shader
skybox_shader_program = shaders_setup('skybox_vertex_shader.glsl', 'skybox_fragment_shader.glsl')

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
    camera_instance.run_loop(window)

    # Draw Scenario 
    scenario_instance.run_loop()

    # Render skybox
    glDepthFunc(GL_LEQUAL)
    glUseProgram(skybox_shader_program)
    view = glm.mat4(glm.mat3(camera_instance.view))  # Remove translation from the view matrix
    projection = camera_instance.projection
    glUniformMatrix4fv(glGetUniformLocation(skybox_shader_program, "view"), 1, GL_FALSE, glm.value_ptr(view))
    glUniformMatrix4fv(glGetUniformLocation(skybox_shader_program, "projection"), 1, GL_FALSE, glm.value_ptr(projection))
    glBindVertexArray(skybox_vao)
    glBindTexture(GL_TEXTURE_CUBE_MAP, skybox_texture)
    glDrawArrays(GL_TRIANGLES, 0, 36)
    glBindVertexArray(0)
    glDepthFunc(GL_LESS)

    # Render text
    glUseProgram(0)  # Disable shader program to render text
    camera_pos_text = f"Camera {camera_instance.position.x:.2f},{camera_instance.position.y:.2f},{camera_instance.position.z:.2f}"
    text_renderer.render_text(camera_pos_text, 0, 0.9, 0.5, (1.0, 1.0, 1.0))

    # Swap buffers and poll events
    glfw.swap_buffers(window)
    glfw.poll_events()

# Cleanup resources
glDeleteProgram(shader_program)
glDeleteProgram(skybox_shader_program)

# Terminate GLFW
glfw.terminate()